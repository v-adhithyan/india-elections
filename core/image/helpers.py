from PIL import Image, ImageDraw, ImageFont
from django.utils.encoding import force_bytes

from core.image.constants import FONT_PATH, BACKGROUND_IMAGE_PATH

WHITE_COLOR = (0, 0, 0)
START_X = 50
START_Y = 100
START_COORDINATES = (START_X, START_Y)


def generate_tweet_image(text, image_path):
    if not text:
        raise AttributeError("Param text should not be None")

    text = force_bytes(text)  # prevent unicodedecode error

    if image_path.exists():
        image_path.unlink()

    img = Image.open(BACKGROUND_IMAGE_PATH)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(str(FONT_PATH), 40)
    draw.text(START_COORDINATES, text.decode("utf-8"), WHITE_COLOR, font=font)
    img.save(image_path)
