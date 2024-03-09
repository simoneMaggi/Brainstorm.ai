// NEW CODE https://github.com/MaceTenth/StickyNotes/tree/master

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


let GLOBAL_MAP_NOTES = new Map();

function updateNote(note_id, note_text){
    // send text data to backend endpoint /addPostIt
    // update the global list of postit
    // transform from string to json
    GLOBAL_MAP_NOTES.set(note_id, note_text);
        
        $.ajax({
            type: "POST",
        url: "/updatePostIT",
        data: JSON.stringify({'post_it_json': JSON.stringify({
            'post_it_id': note_id,
            'post_it_text': note_text
        })}),
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

function removeNote(note_id){

    GLOBAL_MAP_NOTES.delete(note_id);

    $.ajax({
        type: "POST",
        url: "/removePostIt",
        data: JSON.stringify({'post_it_id': note_id}),
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




var captured = null;

function Note(){
    console.log("creating new note");
    
    var self = this;
    
    var note = document.createElement('div');
    
    note.className = 'note';
    note.addEventListener('mousedown', function(e) { return self.onMouseDown(e) }, false);
    note.addEventListener('click', function() { return self.onNoteClick() }, false);
    
    this.note = note
    
    var close = document.createElement('div');
    close.className = 'closebutton';
    close.addEventListener('click', function(event) { return self.close(event) }, false);
    note.appendChild(close);
    
    var edit = document.createElement('div');
    edit.className = 'edit';
    edit.setAttribute('contenteditable', true);
    edit.addEventListener('keyup', function() { return self.onKeyUp() }, false);
    note.appendChild(edit);
    this.editField = edit;
    
    document.body.appendChild(note);
    return this;
}

Note.prototype = {
    get id(){
        if (!("_id" in this))
        this._id = 0;
    return this._id;
},

set id(x){
    this._id = x;
},

get text(){
    return this.editField.innerHTML;
},

set text(x){
    this.editField.innerHTML = x;
},

get left(){
    return this.note.style.left;
},

set left(x){
    this.note.style.left = x;
},

get top(){
    return this.note.style.top;
    },
    
    set top(x){
        this.note.style.top = x;
    },
    
    get zIndex(){
        return this.note.style.zIndex;
    },
    
    set zIndex(x){
        this.note.style.zIndex = x;
    },
    
    close: function(event){
        this.cancelPendingSave();
        var note = this;
        console.log("removing postit with id ", this.id);
        removeNote(this.id);
        document.body.removeChild(this.note);
    },
    
    saveSoon: function(){
        this.cancelPendingSave();
        var self = this;
        this._saveTimer = setTimeout(function() { self.save() }, 1000);
    },
    
    cancelPendingSave: function(){
        if (!("_saveTimer" in this))
        return;
    clearTimeout(this._saveTimer);
    delete this._saveTimer;
},

save: function(){
    console.log("saving note", this);
    this.cancelPendingSave();
    updateNote(this.id, this.text);
    
    if ("dirty" in this) {
        this.timestamp = new Date().getTime();
        delete this.dirty;
    }
    
    var note = this;
    
},

onMouseDown: function(e){
    console.log("mouse down");
    captured = this;
    this.startX = e.clientX - this.note.offsetLeft;
    this.startY = e.clientY - this.note.offsetTop;
    
    var self = this;
    if (!("mouseMoveHandler" in this)) {
        this.mouseMoveHandler = function(e) { return self.onMouseMove(e) }
        this.mouseUpHandler = function(e) { return self.onMouseUp(e) }
    }
    
    document.addEventListener('mousemove', this.mouseMoveHandler, true);
    document.addEventListener('mouseup', this.mouseUpHandler, true);
    
    return false;
},

onMouseMove: function(e){
    if (this != captured)
    return true;

this.left = e.clientX - this.startX + 'px';
this.top = e.clientY - this.startY + 'px';
return false;
},

onMouseUp: function(e){
    document.removeEventListener('mousemove', this.mouseMoveHandler, true);
    document.removeEventListener('mouseup', this.mouseUpHandler, true);
    
    this.save();
    return false;
},

onNoteClick: function(e){
    this.editField.focus();
    getSelection().collapseToEnd();
},

onKeyUp: function(){
    console.log("key up");
    this.dirty = true;
    this.saveSoon();
},
}

function newNote(text = ""){
    var note = new Note();
    note.id = "postit_" + Math.floor(Math.random() * 1000000);
    note.left = Math.round(Math.random() * 400) + 'px';
    note.top = Math.round(Math.random() * 500) + 'px';
    if (text != "")
    {
        note.text = text;
    }
    
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
                newNote(data.idea);
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


   