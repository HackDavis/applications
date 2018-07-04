from flask import Flask
from dotenv import load_dotenv
import os
import src.controller.routes

load_dotenv()

app = Flask(__name__)


