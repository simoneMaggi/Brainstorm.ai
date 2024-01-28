import os
import random

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
POST_IT_LIST = ["Start your brainstorm here!"]

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

@app.route('/addPostIt', methods=['POST'])
def add_post_it():
    """
    Receive the text of the new insertend post-it in the request body
    and append it to the list of post-its.
    """
    post_it_text = request.args.get('post_it_text', "default")
    POST_IT_LIST.append(post_it_text)
    logger.info("addPostIt")
    return jsonify(identity="ok")

@app.route('/getPostItList', methods=['GET'])
def get_post_it_list():
    """
    Return the list of post-its.
    """
    logger.info("getPostItList")
    return jsonify(identity=POST_IT_LIST)

@app.route('/resetPostItList', methods=['POST'])
def reset_post_it_list():
    """
    Reset the list of post-its.
    """
    POST_IT_LIST = ["Start your brainstorm here!"]
    logger.info("resetPostItList")
    return jsonify(identity="ok")

@app.route('/removePostIt', methods=['POST'])
def remove_post_it():
    """
    Receive the text of the post-it to remove in the request body
    and remove it from the list of post-its.
    """
    post_it_to_delete = request.args.get('post_it_text', "default")
    POST_IT_LIST = list((POST_IT_LIST).difference(set(post_it_to_delete)))
    logger.info("removePostIt")
    return jsonify(identity="ok")

@app.route('/getNewIdea', methods=['GET'])
def get_new_idea():
    """
    Return a new idea. From the LLM model.
    """
    logger.info("getNewIdea")
    idea = random.choice(['Bisogna fare brainstorming', "Questa è una idea", "Questa è un'altra idea"])
    return jsonify(identity=idea)
