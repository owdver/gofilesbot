import re
from os import environ
id_pattern = re.compile(r'^.\d+$')


auth_channel = environ.get('AUTH_CHANNEL')
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else auth_channel
invite_link = "https://t.me/joinchat/Ur8bdKHGNRdBoeHW"
