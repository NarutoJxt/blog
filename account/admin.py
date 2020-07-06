from django.contrib import admin

# Register your models here.
from account.models import BlogUser, Attention


class BlogUserAdmin(admin.ModelAdmin):
    list_display = ["username","signature","email","gender","date_joined"]
    list_display_links = ["username"]
    date_hierarchy = "date_joined"
    ordering = ["-date_joined"]
    show_full_result_count = True
    search_fields = ["username","email","gender"]
    view_on_site = True
class AttentionAdmin(admin.ModelAdmin):
    list_display = ["user","B_follower"]
    list_display_links = ["user"]
    list_select_related = ["B_follower"]



admin.site.register(BlogUser,BlogUserAdmin)
admin.site.register(Attention,AttentionAdmin)