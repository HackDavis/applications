from flask import Flask
from dotenv import load_dotenv
from src.review.routes import review_blueprint
import src.db.models as models
import os

load_dotenv()

models.initialize_user_model()

app = Flask(__name__)
app.register_blueprint(review_blueprint)