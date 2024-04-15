import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TG_TOKEN')
FOLDER_ID = os.getenv('FOLDERID')

IAMTOKEN = ''

MAX_TTS_SYMBOLS = 200
MAX_USER_TTS_SYMBOLS = 1000
