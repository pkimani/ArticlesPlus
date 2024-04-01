# rssapp/serializers.py
from rest_framework import serializers
from .models import Article
import pytz

class ArticleSerializer(serializers.ModelSerializer):
    local_publication_date = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = '__all__'  # Include the new field

    def get_local_publication_date(self, obj):
        # Get the user's timezone from the context, default to UTC if not provided
        request = self.context.get('request', None)
        client_timezone = request.query_params.get('timezone', 'UTC') if request else 'UTC'
        tz = pytz.timezone(client_timezone)

        # Convert the publication_date to the user's local timezone
        local_pub_date = obj.publication_date.astimezone(tz)
        return local_pub_date.isoformat()