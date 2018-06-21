from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

if __name__ == '__main__':
    # use port 5000 if PORT environment variable not set
    port = int(os.environ.get('PORT', os.getenv("PORT")))
    app.run(host='localhost', port=port, debug=True,
            use_reloader=False)  # run application from port
