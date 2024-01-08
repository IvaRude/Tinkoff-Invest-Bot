import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

TINKOFF_TOKEN = os.environ.get("TINKOFF_INVEST_TOKEN")
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_BOT_OWNER = os.environ.get('TELEGRAM_BOT_OWNER')
NUM_OF_WORKS_FOR_WORKER = 20