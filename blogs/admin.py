from django.contrib import admin

# Register your models here.
from blogs.models import Artical


@admin.register(Artical)
class ArticalAdmin(admin.ModelAdmin):
    list_display = ["id","title","body","pub_time","status","views","author"]
    list_display_links = ["id","title"]
    list_filter = ["author","status"]
    fields =  ["title","body","pub_time","status","views","author"]
    show_full_result_count = True
    search_fields = ["title","status"]
    date_hierarchy = "pub_time"
