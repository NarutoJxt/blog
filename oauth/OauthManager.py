import json
from urllib import parse
import requests
from abc import ABCMeta, abstractmethod

from django.core.exceptions import ObjectDoesNotExist

from oauth.models import OauthConfig, OauthUser


class BaseOauthManager(metaclass=ABCMeta):
    AUTH_URL = ""
    TOKEN_URL = ""
    ARI_URL = ""
    ICON_NAME = ""
    def __init__(self,access_token,openid):
        self.access_token = access_token
        self.openid = openid
    @property
    def is_access_token(self):

        return self.access_token is not None
    @property
    def is_authorize(self):
        return self.access_token is not None and self.openid is not None
    @abstractmethod
    def get_authorize_url(self,redirect_url = "/"):
        pass
    @abstractmethod
    def get_access_token_by_code(self,code):
        pass
    @abstractmethod
    def get_auth_info(self):
        pass
    def do_get(self,url,param):
        res = requests.get(url=url,params=param)
        return res.text
    def do_post(self,url,param,headers=None):
        if headers:
            res = requests.post(url,param,headers=headers)
        else:
            res = requests.post(url,param)
        return res.text
    def get_config(self):
        value = OauthConfig.objects.filter(type=self.ICON_NAME)
        return value[0] if value else None
class GitHubManager(BaseOauthManager):

    AUTH_URL = 'https://github.com/login/oauth/authorize'
    TOKEN_URL = 'https://github.com/login/oauth/access_token'
    API_URL = 'https://api.github.com/user'
    ICON_NAME = 'github'
    def __init__(self,access_token=None,openid=None):
        config = self.get_config()

        self.client_id = config.app_key if config.app_key else ""
        self.client_secret = config.app_secret if config.app_secret else ""
        self.callback_url = config.callBack_url if config.callBack_url else ""
        super(GitHubManager,self).__init__(access_token=access_token,openid=openid)
    def get_authorize_url(self,next_url = "/"):
        param = {
            "response_type=":"code",
            "client_id":self.client_id,
            'scope': 'user',
            "redirect_uri":self.callback_url,
            "type":"github"
        }
        url = self.AUTH_URL + "?"+parse.urlencode(param)
        return url
    def get_access_token_by_code(self,code):
        param = {
            "client_id":self.client_id,
            "client_secret":self.client_secret,
            "code":code,
            "grant_type":"authorization_code",
            "redirect_ur":self.callback_url
        }
        res = self.do_post(self.TOKEN_URL,param)
        try:
            r = parse.parse_qs(res)
            self.access_token =r["access_token"][0]
            return self.access_token
        except:
            return None
    def get_auth_info(self):
        param = {
            "access_token":self.access_token
        }
        headers = {
            "Authorization":"token OAUTH-TOKEN"
        }
        res = self.do_get(url=self.API_URL,param=param)
        data = json.loads(res)
        is_exist = False
        try:
            user = OauthUser.objects.get(openid=data["node_id"],user_type=self.ICON_NAME.lower())
        except ObjectDoesNotExist as e:
            user = OauthUser()
            user.nickname = data["login"]
            user.picture = data["avatar_url"]
            user.user_type = "github"
            user.openid = data["node_id"]
            user.tocken = self.access_token
            if "email" in data and data["email"]:
                user.email = data["email"]
        else:
            is_exist = True
        return user,is_exist
class GoogleManager(BaseOauthManager):
    AUTH_URL = 'https://accounts.google.com/o/oauth2/auth'
    TOKEN_URL = 'https://accounts.google.com/o/oauth2/token'
    API_URL = "https://www.googleapis.com/oauth2/v3/userinfo"
    ICON_NAME = 'google'
    def __init__(self,access_token=None,openid=None):
        config = self.get_config()
        self.client_id = config.app_key if config.app_key else ""
        self.client_secret = config.app_secret if config.app_secret else ""
        self.callback_url = config.callBack_url if config.callBack_url else ""
        super(GoogleManager,self).__init__(access_token=access_token,openid=openid)
    def get_authorize_url(self,redirect_url = "/"):
        param = {
            "response_type":"code",
            "scope":"profile",
            "client_id":self.client_id,
            "redirect_uri":self.callback_url,
            "type":"google"
        }
        url = self.AUTH_URL + "?"+parse.urlencode(param)
        return url
    def get_auth_info(self):
        param = {
            "access_token": self.access_token
        }
        headers = {
            "Authorization": "token OAUTH-TOKEN"
        }
        res = self.do_get(url=self.API_URL, param=param)
        data = json.loads(res)
        is_exist = False
        try:
            user = OauthUser.objects.get(openid=data["sub"],user_type=self.ICON_NAME.lower())
        except ObjectDoesNotExist as e:
                user = OauthUser()
                user.nickname = data["name"]
                user.picture = data["picture"]
                user.user_type = "google"
                user.openid = data["sub"]
                user.tocken = self.access_token
                if "email" in data and data["email"]:
                    user.email = data["email"]
        else:
            is_exist = True
        return user,is_exist

    def get_access_token_by_code(self,code):
        param = {
            "client_id":self.client_id,
            "client_secret":self.client_secret,
            "code":code,
            "grant_type":"authorization_code",
            "redirect_uri":self.callback_url,
        }

        res = self.do_post(self.TOKEN_URL, param)
        res = json.loads(res)
        self.access_token =res["access_token"]
        return self.access_token
