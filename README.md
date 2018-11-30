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
source venv/bin/activate (Unix-like)
cd applications-frontend
npm install

# Use "deactivate" to exit virtual environment
```

Step 3:
```bash
python3 start.py -c install
```

Step 4: Set .env with these default values
```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=<complete this>
OAUTHLIB_INSECURE_TRANSPORT=1
DB_USER=<complete this>
DB_HOSTNAME=localhost
DB_PORT=5432
DB_PASSWORD=<complete this>
DB_NAME=<complete this>
GOOGLE_CLIENT_ID=<complete this>
GOOGLE_CLIENT_SECRET=<complete this>
```

## Running

```bash
python3 start.py
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

## Useful scripts

### Adding an admin

```bash
python3 admin.py -c make-admin
```

### Removing an admin

```bash
python3 admin.py -c remove-admin
```

### Dropping the database

```bash
python3 admin.py -c drop-database
```
