from dotenv import load_dotenv
from flask import Flask

from src.shared import Shared

# load environment variables
load_dotenv()

app = Flask(__name__)

# load config
app.config.from_object('src.config.config.Config')
app.secret_key = app.config.get('SECRET_KEY')

# instantiate shared data
Shared.instantiate(app)

from src.controller.admin import admin
from src.controller.auth import auth
from src.controller.review import review
from src.controller.static_files import static_files
from src.controller.typeform import typeform
from src.controller.user import user
from src.controller.logger import logger

# register controllers
app.register_blueprint(admin)
app.register_blueprint(auth)
app.register_blueprint(review)
app.register_blueprint(typeform)
app.register_blueprint(static_files)
app.register_blueprint(user)
app.register_blueprint(logger)
