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
python3 start.py -c install
```

## Running

```bash
python3 start.py -c run-windows (Windows)
python3 start.py (Other)
```

## Formatting

```bash
python3 start.py -c format
```

## Deployment

```bash
# Need to install pm2 for this: http://pm2.keymetrics.io/docs/usage/quick-start/#installation
python3 start.py -c deploy
```

