#----------------------------------- https://github.com/m4mallu/gofilesbot --------------------------------------------#

import os
import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            "gofilesbot.txt",
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

class Config(object):

    # Get a bot token from botfather
    TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")

    # Get from my.telegram.org
    APP_ID = int(os.environ.get("APP_ID", ""))
    
    # Welcome Photo
    PICS = os.environ.get("PICS", "https://telegra.ph/file/7e56d907542396289fee4.jpg https://telegra.ph/file/9aa8dd372f4739fe02d85.jpg https://telegra.ph/file/adffc5ce502f5578e2806.jpg https://telegra.ph/file/6937b60bc2617597b92fd.jpg https://telegra.ph/file/09a7abaab340143f9c7e7.jpg https://telegra.ph/file/5a82c4a59bd04d415af1c.jpg https://telegra.ph/file/323986d3bd9c4c1b3cb26.jpg https://telegra.ph/file/b8a82dcb89fb296f92ca0.jpg https://telegra.ph/file/31adab039a85ed88e22b0.jpg https://telegra.ph/file/c0e0f4c3ed53ac8438f34.jpg https://telegra.ph/file/eede835fb3c37e07c9cee.jpg https://telegra.ph/file/e17d2d068f71a9867d554.jpg https://telegra.ph/file/8fb1ae7d995e8735a7c25.jpg https://telegra.ph/file/8fed19586b4aa019ec215.jpg https://telegra.ph/file/8e6c923abd6139083e1de.jpg https://telegra.ph/file/0049d801d29e83d68b001.jpg").split()
    
    # Get from my.telegram.org
    API_HASH = os.environ.get("API_HASH", "")

    # Generate a user session string
    TG_USER_SESSION = os.environ.get("TG_USER_SESSION", "")

    # ID of Channels from which the bot should search files
    CHANNELS = set(int(x) for x in os.environ.get("CHANNELS", "").split())
    
    # ID of Channel from which the bot should Send files
    CHAT = os.environ.get("CHAT", "-1001567765831")

    # Authorized users to perform delete messages in group
    AUTH_USERS = set(int(x) for x in os.environ.get("AUTH_USERS", "").split())
    
    # ForceSub Channel Id
    AUTH_CHANNEL = os.environ.get("AUTH_CHANNEL", "")


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
