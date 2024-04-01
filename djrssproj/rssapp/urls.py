# rssapp/urls.py
from django.urls import path
from .views import ArticleListView, SourceListView, ScoreRangeView, SourceCountView, DateRangeView

urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='article-list'),
    path('sources/', SourceListView.as_view(), name='source-list'),
    path('score-range/', ScoreRangeView.as_view(), name='score-range'),
    path('date-range/', DateRangeView.as_view(), name='date-range'),
    path('source-counts/', SourceCountView.as_view(), name='source-counts'),
]