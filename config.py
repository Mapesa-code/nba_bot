import os
from dotenv import load_dotenv

# Load variables from .env file (if present)
load_dotenv()
SPORTSDATA_API_KEY = os.getenv("861c2d372b8a409b9db663cb0bc08dbc")
OPENAI_API_KEY = os.getenv("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")
TELEGRAM_BOT_TOKEN = os.getenv("7972586424:AAH7YaQ2c2K8GhD_FThpYku3VjmcX_mZkJI")
REDDIT_API_KEY = os.getenv("yMDHFEMGGDJjcgiFgdOC3G4Ax6um-Q")
YOUTUBE_API_KEY = os.getenv("AIzaSyAbTk3dh42inDAQZ7-OYsWXiMRfLcbCKmM")
