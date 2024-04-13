from dataclasses import dataclass
import os
import random
from typing import Dict
import threading
import time
from flask import Flask, request, jsonify, render_template
import json

from brainstormer.brainstormer import Brainstomer

from utils.utils import BRAINSTORM_LOGGER

@dataclass
class PostIt:
    post_it_id: str
    post_it_text: str
    post_it_left: int
    post_it_top: int

app = Flask(__name__)
POST_IT_LIST : Dict[str, PostIt] = {}
IDEA_GENERATOR = Brainstomer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ready')
def ready():
    return "I am ready"

@app.route('/updatePostIt', methods=['POST'])
def add_post_it():
    """
    Receive the text of the new insertend post-it in the request body
    and append it to the list of post-its.
    """
    try:
        BRAINSTORM_LOGGER.info("addPostIt")
        BRAINSTORM_LOGGER.info("post_it_json: " + str(request.json))

        POST_IT_LIST[request.json['post_it_id']] = PostIt(
            post_it_id=request.json['post_it_id'],
            post_it_text=request.json['post_it_text'],
            post_it_left=request.json['post_it_left'],
            post_it_top=request.json['post_it_top']
        )

        BRAINSTORM_LOGGER.info("POST_IT_LIST: " + str(POST_IT_LIST))
        return jsonify(identity="ok")
    except Exception as e:
        BRAINSTORM_LOGGER.info(f"addPostIt: {e}")
        
        return jsonify(identity="error"), 400

@app.route('/getPostItList', methods=['GET'])
def get_post_it_list():
    """
    Return the list of post-its.
    """
    BRAINSTORM_LOGGER.debug(f"getPostItList: \n {POST_IT_LIST}")
    postit_list_json = json.dumps({post_it.post_it_id: post_it.__dict__ for post_it in POST_IT_LIST.values()})
    return postit_list_json

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
    post_it_to_delete = request.args.get('post_it_id', "err")
    if post_it_to_delete in POST_IT_LIST:
        del POST_IT_LIST[post_it_to_delete]
        BRAINSTORM_LOGGER.info("removePostIt")
    else:
        BRAINSTORM_LOGGER.info("removePostIt: post_it not found")
        return jsonify(identity="error"), 404
    return jsonify(identity="ok")


if __name__ == '__main__':
    def create_idea(idea_generator: Brainstomer, post_it_list: Dict[str, PostIt]):
        while True:
            ideas = [post_it.post_it_text for post_it in post_it_list.values()]
            idea = idea_generator.generate_idea(ideas)
            if idea:
                posit_id = random.randint(0, 100000000)
                post_it_list[posit_id] = PostIt(
                    post_it_id=str(posit_id),
                    post_it_text=idea,
                    post_it_left=random.randint(0, 400),
                    post_it_top=random.randint(0, 400)
                )
            time.sleep(3000)
    

    threading.Thread(target=create_idea, args = [IDEA_GENERATOR, POST_IT_LIST]).start()

    BRAINSTORM_LOGGER.info("Thread brainstormer started")
    app.run(host='0.0.0.0', port=5000)