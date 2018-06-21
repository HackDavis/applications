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
pip3 install -r requirements.txt (or) python3 start.py install
```

## Running

```bash
set FLASK_APP=app.py && flask run (or) python3 start.py run-windows (Windows)
export FLASK_APP=app.py && flask run (or) python3 start.py all (Other)
```

## Formatting

```bash
autopep8 --in-place --aggressive --aggressive *.py (or) python3 start.py format
```

## Deployment

```bash
# Need to install pm2 for this: http://pm2.keymetrics.io/docs/usage/quick-start/#installation
pm2 start deploy.sh (or) python3 start.py deploy
```

