from flask import Flask
from dotenv import load_dotenv
from src.review.routes import review_blueprint
import os

load_dotenv()

app = Flask(__name__)
app.register_blueprint(review_blueprint)