

var syncStream;
$(document).ready(function () {
    var syncClient;
    var lastSyncData = null;
    var message = $('#message');
    $.getJSON('/token', function(tokenResponse) {
        console.log(tokenResponse.token);
        syncClient = new Twilio.Sync.Client(tokenResponse.token);
        
        syncClient.on('connectionStateChanged', function(state) {
            if (state != 'connected') {
                message.html('Sync is not live (websocket connection <span style="color: red">' + state + '</span>)…');
            } else {
                message.html('Sync is live!');
            }
        });

        // create the stream object
        syncClient.stream('sendData').then(function(stream) {
            console.log('stream created');
            syncStream = stream;
            // listen update and sync drawing data
            syncStream.on('messagePublished', function(event) {
                console.log('Received Document update event. New data:', event);
                console.log(event.message.data);
                this.lastSyncData = event.message.data;
            });
        });
    });
});


var GLOBAL_LIST_OF_POSTIT = new Map();

function updatePostIt(post_it_json_data){
    // send text data to backend endpoint /addPostIt
    // update the global list of postit
    // transform from string to json
    var post_it_json = JSON.parse(post_it_json_data);
    this.GLOBAL_LIST_OF_POSTIT.set(post_it_json.post_it_id, 
        post_it_json.post_it_text);

    $.ajax({
        type: "POST",
        url: "/updatePostIT",
        data: JSON.stringify({'post_it_json': post_it_json_data}),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(data){
            console.log("sent new postit to backend", data);
        },
        failure: function(errMsg) {
            alert(errMsg);
        }
    });
}

function removePostIt(post_it_id){

    this.GLOBAL_LIST_OF_POSTIT.delete(post_it_id);

    $.ajax({
        type: "POST",
        url: "/removePostIT",
        data: JSON.stringify({'post_it_id': post_it_id}),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(data){
            console.log("sent new postit to backend", data);
        },
        failure: function(errMsg) {
            alert(errMsg);
        }
    });
}

function publishData(data) {
    console.log("the object sent is ", data);
    console.log("last sync data is ", this.lastSyncData);
    syncStream.publishMessage(data);
};



function addPostIt_UI(idea){
    var postIt = document.createElement('div');
    postIt.className = "postit";
    postIt.draggable = true;
    postIt.contentEditable = true;
    // add a button on top to delete the postit
    var deleteButton = document.createElement('button');
    deleteButton.innerHTML = "X";
    deleteButton.className = "deleteButton";
    deleteButton.onclick = function(event){
        console.log("delete button clicked");
        postIt = event.target.parentElement;
        removePostIt(postIt.id);
        postIt.remove();
    };
    postIt.appendChild(deleteButton);



    // random UUID
    postIt.id = "postit_" + Math.floor(Math.random() * 1000000);
    postIt.innerHTML = idea;

    // put it in a random position on the witheboard
    postIt.style.left = Math.floor(Math.random() * 500) + "px";
    postIt.style.top = Math.floor(Math.random() * 500) + "px";

    document.getElementById('page').appendChild(postIt);

    return postIt.id;
}





function getNewPostIt(){
    $.ajax({
        type: "GET",
        url: "/getNewIdea",
        success: function(data){
            console.log("received new postit from backend", data);
            // publishData(data);
            if (data.hasOwnProperty('idea'))
            {
                var id = addPostIt_UI(data.idea);
                updatePostIt(JSON.stringify({'post_it_id': id, 'post_it_text': data.idea}));
            }
        },
        failure: function(errMsg) {
            alert(errMsg);
        }
    });
}

setInterval(function(){
    getNewPostIt();
}, 50000);



