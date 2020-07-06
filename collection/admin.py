from django.contrib import admin

# Register your models here.
from collection.models import Collection


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["blog_user","collected_article","collected_time"]
    list_display_links = ["collected_article"]
    list_select_related = ["collected_article"]
    date_hierarchy = "collected_time"
