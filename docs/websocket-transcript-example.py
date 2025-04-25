#!/usr/bin/env python3
"""
Example Python client for the WebSocket transcript streaming endpoint.
Requires websockets package: pip install websockets
"""

import asyncio
import json
import websockets

# Replace with your actual bot ID and API key
BOT_ID = 'bot_xxxxxxxxxxx'
API_KEY = 'your_api_key_here'
BASE_URL = 'wss://app.attendee.dev'

async def connect_to_transcript_websocket():
    """Connect to the transcript WebSocket endpoint and handle messages."""
    url = f"{BASE_URL}/ws/bots/{BOT_ID}/transcript/?token={API_KEY}"
    
    try:
        async with websockets.connect(url) as websocket:
            print("WebSocket connection established")
            
            while True:
                # Wait for messages
                message = await websocket.recv()
                data = json.loads(message)
                
                if data.get("type") == "initial_transcript":
                    # Handle initial transcript data
                    utterances = data.get("utterances", [])
                    print(f"Initial transcript received: {len(utterances)} utterances")
                    
                    # Process each utterance in the initial transcript
                    for utterance in utterances:
                        display_utterance(utterance)
                
                elif data.get("type") == "new_utterance":
                    # Handle new utterance that came in real-time
                    utterance = data.get("utterance")
                    print(f"New utterance received from {utterance.get('speaker_name')}")
                    display_utterance(utterance)
    
    except websockets.exceptions.InvalidStatusCode as e:
        if e.status_code == 4003:
            print("Authentication failed. Check your API key.")
        else:
            print(f"Connection failed with status code: {e.status_code}")
    
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Connection closed with code: {e.code}, reason: {e.reason}")
    
    except Exception as e:
        print(f"Error: {e}")

def display_utterance(utterance):
    """Display an utterance in the console."""
    speaker = utterance.get("speaker_name", "Unknown Speaker")
    text = utterance.get("transcription", {}).get("transcript", "")
    timestamp_ms = utterance.get("timestamp_ms", 0)
    
    # Convert timestamp to seconds
    timestamp_sec = timestamp_ms / 1000
    minutes = int(timestamp_sec // 60)
    seconds = int(timestamp_sec % 60)
    timestamp_formatted = f"{minutes:02}:{seconds:02}"
    
    print(f"[{timestamp_formatted}] {speaker}: {text}")

if __name__ == "__main__":
    asyncio.run(connect_to_transcript_websocket()) 