import random
from pyscript  import document, window
import json
import js



POST_IT_MAP = {}
EDITING_POST_IT = False
CLICKED_ON_POSTIT = False

def manageUserClick(event):
    global EDITING_POST_IT
    global CLICKED_ON_POSTIT

    if not CLICKED_ON_POSTIT and not EDITING_POST_IT:
        window.console.log("you are clicking on the withboard in order to create a new postit")
        EDITING_POST_IT = True # now you are editing a postit
        CLICKED_ON_POSTIT = False
        createPostIt(event)
    elif not CLICKED_ON_POSTIT and EDITING_POST_IT:
        window.console.log("you are clicking on the whiteboard in order to finish editing the postit")
        EDITING_POST_IT = False
        CLICKED_ON_POSTIT = False
    elif CLICKED_ON_POSTIT and EDITING_POST_IT:
        window.console.log("you are clicking on a postit in order to edit it")
        CLICKED_ON_POSTIT = True
        EDITING_POST_IT = True
    CLICKED_ON_POSTIT = False


def savePostIt(event):
    global POST_IT_MAP
    global EDITING_POSTIT
    global CLICKED_ON_POSTIT

    CLICKED_ON_POSTIT = False
    EDITING_POSTIT = False

    post_it = event.target
    post_it_text = post_it.innerText
    post_it_id = post_it.id
    POST_IT_MAP[post_it_id] = post_it_text
    postit_json = json.dumps({"post_it_id": post_it_id, "post_it_text": post_it_text})
    window.console.log("saving postit id "+ post_it_id + " with text: " + post_it_text)
    js.updatePostIt(postit_json)


def editTextInPostIt(event):
    global POST_IT_MAP
    global EDITING_POST_IT
    global CLICKED_ON_POSTIT

    CLICKED_ON_POSTIT = True
    EDITING_POST_IT = True
    post_it = event.target
    post_it_id = post_it.id
    window.console.log(f"editing post it id: {post_it_id}")
    if post_it_id not in POST_IT_MAP:
        # firsst click on the postit
        post_it.innerText = ""
        POST_IT_MAP[post_it_id] = ""

def deletePostIt(event):
    global POST_IT_MAP
    post_it = event.target.parentElement
    post_it_id = post_it.id
    window.console.log(f"deleting post it id: {post_it_id}")
    del POST_IT_MAP[post_it_id]
    post_it.remove()
    js.removePostIt(post_it_id)




def createPostIt(event):
    global POST_IT_MAP
    whiteboard = document.querySelector("#page")
    post_it = document.createElement("div")
    post_it.setAttribute("class", "postit")
    post_it.setAttribute("draggable", "true")
    post_it.setAttribute("contenteditable", "true")
    post_it.setAttribute("id", "postit_" + str(hash(str(random.uniform(0, 100000)))))
    post_it.onblur = savePostIt
    post_it.onclick = editTextInPostIt
    # the postit has a little button on the top right corner to delete it
    delete_button = document.createElement("button")
    delete_button.setAttribute("class", "delete_button")
    delete_button.onclick = deletePostIt
    delete_button.innerText = "X"
    post_it.appendChild(delete_button)


    # post_it._js.onblur = savePostIt
    post_it.innerText = random.choice(["The best idea in the history of brainstorming", 
                                       "Idea here", "Eureka!", 
                                       "Silly Idea, but It is okay! It is just a brainstorming session"])
    post_it.style.left = str(event.clientX) + "px"
    post_it.style.top = str(event.clientY) + "px"
    whiteboard.appendChild(post_it)
    window.console.log(f"post it created until now: \n {POST_IT_MAP}")


