import twilio
from pyscript  import document

def print_ciao(event):
    page_div = document.querySelector("#page")
    page_div.innerText = "Ciao " + event.data["identity"] + "!"
        