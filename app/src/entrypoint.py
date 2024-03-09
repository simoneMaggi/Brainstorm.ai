import os
import random

from flask import Flask, request, jsonify, render_template
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant
import json

from brainstormer.brainstormer import Brainstomer

from utils.utils import BRAINSTORM_LOGGER


# from dotenv import load_dotenv
# load_dotenv(os.path.join(os.path.dirname(__file__), '../../.env'))
# get credentials from environment variables
ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', 'xxxxxxx')
API_KEY = os.getenv('TWILIO_API_KEY', 'xxxxxxx')
API_SECRET = os.getenv('TWILIO_API_SECRET', 'xxxxxxx')
SYNC_SERVICE_SID = os.getenv('TWILIO_SYNC_SERVICE_SID', 'xxxxxxx')

BRAINSTORM_LOGGER.info("account_sid: " + ACCOUNT_SID)
BRAINSTORM_LOGGER.info("api_key: " + API_KEY)
BRAINSTORM_LOGGER.info("api_secret: " + API_SECRET)
BRAINSTORM_LOGGER.info("sync_service_sid: " + SYNC_SERVICE_SID)

app = Flask(__name__)
fake = Faker()
POST_IT_LIST = {}
IDEA_GENERATOR = Brainstomer()

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
    BRAINSTORM_LOGGER.info("token: " + tk)
    return jsonify(identity=username, token=tk)

@app.route('/updatePostIT', methods=['POST'])
def add_post_it():
    """
    Receive the text of the new insertend post-it in the request body
    and append it to the list of post-its.
    """
    try:
        BRAINSTORM_LOGGER.info("addPostIt")
        post_it_json = request.json.get('post_it_json', "\{\}")
        BRAINSTORM_LOGGER.info("post_it_json: " + post_it_json)
        post_it_json = json.loads(post_it_json)
        POST_IT_LIST[post_it_json['post_it_id']] = post_it_json['post_it_text'] 
        BRAINSTORM_LOGGER.info("POST_IT_LIST: " + str(POST_IT_LIST))
        return jsonify(identity="ok")
    except:
        BRAINSTORM_LOGGER.info("addPostIt: error")
        return jsonify(identity="error"), 400

@app.route('/getPostItList', methods=['GET'])
def get_post_it_list():
    """
    Return the list of post-its.
    """
    BRAINSTORM_LOGGER.info("getPostItList")
    return jsonify(identity=POST_IT_LIST)

@app.route('/resetPostItList', methods=['POST'])
def reset_post_it_list():
    """
    Reset the list of post-its.
    """
    POST_IT_LIST.clear()
    BRAINSTORM_LOGGER.info("resetPostItList")
    return jsonify(identity="ok")

@app.route('/removePostIt', methods=['POST'])
def remove_post_it():
    """
    Receive the text of the post-it to remove in the request body
    and remove it from the list of post-its.
    """
    post_it_to_delete = request.json.get('post_it_id', "err")
    BRAINSTORM_LOGGER.info("post_it_to_delete: " + post_it_to_delete)
    if post_it_to_delete in POST_IT_LIST:
        del POST_IT_LIST[post_it_to_delete]
        BRAINSTORM_LOGGER.info("removed correctly the PostIt")
    else:
        BRAINSTORM_LOGGER.info("post_it not found")
        return jsonify(identity="error"), 404
    return jsonify(identity="ok")

@app.route('/getNewIdea', methods=['GET'])
def get_new_idea():
    """
    Return a new idea. From the LLM model.
    """
    global IDEA_GENERATOR
    
    ideas_list = POST_IT_LIST.values()
    try:
        idea = IDEA_GENERATOR.generate_idea(ideas_list)
    except:
        idea = None
    if idea is None:
        return jsonify(identity="ok")
    BRAINSTORM_LOGGER.info("getNewIdea "+ idea)
    return jsonify(identity='ok', idea=idea)
