import os
from dotenv import load_dotenv

load_dotenv()

WEB_PASS_AUTH = os.getenv('WEB_PASS_AUTH')
WEB_USER_AUTH = os.getenv('WEB_USER_AUTH')