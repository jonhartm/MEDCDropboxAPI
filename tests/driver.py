import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

import medcbox
import json

with open("tests/oauth/auth.json") as f:
    data = json.load(f)
    print(data)

    print(medcbox.Session(data))
