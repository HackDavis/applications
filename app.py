from dotenv import load_dotenv
from flask import Flask

from src.shared import Shared

load_dotenv()

app = Flask(__name__)
app.config.from_object('src.lib.config.Config')
app.secret_key = app.config['SECRET_KEY']

Shared.instantiate(app)

from src.controller.review import review
from src.controller.static_files import static_files

app.register_blueprint(review)
app.register_blueprint(static_files)
