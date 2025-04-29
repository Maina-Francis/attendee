from django.urls import re_path

from . import consumers
 
websocket_urlpatterns = [
    # Make the pattern more permissive for testing
    re_path(r"ws/bots/(?P<bot_id>.*)/transcript/$", consumers.TranscriptConsumer.as_asgi()),
] 