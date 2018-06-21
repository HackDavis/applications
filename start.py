import os
import argparse

commands = {
    'all': "export FLASK_APP=app.py; flask run",
    'run-windows': "set FLASK_APP=app.py; flask run",
    'install': "pip3 install -r requirements.txt",
    'format': "autopep8 --in-place --aggressive --aggressive *.py",
    'deploy': "pm2 start start.sh"
}

parser = argparse.ArgumentParser(description='Manage the Flask App')
parser.add_argument("command", help="[all | install | run-windows | format | deploy]", type=str)

if __name__ == "__main__":
    args = parser.parse_args()
    os.system(commands[args.command])
