import json
import logging
from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token

from .models import Bot, Recording, Utterance
from .serializers import TranscriptUtteranceSerializer

logger = logging.getLogger(__name__)


class TranscriptConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.bot_id = self.scope["url_route"]["kwargs"]["bot_id"]
        self.transcript_group_name = f"transcript_{self.bot_id}"
        
        # Authentication disabled for testing
        # Add the connection to the transcript group
        await self.channel_layer.group_add(self.transcript_group_name, self.channel_name)
        
        # Accept the connection
        await self.accept()
        
        # Send existing transcript data on connection
        await self.send_initial_transcript()

    async def disconnect(self, close_code):
        # Remove the connection from the transcript group
        await self.channel_layer.group_discard(self.transcript_group_name, self.channel_name)

    async def receive(self, text_data):
        # We don't expect to receive messages from clients for transcript streaming
        pass

    async def transcript_message(self, event):
        # Forward the transcript message to the client
        await self.send(text_data=json.dumps(event["message"]))

    @database_sync_to_async
    def authenticate(self, token_key, bot_id):
        try:
            token = Token.objects.select_related("user").get(key=token_key)
            bot = Bot.objects.get(object_id=bot_id)
            
            # Check if the token's project matches the bot's project
            return bot.project == token.user.api_key.project
        except (Token.DoesNotExist, Bot.DoesNotExist, ObjectDoesNotExist, AttributeError):
            return False

    @database_sync_to_async
    def get_initial_transcript(self, bot_id):
        try:
            bot = Bot.objects.get(object_id=bot_id)
            recording = Recording.objects.filter(bot=bot, is_default_recording=True).first()
            
            if not recording:
                return []
            
            # Get all utterances with transcriptions, sorted by timeline
            utterances = Utterance.objects.select_related("participant").filter(
                recording=recording, 
                transcription__isnull=False
            ).order_by("timestamp_ms")
            
            # Format the response, skipping empty transcriptions
            transcript_data = [
                {
                    "speaker_name": utterance.participant.full_name,
                    "speaker_uuid": utterance.participant.uuid,
                    "speaker_user_uuid": utterance.participant.user_uuid,
                    "timestamp_ms": utterance.timestamp_ms,
                    "duration_ms": utterance.duration_ms,
                    "transcription": utterance.transcription,
                }
                for utterance in utterances
                if utterance.transcription.get("transcript", "")
            ]
            
            return TranscriptUtteranceSerializer(transcript_data, many=True).data
        except Bot.DoesNotExist:
            return []

    async def send_initial_transcript(self):
        transcript_data = await self.get_initial_transcript(self.bot_id)
        await self.send(text_data=json.dumps({
            "type": "initial_transcript",
            "utterances": transcript_data
        })) 