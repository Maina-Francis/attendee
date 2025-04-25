// Example of using the WebSocket transcript streaming endpoint
// Replace with your actual bot ID and API key
const BOT_ID = 'bot_xxxxxxxxxxx';
const API_KEY = 'your_api_key_here';

const socket = new WebSocket(`wss://app.attendee.dev/ws/bots/${BOT_ID}/transcript/?token=${API_KEY}`);

// Handle connection open
socket.addEventListener('open', event => {
    console.log('WebSocket connection established');
});

// Handle messages
socket.addEventListener('message', event => {
    const data = JSON.parse(event.data);
    
    if (data.type === 'initial_transcript') {
        // Handle initial transcript data
        console.log('Initial transcript received:', data.utterances.length, 'utterances');
        
        // Process each utterance in the initial transcript
        data.utterances.forEach(utterance => {
            displayUtterance(utterance);
        });
    } 
    else if (data.type === 'new_utterance') {
        // Handle new utterance that came in real-time
        console.log('New utterance received:', data.utterance);
        displayUtterance(data.utterance);
    }
});

// Handle errors
socket.addEventListener('error', event => {
    console.error('WebSocket error:', event);
});

// Handle connection close
socket.addEventListener('close', event => {
    console.log('WebSocket connection closed with code:', event.code);
    
    // You might want to implement reconnection logic here
    if (event.code === 4003) {
        console.error('Authentication failed. Check your API key.');
    }
});

// Example function to display an utterance in the UI
function displayUtterance(utterance) {
    // Example implementation - replace with your actual UI logic
    const transcriptContainer = document.getElementById('transcript-container');
    
    const utteranceElement = document.createElement('div');
    utteranceElement.className = 'utterance';
    
    const speakerElement = document.createElement('div');
    speakerElement.className = 'speaker';
    speakerElement.textContent = utterance.speaker_name || 'Unknown Speaker';
    
    const textElement = document.createElement('div');
    textElement.className = 'text';
    textElement.textContent = utterance.transcription.transcript;
    
    utteranceElement.appendChild(speakerElement);
    utteranceElement.appendChild(textElement);
    
    transcriptContainer.appendChild(utteranceElement);
    
    // Auto-scroll to the bottom
    transcriptContainer.scrollTop = transcriptContainer.scrollHeight;
}

// Example of how to close the connection when done
function closeConnection() {
    socket.close();
}

// Example of how to reconnect if needed
function reconnect() {
    if (socket.readyState === WebSocket.CLOSED) {
        socket = new WebSocket(`wss://app.attendee.dev/ws/bots/${BOT_ID}/transcript/?token=${API_KEY}`);
        // Re-add all event listeners
    }
} 