import os
from dotenv import load_dotenv

load_dotenv()

WEB_URL = os.getenv('WEB_URL')
WEB_AUTH = os.getenv('WEB_AUTH')