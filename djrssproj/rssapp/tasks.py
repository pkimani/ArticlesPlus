# rssapp/tasks.py
from .models import Article
from celery import shared_task
from django.core.management import call_command
from django.db import transaction
from django.db.utils import IntegrityError
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import feedparser
import hashlib
import json
import logging
import re
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from celery.exceptions import MaxRetriesExceededError
from celery.signals import task_prerun, task_postrun
from django.db import connection
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

# Constants for rate limiting
MAX_REQUESTS_PER_MINUTE = 250  # Adjust as needed
NUM_WORKERS = 1
RATE_LIMIT_PER_WORKER = MAX_REQUESTS_PER_MINUTE / NUM_WORKERS

# Default number of hours to read articles from
DEFAULT_HOURS = 800

@task_prerun.connect
def close_old_connections(**kwargs):
    # Close the old database connections
    connection.close()

@task_postrun.connect
def close_connection_again(**kwargs):
    # Close the database connection again
    connection.close()

@shared_task
def update_articles_command():
    """Call 'update_articles' management command."""
    logger.info("Calling 'update_articles' management command")

    call_command('update_articles')
    requeue_update_articles.apply_async()

@shared_task
def requeue_update_articles():
    """Requeue the 'update_articles_command' task."""
    logger.info("Requeuing 'update_articles_command'")
    update_articles_command.apply_async()

@shared_task
def query_articles_with_null_score():
    """Query all articles with a score of null."""
    logger.info("Querying articles with null score")

    # Filter articles where score is None
    articles_with_null_score = Article.objects.filter(score__isnull=True)

    # Perform an action with the articles, e.g., log their titles
    for article in articles_with_null_score:
        logger.info(f"Querying article with null score: {article.hash}")
        query_openai_api.apply_async(args=[article.title, settings.PROMPT, article.hash], priority=3)
        

@shared_task
def download_rss_feeds(opml_content, hours=DEFAULT_HOURS):
    """Download RSS feeds and process them individually."""
    logger.info("Calling 'download_rss_feeds'")

    cutoff_time = datetime.now(timezone.utc) - timedelta(hours=int(hours))
    root = ET.fromstring(opml_content)
    outlines = (outline.get('xmlUrl') for outline in root.findall(".//outline") if outline.get('xmlUrl'))
    
    # Get the scored article hashes once to avoid repeated database hits
    scored_hashes = get_scored_article_hashes()

    # Call fetch_feed asynchronously for each feed URL
    for url in outlines:
        # Dispatch fetch_feed task asynchronously for each feed URL
        fetch_feed.apply_async(args=[url, cutoff_time, scored_hashes], priority=1)

def get_scored_article_hashes():
    """Get hashes of articles with a score greater than or equal to 0."""
    logger.info("Calling 'get_scored_article_hashes'")

    return list(Article.objects.filter(score__gte=0).values_list('hash', flat=True))

@shared_task
def fetch_feed(url, cutoff_time, scored_hashes):
    """Fetch a single feed and process it."""
    logger.info(f"Calling 'fetch_feed' on url: {url}")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        feed_data = response.text
        # Process the feed data immediately after fetching
        process_and_store_articles(feed_data, cutoff_time, scored_hashes)
    except requests.RequestException as e:
        logger.error(f"Error fetching {url}: {e}")

def process_and_store_articles(feed_data, cutoff_time, scored_hashes):
    """Process and store articles from a single feed result."""
    logger.info("Calling 'process_and_store_articles'")

    # Process the feed data (assuming feed_data is not a list of results but a single feed's result)
    articles = process_feed(feed_data, cutoff_time, scored_hashes)
    
    # Flatten the list if necessary and insert articles to the database
    if articles:
        insert_articles_to_db.apply_async(args=[articles], priority=2)

