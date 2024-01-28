import random
from pyscript  import document, window
import json
import js
# import requests


POST_IT_MAP = {}
EDITING_POST_IT = False
FINISHED_EDITING_POSTIT = False

def manageUserClick(event):
    global EDITING_POST_IT
    global FINISHED_EDITING_POSTIT
    window.console.log(str(event) + "\n" + str(event.clientX) + "\n" + str(event.clientY) 
                 + "\n you are editing a postit " + str(EDITING_POST_IT)
                 )
    if FINISHED_EDITING_POSTIT:
        FINISHED_EDITING_POSTIT = False
        EDITING_POST_IT = False
        return
    if not EDITING_POST_IT:
        EDITING_POST_IT = True
        createPostIt(event)

def savePostIt(event):
    global POST_IT_MAP
    global FINISHED_EDITING_POSTIT
    post_it = event.target
    post_it_text = post_it.innerText
    window.console.log(str(event) + "\n" + str(post_it_text))
    post_it_id = post_it.id
    POST_IT_MAP[post_it_id] = post_it_text
    post_it_state_string = json.dumps(POST_IT_MAP)
    js.debugPyScript(post_it_state_string)
    FINISHED_EDITING_POSTIT = True
    # requests.post("http://localhost:5000/addPostIt", data={"post_it_text": post_it_text})

def clearPostItText(event):
    global POST_IT_MAP
    post_it = event.target
    post_it.innerText = ""
    post_it_id = post_it.id
    POST_IT_MAP[post_it_id] = ""
    post_it_state_string = json.dumps(POST_IT_MAP)
    js.debugPyScript(post_it_state_string)

def clearPostItIfFirstClick(event):
    global POST_IT_MAP
    post_it = event.target
    post_it_id = post_it.id
    if post_it_id not in POST_IT_MAP:
        post_it.innerText = ""
        POST_IT_MAP[post_it_id] = ""
        post_it_state_string = json.dumps(POST_IT_MAP)
        js.debugPyScript(post_it_state_string)

def createPostIt(event):
    global POST_IT_MAP
    whiteboard = document.querySelector("#page")
    post_it = document.createElement("div")
    post_it.setAttribute("class", "postit")
    post_it.setAttribute("draggable", "true")
    post_it.setAttribute("contenteditable", "true")
    post_it.setAttribute("id", "postit_" + str(len(POST_IT_MAP)))
    post_it.onblur = savePostIt
    post_it.onclick = clearPostItIfFirstClick
    # post_it._js.onblur = savePostIt
    post_it.innerText = random.choice(["The best idea in the history of brainstorming", 
                                       "Idea here", "Eureka!", 
                                       "Silly Idea, but It is okay! It is just a brainstorming session"])
    post_it.style.left = str(event.clientX) + "px"
    post_it.style.top = str(event.clientY) + "px"
    whiteboard.appendChild(post_it)
    window.console.log(f"post it created until now: \n {POST_IT_MAP}")
    

def print_ciao(event):
    global POST_IT_MAP
    page_div = document.querySelector("#page")
    page_div.innerText = "Ciao " + str(event) + "!"
    window.alert("Ciao " + str(event) + "!")
    window.console.log("Ciao " + str(event) + "!")
    post_it_state_string = json.dumps(POST_IT_MAP)
    js.debugPyScript(post_it_state_string)
