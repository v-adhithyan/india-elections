"""Main module."""
from flask import Flask
from app import constants


def create_app():
    """Use app factory pattern to create app."""
    app = Flask(constants.APP_NAME)
    return app


app = create_app()


@app.route("/")
def hello_world():
    """Getter method for main path."""
    return "India elections 2k19 - visulizations"
