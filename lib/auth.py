import os
from dotenv import load_dotenv
from boxsdk import Client, CCGAuth

load_dotenv()

def auth():
    auth = CCGAuth(
        client_id=os.getenv("BOX_CLIENT_ID"),
        client_secret=os.getenv("BOX_CLIENT_SECRET"),
        enterprise_id=os.getenv("BOX_ENTERPRISE_ID"),
    )
    client = Client(auth)
    return client
