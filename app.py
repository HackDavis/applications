from flask import Flask
from dotenv import load_dotenv
import os

from src.controller.review import review
from src.controller.static_files import static_files

load_dotenv()

app = Flask(__name__)
app.register_blueprint(review)
app.register_blueprint(static_files)
