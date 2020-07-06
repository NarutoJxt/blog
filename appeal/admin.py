from django.contrib import admin

# Register your models here.
from appeal.models import AppealArticleModel


@admin.register(AppealArticleModel)
class AppealArticleAdmin(admin.ModelAdmin):
    list_display = ["appeal_options","appealed_article","appeal_body"]
    list_select_related = ["appealed_article"]
    list_filter = ["appeal_options"]
    search_fields = ["appeal_article"]

