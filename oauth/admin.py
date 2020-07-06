from django.contrib import admin

# Register your models here.
from oauth.models import OauthUser, OauthConfig


@admin.register(OauthUser)
class OauthUserAdmin(admin.ModelAdmin):
    # fields = ["user","openid","user_type"]
    list_display = ["nickname","user","openid","user_type","email","create_time","last_mod_time","user_type"]
    list_display_links = ["nickname","user","email"]
    list_filter = ["user","user_type"]
    list_per_page = 20
    ordering = ["-nickname"]
    search_fields = ["nickname","user_type"]
@admin.register(OauthConfig)
class OauthConfigAdmin(admin.ModelAdmin):
    list_display = ["type","app_key","app_secret","callBack_url","create_time","last_mod_time"]
    list_display_links = ["app_key","app_secret","callBack_url","create_time","last_mod_time"]
    list_filter = ["app_key"]
    list_per_page = 20
    ordering = ["app_key"]