def process_feed(feed_data, cutoff_time, scored_hashes):
    """Process a single feed."""
    logger.info("Calling 'process_feed'")

    feed = feedparser.parse(feed_data)

    return [
        {
            'hash': hashlib.md5(entry.title.encode()).hexdigest(),
            'publication_date': datetime(*entry.published_parsed[:6], tzinfo=timezone.utc),
            'title': entry.title,
            'author': extract_author(entry),
            'link': entry.link,
            'description': entry.get('description', ''),
            'image': extract_first_image_link(entry),
            'source': sanitize_filename(feed.feed.title),
            'source_url': extract_base_url(entry.link),
            'source_image': feed.feed.get('image', {}).get('href', ''),
        }
        for entry in feed.entries
        if 'published' in entry
        and datetime(*entry.published_parsed[:6], tzinfo=timezone.utc) >= cutoff_time
        and hashlib.md5(entry.title.encode()).hexdigest() not in scored_hashes
    ]

def extract_author(entry):
    """Extract the author from an RSS feed entry."""
    authors = []

    # Handle <dc:creator> tags (with or without CDATA)
    dc_creators = entry.get('dc_creator') or []
    if not isinstance(dc_creators, list):
        dc_creators = [dc_creators]
    for creator in dc_creators:
        if isinstance(creator, str):
            authors.append(strip_cdata(creator))

    # Handle <author> tags (with or without CDATA, with or without nested <name> tags)
    author_elements = entry.get('author_detail') or []
    if not isinstance(author_elements, list):
        author_elements = [author_elements]
    for author_element in author_elements:
        if 'name' in author_element and isinstance(author_element['name'], str):
            authors.append(author_element['name'])
        elif isinstance(author_element, str):
            authors.append(strip_cdata(author_element))

    # Handle multiple <author> tags
    if 'authors' in entry:
        for author in entry['authors']:
            if 'name' in author and isinstance(author['name'], str):
                authors.append(strip_cdata(author['name']))

    # Remove duplicates
    unique_authors = set(authors)

    # Join multiple authors with commas and an Oxford comma before the last author
    return join_authors_with_oxford_comma(unique_authors)

def strip_cdata(text):
    """Strip CDATA tags from a string."""
    if not isinstance(text, (str, bytes)):
        return text  # Return the original input if it's not a string or bytes
    cdata_pattern = re.compile(r'<!\[CDATA\[(.*?)\]\]>', re.DOTALL)
    return cdata_pattern.sub(r'\1', text)

def join_authors_with_oxford_comma(authors):
    """Join authors with commas and an Oxford comma before the last author."""
    authors_list = list(filter(None, authors))  # Filter out empty strings
    if len(authors_list) > 2:
        return ', '.join(authors_list[:-1]) + ', and ' + authors_list[-1]
    elif len(authors_list) == 2:
        return ' and '.join(authors_list)
    elif authors_list:
        return authors_list[0]
    return None  # Return None instead of an empty string

def extract_first_image_link(entry):
    """Extract the first image link from an RSS feed entry."""
    # Check for media:content or enclosure tags
    if 'media_content' in entry:
        media_content = entry.get('media_content', [])
        if media_content and 'url' in media_content[0]:
            return media_content[0]['url']
    elif 'enclosures' in entry:
        enclosures = entry.get('enclosures', [])
        if enclosures and 'url' in enclosures[0]:
            return enclosures[0]['url']

    # Check for image links in description or content:encoded
    if 'description' in entry:
        image_url = find_image_url_in_html(entry['description'])
        if image_url:
            return image_url
    if 'content' in entry and 'value' in entry['content']:
        image_url = find_image_url_in_html(entry['content']['value'])
        if image_url:
            return image_url

    return None

def sanitize_filename(filename):
    """Sanitize the filename by removing special characters."""
    logger.info("Calling 'sanitize_filename'")

    return re.sub(r'[\\/*?:"<>|]', "", filename)

def find_image_url_in_html(html_content):
    """Find the first image URL in an HTML string."""
    try:
        # Parse the HTML content
        root = ET.fromstring(f'<root>{html_content}</root>')
        # Find the first img tag and return its src or srcset attribute
        img_tag = root.find('.//img')
        if img_tag is not None:
            # Prefer src attribute, but if not present, look for srcset
            return img_tag.get('src') or img_tag.get('srcset').split(',')[0].split()[0]
    except ET.ParseError:
        # Handle cases where the HTML content is not well-formed
        pass
    return None

def extract_base_url(url):
    """Extract the base URL from a full URL."""
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}/"

