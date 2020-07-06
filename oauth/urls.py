from django.urls import path, include

from oauth.views import oauth_login, authorize, EmailCheckRequiredView

app_name = "Oauth"
urlpatterns = [
    # path(r"authorize/",)
    path(r"login/",oauth_login,name="login"),
    path(r"authorize/",authorize,name="authorize"),
    path(r"bindEmail/<int:oauthid>",EmailCheckRequiredView.as_view(),name="bindEmail")
]