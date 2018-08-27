from flask import Flask
from dotenv import load_dotenv

from src.controller.review import review
from src.controller.static_files import static_files
import src.db.models.UserModel as UserModel
import src.db.models.ApplicationsModel as ApplicationsModel

load_dotenv()

UserModel.initialize_user_model()
ApplicationsModel.initialize_applications_model()

app = Flask(__name__)

# load config
app.config.from_object('src.config.config.Config')
app.secret_key = app.config.get('SECRET_KEY')
app.register_blueprint(review)
app.register_blueprint(static_files)
