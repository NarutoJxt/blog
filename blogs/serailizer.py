from django.core import serializers


from rest_framework import serializers
class ArticlSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(min_length=3,max_length=20)
    body = serializers.CharField()
    thumb_up = serializers.IntegerField()
    collection_counts = serializers.IntegerField()
    comment_counts = serializers.IntegerField()