# rssapp/models.py
from django.db import models

class Article(models.Model):
    hash = models.CharField(max_length=32, unique=True)
    publication_date = models.DateTimeField()
    title = models.TextField()
    link = models.TextField()
    source = models.TextField()
    score = models.IntegerField(null=True, blank=True, default=None)
    author = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    source_url = models.TextField(blank=True, null=True)
    source_image = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'articles'
        indexes = [
            models.Index(fields=['score', 'publication_date', 'id'], name='score_pubdate_id_idx'),
            models.Index(fields=['publication_date', 'id'], name='pubdate_id_idx'),
        ]