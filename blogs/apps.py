from django.apps import AppConfig


class MainblogConfig(AppConfig):
    name = 'blogs'
def ready():
    import signal
