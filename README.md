# applications
An App that helps us process applications for our event

## Installation

Step 1:
```bash
git clone https://github.com/HackDavis/applications.git
cd applications
```

Step 2:
```bash
pip3 install virtualenv
virtualenv -p python3 venv
venv\Scripts\activate (Windows)
source venv/bin/activate (Other)

# Use "deactivate" to exit virtual environment
```

Step 3:
```bash
pip3 install -r requirements.txt (or) make install
```

## Running

```bash
set FLASK_APP=app.py && flask run (or) make run-windows (Windows)
export FLASK_APP=app.py && flask run (or) make (Other)
```

## Formatting

```bash
autopep8 --in-place --aggressive --aggressive *.py (or) make format
```

## Deployment

```bash
# Need to install pm2 for this: http://pm2.keymetrics.io/docs/usage/quick-start/#installation
pm2 start start.sh (or) make deploy
```

