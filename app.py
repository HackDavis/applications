from flask import Flask
from dotenv import load_dotenv
import os
import src.controller.routes

load_dotenv()

app = Flask(__name__)

if __name__ == '__main__':

    # use port 5000 if PORT environment variable not set

    port = int(os.getenv('PORT', 5000))
    host = os.getenv("HOSTNAME", "localhost")
    app.run(host=host, port=port, debug=True,
            use_reloader=False)
