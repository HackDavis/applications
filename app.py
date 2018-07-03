from flask import Flask
from dotenv import load_dotenv
import os

from src.review.routes import review_blueprint
from src.controller.routes import routes

load_dotenv()

app = Flask(__name__)
app.register_blueprint(review_blueprint)
app.register_blueprint(routes)

