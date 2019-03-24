import os
from pathlib import Path

from poll.management.commands.scrape_loksabha_constituencies import DATA_DIR

BACKGROUND_IMAGE_PATH = Path(DATA_DIR / "tweet-background.png")
FONT_PATH = os.path.join(DATA_DIR, "lato.ttf")
TWEET_IMAGE = Path(os.path.join("/tmp", "tweet.png"))
