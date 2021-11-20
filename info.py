import re
from os import environ
id_pattern = re.compile(r'^.\d+$')
 
 # ForceSub Channel Id
    AUTH_CHANNEL = os.environ.get("AUTH_CHANNEL", "")
