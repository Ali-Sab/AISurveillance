import sqlite3
from datetime import datetime
import logging

formattedTime = datetime.now().strftime('%Y.%m.%d')
logging.basicConfig(filename="logs/http_client_" + formattedTime + ".log", filemode='a', encoding='utf-8', level=logging.DEBUG)