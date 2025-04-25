from django.urls import re_path

from . import consumers
 
websocket_urlpatterns = [
    re_path(r"ws/bots/(?P<bot_id>bot_[a-zA-Z0-9]+)/transcript/$", consumers.TranscriptConsumer.as_asgi()),
] 