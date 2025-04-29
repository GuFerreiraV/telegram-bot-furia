import os
import logging
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session
from _telegram_bot import send_message_to_telegram
from telegram.ext import Updater


BOT_TOKEN = os.getenv("TELEGRAM_TOKEN") or "your_fallback_token_here"

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")

message_history = {}

@app.route('/')
def index():
    """Render the main chat interface."""
    if 'chat_id' not in session:
        session['chat_id'] = f"user_{datetime.now().timestamp()}"
    
    chat_id = session['chat_id']
    if chat_id not in message_history:
        message_history[chat_id] = []
        
        message_history[chat_id].append({
            "sender": "bot",
            "text": "Olá, furioso! Eu sou o FURIA Bot. Posso te ajudar com:\n/jogadores - Elenco atual\n/jogos - Partidas recentes\n /proximos-camps - Próximos campeonatos",
            "timestamp": datetime.now().strftime("%H:%M")
        })
    
    return render_template('index.html')

@app.route('/api/messages', methods=['GET'])
def get_messages():
    """API endpoint to get message history."""
    chat_id = session.get('chat_id')
    if not chat_id or chat_id not in message_history:
        return jsonify([])
    return jsonify(message_history[chat_id])

@app.route('/api/send', methods=['POST'])
def send_message():
    """API endpoint to send a message to the Telegram bot."""
    data = request.json
    message_text = data.get('message', '').strip()
    chat_id = session.get('chat_id')
    
    if not message_text or not chat_id:
        return jsonify({"success": False, "error": "Invalid message or chat ID"}), 400
    
    user_message = {
        "sender": "user",
        "text": message_text,
        "timestamp": datetime.now().strftime("%H:%M")
    }
    
    if chat_id not in message_history:
        message_history[chat_id] = []
    
    message_history[chat_id].append(user_message)
    
    try:
        bot_response = send_message_to_telegram(message_text)
        
        bot_message = {
            "sender": "bot",
            "text": bot_response,
            "timestamp": datetime.now().strftime("%H:%M")
        }
        message_history[chat_id].append(bot_message)
        
        return jsonify({"success": True})
    except Exception as e:
        logger.error(f"Error sending message to Telegram: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/typing', methods=['GET'])
def get_typing_status():
    """Check if the bot is currently typing (simulated)."""
    return jsonify({"typing": False})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
