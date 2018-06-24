import argparse
import subprocess
import sys


'''
exit_with_error prints an error to stderr and exits

Parameters
    error_message(str)
'''


def exit_with_error(error_message):
    print(error_message, file=sys.stderr)
    exit(1)


commands = {
    'run-other': "export FLASK_APP=app.py && flask run",
    'run-windows': "set FLASK_APP=app.py && flask run",
    'install': "pip3 install -r requirements.txt && cd applications-frontend && npm install && cd ..",
    'format': "autopep8 --in-place --aggressive --aggressive *.py",
    'deploy': "pm2 start deploy.sh",
    'save-deps': 'pip3 freeze > requirements.txt'}

parser = argparse.ArgumentParser(description='Manage the Flask App')
parser.add_argument(
    "-c",
    "--command",
    default="run-other",
    help="[run-other | run-windows | install | format | deploy | save-deps]",
    type=str)  # optional, default is 'run-other'

if __name__ == "__main__":
    args = parser.parse_args()
    command = args.command.strip()  # strip all whitespace

    # check if command is a valid option
    if command not in commands:
        exit_with_error(f"command {command} is not valid!")

    try:
        subprocess.run(commands[args.command], shell=True)
    except BaseException:
        pass  # hush
