from dotenv import load_dotenv
import os
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./deals.db")
SCRAPE_INTERVAL_SECONDS = int(os.getenv("SCRAPE_INTERVAL_SECONDS", 300))
DISCOUNT_THRESHOLD = float(os.getenv("DISCOUNT_THRESHOLD", 50.0))
