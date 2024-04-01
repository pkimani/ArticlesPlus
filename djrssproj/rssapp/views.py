# rssapp/views.py
from django.db.models import Count, Min, Max, Q
from django.db.models.functions import Lower
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Article
from .serializers import ArticleSerializer
from .pagination import ArticleCursorPagination
from django.utils import timezone
from datetime import datetime
import pytz
from django.http import JsonResponse
from .tasks import download_rss_feeds, query_openai_api
from django.conf import settings

class ArticleListView(ListAPIView):
    serializer_class = ArticleSerializer
    pagination_class = ArticleCursorPagination

    def get_queryset(self):
        # Get timezone from the request, default to UTC if not provided
        client_timezone = self.request.query_params.get('timezone', 'UTC')
        tz = pytz.timezone(client_timezone)

        # Get date range from the request
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        # Convert dates to datetime objects in the client's timezone
        if start_date:
            start_date = tz.localize(datetime.strptime(start_date, '%Y-%m-%d'))
            # Convert to UTC
            start_date = start_date.astimezone(pytz.utc)
        if end_date:
            end_date = tz.localize(datetime.strptime(end_date, '%Y-%m-%d'))
            # Set to the end of the day before converting to UTC
            end_date = (end_date + timezone.timedelta(days=1, seconds=-1)).astimezone(pytz.utc)

        q_objects = Q(score__isnull=False)
        if source_filter := self.request.query_params.get('source'):
            q_objects &= Q(source__in=source_filter.split(','))
        if min_score := self.request.query_params.get('min_score'):
            q_objects &= Q(score__gte=min_score)
        if max_score := self.request.query_params.get('max_score'):
            q_objects &= Q(score__lte=max_score)

        # Filter by date range if provided
        if start_date:
            q_objects &= Q(publication_date__gte=start_date)
        if end_date:
            q_objects &= Q(publication_date__lt=end_date)

        # Determine the sort order
        sort_by = self.request.query_params.get('s', 'date')
        if sort_by == 'score':
            order_fields = ['-score', '-publication_date', '-id']
        else:
            order_fields = ['-publication_date', '-id']

        return Article.objects.filter(q_objects).order_by(*order_fields)
    
    def get_serializer_context(self):
        # Override the method to add the request to the serializer context
        return {'request': self.request}

class SourceListView(APIView):
    def get(self, request, *args, **kwargs):
        sources = Article.objects.values('source').annotate(count=Count('source')).order_by(Lower('source'))
        return Response({'sources': sources})

class ScoreRangeView(APIView):
    def get(self, request, *args, **kwargs):
        q_objects = Q(score__isnull=False)
        if source_filter := request.query_params.get('source'):
            q_objects &= Q(source__in=source_filter.split(','))
        score_range = Article.objects.filter(q_objects).aggregate(min_score=Min('score'), max_score=Max('score'))
        return Response(score_range)

class DateRangeView(APIView):
    def get(self, request, *args, **kwargs):
        date_range = Article.objects.aggregate(min_date=Min('publication_date'), max_date=Max('publication_date'))
        return Response(date_range)
    
class SourceCountView(APIView):
    def get(self, request, *args, **kwargs):
        q_objects = Q(score__isnull=False)
        if min_score := request.query_params.get('min_score'):
            q_objects &= Q(score__gte=min_score)
        if max_score := request.query_params.get('max_score'):
            q_objects &= Q(score__lte=max_score)

        total_source_counts = Article.objects.values('source').annotate(total_count=Count('source')).order_by(Lower('source'))
        filtered_source_counts = Article.objects.filter(q_objects).values('source').annotate(filtered_count=Count('source')).order_by(Lower('source'))

        response_data = {
            source['source']: {
                'total_count': source['total_count'],
                'filtered_count': next((filtered['filtered_count'] for filtered in filtered_source_counts if filtered['source'] == source['source']), 0)
            } for source in total_source_counts
        }

        return Response(response_data)

def start_rss_feed_download(request):
    # You might want to add authentication and permissions checks here
    opml_content = open(settings.OPML_FILE_PATH, 'r').read()
    download_rss_feeds.delay(opml_content)  # Assuming you want to start this as a background task
    return JsonResponse({'status': 'started'})

def start_openai_query(request):
    # You might want to add authentication and permissions checks here
    # For demonstration purposes, let's assume you want to query all articles
    # with a null score and you have a function in your tasks.py for this purpose
    articles = Article.objects.filter(score__isnull=True)
    for article in articles:
        # Assuming query_openai_api is a task that takes the article title and hash as arguments
        query_openai_api.delay(article.title, settings.PROMPT, article.hash)
    return JsonResponse({'status': 'queries_started'})