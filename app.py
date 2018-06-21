from flask import Flask

app = Flask(__name__)

if __name__ == '__main__':
    # use port 5000 if PORT environment variable not set
    port = int(os.environ.get('PORT', 5000))
    app.run(host='localhost', port=port, debug=True,
            use_reloader=False)  # run application from port
