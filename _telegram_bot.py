import os
import logging
import requests
import time
from bs4 import BeautifulSoup
from telegram.ext import Updater
from dotenv import load_dotenv

load_dotenv()
# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN") or "your_fallback_token_here"

def start_polling():
    updater = Updater(BOT_TOKEN)
    updater.start_polling()
    updater.idle()

def send_message_to_telegram(message_text):
    logger.debug(f"Sending message to Telegram bot: {message_text}")
    
    try:
        time.sleep(1)
        
        if message_text.startswith('/'):
            command = message_text[1:].lower()  
            
            if command == "start":
                return "Olá, furioso! Eu sou o FURIA Bot. Posso te ajudar com:\n" \
                       "/jogadores - Elenco atual\n" \
                       "/jogos - Partidas recentes\n" \
                       "/proximos-camps - Próximos campeonatos\n" \
                            
            elif command == "jogadores":
                return get_furia_players()
            
            elif command == "jogos":
                return get_recent_matches()
            
            elif command == "proximos-camps": 
                return get_upcoming_tournaments()
                        
            else:
                return "Comando não reconhecido. Use /start para ver os comandos disponíveis."
        
        message_lower = message_text.lower()
        
        if "ola" in message_lower or "olá" in message_lower or "hello" in message_lower or "hi" in message_lower:
            return "Olá, furioso! Como posso ajudar? Use /start para ver os comandos disponíveis."
        
        elif any(word in message_lower for word in["jogadores", "elenco", "time", "players", "roster"]):
            return get_furia_players()
        
        elif any(word in message_lower for word in ["jogo", "partida", "match"]):
            return get_recent_matches()
        
        elif any(word in message_lower for word in ["proximos", "próximos", "campeonatos", "torneios"]):
            return get_upcoming_tournaments()
               
        else:
            return "Desculpe, não entendi. Use /start para ver os comandos disponíveis."
    
    except Exception as e:
        logger.error(f"Error in send_message_to_telegram: {str(e)}")
        return f"Estou com problemas para processar sua solicitação. Erro: {str(e)}"

def get_telegram_updates():
    logger.debug("Getting updates from Telegram bot")
    
    try:
    
        return []
    
    except Exception as e:
        logger.error(f"Error in get_telegram_updates: {str(e)}")
        return []




def get_upcoming_tournaments():
    return """🗓️ PRÓXIMOS CAMPEONATOS DA FURIA:

⏰ EM 12 DIAS
🏆 PGL Astana 2025
📅 10/05/25 à 18/05/25

⏰ EM 21 DIAS
🏆 IEM Dallas 2025
📅 19/05/25 à 25/05/25
🏷️ EXITREME MASTERS @ESL

⏰ EM 36 DIAS
🏆 BLAST.tv Austin Major 2025
📅 03/06/25 à 22/06/25
🏷️ BLAST.TV – AUSTIN.TV
"""
def get_furia_players():
    return """🎮 Elenco Atual da FURIA CS2 (2024):
    
🔫 Jogadores Ativos:
- KSCERATO (Kaike Cerato)
- yuurih (Yuri Boian)
- molodoy (Danil Golubenko)
- FalleN (Gabriel Toledo)
- YEKINDAR (Mareks Gaļinskis)

👔 Staff:
- sidde (Sidnei Macedo) (Coach)

⏸️ Reservas:
- skullz (Felipe Medeiros)
- chelo (Marcelo Cespedes)

🏆 Ex-jogadores:
- arT (Andrei Piovezan)
- guerri (Nicholas Nogueira)

📢 Use /jogos para ver os jogos recentes!"""
def get_recent_matches():  
    return """📅 Últimos 10 Jogos da FURIA (CS2):

🏆 PGL Bucharest 2025:
• 09/04 - FURIA 0 : 2 vs MongolZ
• 08/04 - FURIA 0 : 2 vs Virtus.pro
• 07/04 - FURIA 1 : 2 vs Complexity
• 06/04 - FURIA 2 : 0 vs Apogee

💥 BLAST Open Spring 2025:
• 22/03 - FURIA 1 : 2 vs M80
• 20/03 - FURIA 0 : 2 vs Natus Vincere

🏆 ESL Pro League S21:
• 10/03 - FURIA 1 : 2 vs Falcons
• 09/03 - FURIA 2 : 1 vs MIBR
• 08/03 - FURIA 0 : 2 vs Liquid
• 07/03 - FURIA 1 : 2 vs MOUZ
"""