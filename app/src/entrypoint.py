import os

from flask import Flask, request, jsonify, render_template
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant


import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# from dotenv import load_dotenv
# load_dotenv(os.path.join(os.path.dirname(__file__), '../../.env'))
# get credentials from environment variables
ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
API_KEY = os.getenv('TWILIO_API_KEY')
API_SECRET = os.getenv('TWILIO_API_SECRET')
SYNC_SERVICE_SID = os.getenv('TWILIO_SYNC_SERVICE_SID')

logger.info("account_sid: " + ACCOUNT_SID)
logger.info("api_key: " + API_KEY)
logger.info("api_secret: " + API_SECRET)
logger.info("sync_service_sid: " + SYNC_SERVICE_SID)

app = Flask(__name__)
fake = Faker()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ready')
def ready():
    return "I am ready"


@app.route('/token')
def generate_token():

    username = request.args.get('username', fake.user_name())

    # create access token with credentials
    token = AccessToken(ACCOUNT_SID, API_KEY, API_SECRET, identity=username)
    # create a Sync grant and add to token
    sync_grant = SyncGrant(SYNC_SERVICE_SID)
    token.add_grant(sync_grant)
    tk = token.to_jwt()
    logger.info("token: " + tk)
    return jsonify(identity=username, token=tk)
