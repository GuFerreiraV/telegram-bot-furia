// DOM elements
const messageForm = document.getElementById('message-form');
const messageInput = document.getElementById('message-input');
const chatContainer = document.getElementById('chat-container');
const typingIndicator = document.getElementById('typing-indicator');
const connectionStatus = document.getElementById('connection-status');

// State variables
let isConnected = true;
let typingTimeout = null;

// Initialize the chat interface
document.addEventListener('DOMContentLoaded', function() {
    // Load message history
    loadMessages();
    
    // Set up periodic connection check
    setInterval(checkConnection, 10000);
    
    // Scroll to the bottom of chat
    scrollToBottom();
});

// Form submission for sending messages
messageForm.addEventListener('submit', function(event) {
    event.preventDefault();
    
    const message = messageInput.value.trim();
    if (!message) return;
    
    // Clear input
    messageInput.value = '';
    
    // Send message to server
    sendMessage(message);
});

/**
 * Load message history from server
 */
async function loadMessages() {
    try {
        const response = await fetch('/api/messages');
        if (!response.ok) throw new Error('Failed to fetch messages');
        
        const messages = await response.json();
        
        // Clear chat container
        chatContainer.innerHTML = '';
        
        // Add messages to chat
        messages.forEach(message => {
            addMessageToChat(message.text, message.sender, message.timestamp);
        });
        
        // Scroll to bottom
        scrollToBottom();
        
        updateConnectionStatus(true);
    } catch (error) {
        console.error('Error loading messages:', error);
        updateConnectionStatus(false);
    }
}

/**
 * Send a message to the server
 * @param {string} message - The message text to send
 */
async function sendMessage(message) {
    try {
        // Add user message to chat immediately
        const now = new Date();
        const timestamp = now.getHours().toString().padStart(2, '0') + ':' + 
                         now.getMinutes().toString().padStart(2, '0');
        
        addMessageToChat(message, 'user', timestamp);
        scrollToBottom();
        
        // Show typing indicator
        showTypingIndicator();
        
        // Send message to server
        const response = await fetch('/api/send', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message }),
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to send message');
        }
        
        // Hide typing indicator and reload messages
        hideTypingIndicator();
        loadMessages();
        updateConnectionStatus(true);
    } catch (error) {
        console.error('Error sending message:', error);
        hideTypingIndicator();
        
        // Show error message
        addMessageToChat(
            'Sorry, there was an error sending your message. Please try again later.', 
            'bot', 
            getCurrentTimestamp()
        );
        
        updateConnectionStatus(false);
        scrollToBottom();
    }
}

/**
 * Add a message to the chat interface
 * @param {string} text - The message text
 * @param {string} sender - 'user' or 'bot'
 * @param {string} timestamp - Time string in format HH:MM
 */
function addMessageToChat(text, sender, timestamp) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', `message-${sender}`);
    
    // Format text with newlines
    const formattedText = text.replace(/\n/g, '<br>');
    
    messageElement.innerHTML = `
        <div class="message-text">${formattedText}</div>
        <div class="message-timestamp">${timestamp}</div>
    `;
    
    chatContainer.appendChild(messageElement);
}

/**
 * Show the typing indicator
 */
function showTypingIndicator() {
    typingIndicator.classList.remove('d-none');
    scrollToBottom();
    
    // Clear any existing timeout
    if (typingTimeout) {
        clearTimeout(typingTimeout);
    }
    
    // Set a timeout to hide the indicator after 30 seconds
    // (in case the server doesn't respond)
    typingTimeout = setTimeout(() => {
        hideTypingIndicator();
    }, 30000);
}

/**
 * Hide the typing indicator
 */
function hideTypingIndicator() {
    typingIndicator.classList.add('d-none');
    
    // Clear any existing timeout
    if (typingTimeout) {
        clearTimeout(typingTimeout);
        typingTimeout = null;
    }
}

/**
 * Get the current timestamp in HH:MM format
 * @returns {string} Formatted timestamp
 */
function getCurrentTimestamp() {
    const now = new Date();
    return now.getHours().toString().padStart(2, '0') + ':' + 
           now.getMinutes().toString().padStart(2, '0');
}

/**
 * Scroll to the bottom of the chat container
 */
function scrollToBottom() {
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

/**
 * Check the connection status with the server
 */
async function checkConnection() {
    try {
        const response = await fetch('/api/typing');
        if (!response.ok) {
            throw new Error('Connection check failed');
        }
        
        updateConnectionStatus(true);
    } catch (error) {
        console.error('Error checking connection:', error);
        updateConnectionStatus(false);
    }
}

/**
 * Update the connection status indicator
 * @param {boolean} connected - Whether the client is connected to the server
 */
function updateConnectionStatus(connected) {
    if (connected) {
        connectionStatus.className = 'badge bg-success';
        connectionStatus.innerHTML = '<i class="fas fa-circle"></i> Connected';
        isConnected = true;
    } else {
        connectionStatus.className = 'badge bg-danger';
        connectionStatus.innerHTML = '<i class="fas fa-exclamation-circle"></i> Disconnected';
        isConnected = false;
    }
}
