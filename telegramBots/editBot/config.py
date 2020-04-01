import logging
from dotenv import load_dotenv
import os
import aiohttp


# Configure logging
logging.basicConfig(level=logging.INFO)

load_dotenv()
TG_TOKEN = os.getenv('USER_BOT_TOKEN')
PROXY_URL = os.getenv('PROXY_URL')
PROXY_LOGIN = os.getenv('PROXY_LOGIN')
PROXY_PASSWORD = os.getenv('PROXY_PASSWORD')
API_HOST = os.getenv('API_HOST')
API_PORT = os.getenv('API_PORT')
WIKI_API = f"http://{API_HOST}:{API_PORT}/api/wiki"
WIKI_API_AUTOSUGGET = f"http://{API_HOST}:{API_PORT}/api/wiki/autosuggest"
SUPPORTED_MEDIA_TYPES = ["photo", "voice", "audio", "video", "document"]

if PROXY_URL != None:
    PROXY_AUTH = aiohttp.BasicAuth(login=PROXY_LOGIN, password=PROXY_PASSWORD)
else:
    PROXY_AUTH = None
logging.info(f"Proxy is set to {PROXY_AUTH}")
logging.info(f"WIKI_API is set to {WIKI_API}")
