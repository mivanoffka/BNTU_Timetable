import os
from pathlib import Path

TOKEN = os.environ.get('TOKEN')
LOG_TO_CONSOLE = bool(os.environ.get('LOG_TO_CONSOLE'))
TABLE_NAME = 'groups'
BASE_DIR = Path(__file__).parent
ADMIN_ID = "640091837"