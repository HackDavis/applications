import argparse
import subprocess
import sys


def exit_with_error(error_message):
    '''
    exit_with_error prints an error to stderr and exits

    Parameters
        error_message(str)
    '''
    print(error_message, file=sys.stderr)
    exit(1)


commands = {
    'run': "flask run",
    'unit-test': "pytest test/unit",
    # needs server to be running
    'integ-test': "pytest test/integ --tavern-global-cfg test/config/common.yaml",
    'install': "pip3 install -r requirements.txt",
    'format': "yapf --recursive -i -vv ./src *.py",
    'deploy': "pm2 start deploy.sh",
    'save-deps': 'pip3 freeze > requirements.txt'
}

parser = argparse.ArgumentParser(description='Manage the Flask App')
parser.add_argument(
    "-c", "--command", default="run", choices=list(commands.keys()),
    type=str)  # optional, default is 'run'

if __name__ == "__main__":
    args = parser.parse_args()
    command = args.command

    # check if command is a valid option
    if command not in commands:
        exit_with_error(f"command {command} is not valid!")

    try:
        subprocess.run(commands[command], shell=True)
    except KeyboardInterrupt:
        pass  # hush
