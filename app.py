from flask import Flask
from dotenv import load_dotenv
from review.routes import review_blueprint
import os
import src.controller.routes

load_dotenv()

app = Flask(__name__)
app.register_blueprint(review_blueprint)