from dotenv import load_dotenv
import requests
import os

load_dotenv()

LASTFM_KEY = os.getenv(key="LASTFM_API_KEY")