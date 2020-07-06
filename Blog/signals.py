from django.core.cache import cache
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver

from account.models import BlogUser, Attention
from blogs.models import Artical


def refresh_cache_signals_save_articles(sender,**kwargs):
    cache_key_list = list(cache.iter_keys("*articles*"))
    for article in cache_key_list:
        cache.delete(article)
def refresh_cache_signals_save_user(sender,**kwargs):
    cache_key_list = list(cache.iter_keys("*user*"))
    for article in cache_key_list:
        cache.delete(article)

def refresh_cache_signals_delete_articles(sender,**kwargs):
    cache_key_list = list(cache.iter_keys("*articles*"))
    for article in cache_key_list:
        cache.delete(article)

def refresh_cache_signals_save_attention(sender,**kwargs):
    cache_key_list = list(cache.iter_keys("*attention*"))
    for follower in cache_key_list:
        cache.delete(follower)
def refresh_cache_signals_delete_attention(sender,**kwargs):
    cache_key_list = list(cache.iter_keys("*attention*"))
    for follow in cache_key_list:
        cache.delete(follow)
