import os
from dotenv import load_dotenv

load_dotenv()
TG_TOKEN = os.getenv("TG_TOKEN")
TG_API_URL = "https://telegg.ru/orig/bot"  # proxy url
