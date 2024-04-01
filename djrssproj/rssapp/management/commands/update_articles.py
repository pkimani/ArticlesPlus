# djrssproj/rssapp/management/commands/update_articles.py
from django.core.management.base import BaseCommand
from django.conf import settings
from rssapp.tasks import query_articles_with_null_score, download_rss_feeds, update_articles_command
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Update articles by downloading RSS feeds and starting the update articles loop.'

    def handle(self, *args, **options):
        # Obtain scores for articles that were not sent to API
        logger.info("Calling query_articles_with_null_score")
        query_articles_with_null_score()

        # Ensure the OpenAI API key is set
        if not hasattr(settings, 'OPENAI_API_KEY'):
            logger.error('The OpenAI API key has not been set in the Django settings.')
            return

        # Read the OPML file content
        logger.info(f"Opening OPML file at {settings.OPML_FILE_PATH}")
        with open(settings.OPML_FILE_PATH, 'rb') as opml_file:
            opml_content = opml_file.read()

        # Call the task to download and process RSS feeds asynchronously
        logger.info("Calling download_rss_feeds asynchronously")
        download_rss_feeds.apply_async(args=[opml_content.decode('utf-8'), 99])

        logger.info("Calling query_openai_api for articles that were not scored")

        # Start the update articles loop
        logger.info("Starting the update articles loop")
        update_articles_command.delay()

        logger.info('Update articles command completed.')