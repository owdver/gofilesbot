import re
from os import environ
id_pattern = re.compile(r'^.\d+$')


ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('AUTH_USERS', '').split()]
auth_channel = environ.get('AUTH_CHANNEL')
CHANNEL_USERNAME = environ.get('CHANNEL_USERNAME')
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else auth_channel