@shared_task
def insert_articles_to_db(articles):
    articles_str = '\n'.join(json.dumps(article, indent=2, cls=CustomJSONEncoder) for article in articles)
    logger.info(f"Calling 'insert_articles_to_db' on articles:\n{articles_str}")

    for article_data in articles:
        try:
            with transaction.atomic():
                article, created = Article.objects.get_or_create(
                    hash=article_data['hash'],
                    defaults=article_data
                )
            if created:
                logger.info(f"[insert_articles_to_db] Inserted article with hash: {article_data['hash']}")
                query_openai_api.apply_async(args=[article.title, settings.PROMPT, article.hash], priority=3)
            else:
                logger.error(f"[insert_articles_to_db] Article with hash: {article_data['hash']} already exists in the database, not inserted")
        except IntegrityError as e:
            logger.error(f"[insert_articles_to_db] Error inserting article: {e}")

class CustomJSONEncoder(json.JSONEncoder):
    """JSON Encoder that converts datetime objects to ISO format strings."""
    def default(self, obj):
        if isinstance(obj, datetime):
            # Format datetime object as an ISO string
            return obj.isoformat()
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

# Set the rate limit to 250 requests per minute (250/m)
@shared_task(bind=True, rate_limit=f'{RATE_LIMIT_PER_WORKER}/m')
def query_openai_api(self, title, prompt, article_hash, retry_count=0):
    """Query the OpenAI API with the given text and prompt."""
    logger.info(f"Querying OpenAI API for article: {article_hash}")

    if not hasattr(settings, 'OPENAI_API_KEY'):
        raise ImproperlyConfigured('The OpenAI API key has not been set in the Django settings.')

    headers = {
        'Authorization': f'Bearer {settings.OPENAI_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'gpt-4-1106-preview',
        'messages': [
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': f"{prompt}Title: `{title}` Hash (\"id\"): `{article_hash}`"}
        ],
        'temperature': 0,
    }

    try:
        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data, timeout=30)
        response.raise_for_status()
        response_content = response.json()
        rankings = json.loads(response_content['choices'][0]['message']['content'].strip('`').replace('json\n', '', 1).strip())

        # Check if the 'id' in the response matches the article_hash
        for article_data in rankings.get('articles', []):
            if article_data['id'] != article_hash:
            # If the 'id' does not match, log an error and retry
                logger.error(f"Mismatched hash in response. Expected: {article_hash}, Received: {rankings.get('id')}")
                raise ValueError("Mismatched hash in response")

        process_api_response.apply_async(args=[rankings], priority=4)
        logger.info(f"OpenAI API call successful for article hash: {article_hash}")
        return rankings
    except (requests.exceptions.RequestException, ValueError) as e:
        logger.error(f"OpenAI API request failed or hash mismatch: {e}")
        # Calculate the delay for the exponential backoff
        countdown = min(2 ** retry_count, 3600)  # Cap the delay at 1 hour
        retry_count += 1
        # Retry the task with exponential backoff
        raise self.retry(exc=e, countdown=countdown, max_retries=5, kwargs={'retry_count': retry_count})

@shared_task(bind=True)
def process_api_response(self, rankings):
    """Process the API response and update article scores."""
    logger.info(f"Processing API response for article rankings: {json.dumps(rankings, indent=4)}")

    # Iterate over the list of articles in the rankings dictionary
    for article_data in rankings.get('articles', []):
        article_hash = article_data.get('id')
        article_score = article_data.get('score')

        # Update the article score in the database
        try:
            with transaction.atomic():
                article = Article.objects.get(hash=article_hash)
                article.score = article_score
                article.save()
                logger.info(f"[process_api_response] Updated score for article with hash: {article_hash}")
        except KeyError:
            logger.error(f"[process_api_response] Invalid article data format: {article_data}")
        except Exception as e:
            logger.error(f"[process_api_response] Error updating article with hash {article_hash}: {e}")
            try:
                # Retry the task with a delay
                raise self.retry(exc=e, countdown=30, max_retries=3)
            except MaxRetriesExceededError:
                logger.error(f"[process_api_response] Max retries exceeded for article with hash {article_hash}")