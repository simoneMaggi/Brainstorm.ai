// NEW CODE https://github.com/MaceTenth/StickyNotes/tree/master

var UPDATE_RATE = 2000;

var GLOBAL_LIST_OF_POSTIT = new Map();

var captured = null;

function syncBackend() {
    $.ajax({
        type: "GET",
        url: "/getPostItList",
        success: function (data) {
            console.log("received new postit from backend", data);
            parsed = JSON.parse(data)

            for (postit in parsed) {
                analized_postit = parsed[postit];
                console.log("analizeing postit", analized_postit);
                captured_id = captured ? captured._id : null;
                console.log("captured", captured_id);
                if (GLOBAL_LIST_OF_POSTIT.has(postit) && captured_id != postit) {
                    console.log("updating postit", postit);
                    var note = GLOBAL_LIST_OF_POSTIT.get(postit);
                    note.text = analized_postit.post_it_text;
                    note.left = Math.round(analized_postit.post_it_left) + 'px';
                    note.top = Math.round(analized_postit.post_it_top) + 'px';
                }
                else if (!GLOBAL_LIST_OF_POSTIT.has(postit)) {
                    console.log("creating new postit", postit);
                    var note = new Note();
                    note.id = analized_postit.post_it_id;
                    note.left = Math.round(analized_postit.post_it_left) + 'px';
                    note.top = Math.round(analized_postit.post_it_top) + 'px';
                    GLOBAL_LIST_OF_POSTIT.set(note.id, note);
                }
            }
        },
        failure: function (errMsg) {
            alert(errMsg);
        }
    });
}

setInterval(function () {
    syncBackend();
}, UPDATE_RATE);

function updatePostIt(postit) {
    body = JSON.stringify({
        'post_it_id': postit.id,
        'post_it_text': postit.text,
        'post_it_left': postit.left,
        'post_it_top': postit.top
    });
    console.log("sending postit to backend", body);

    $.ajax({
        type: "POST",
        url: "/updatePostIt",
        data: body,
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (data) {
            console.log("postit saved", data);
        },
        failure: function (errMsg) {
            alert(errMsg);
        }
    });
}


function removePostIt(postit) {

    body = JSON.stringify({
        'post_it_id': postit.id
    })

    $.ajax({
        type: "POST",
        url: "/removePostIt",
        data: body,
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (data) {
            console.log("postit deleted", data);
        },
        failure: function (errMsg) {
            alert(errMsg);
        }
    });
}


function Note() {
    console.log("creating new note");

    var self = this;

    var note = document.createElement('div');

    note.className = 'note';
    note.addEventListener('mousedown', function (e) { return self.onMouseDown(e) }, false);
    note.addEventListener('click', function () { return self.onNoteClick() }, false);

    this.note = note;

    var close = document.createElement('div');
    close.className = 'closebutton';
    close.addEventListener('click', function (event) { return self.close(event) }, false);
    note.appendChild(close);


    var edit = document.createElement('div');
    edit.className = 'edit';
    edit.setAttribute('contenteditable', true);
    edit.addEventListener('blur', function () { return self.onBlur() }, false);
    edit.addEventListener('keyup', function () { return self.onKeyUp() }, false);
    note.appendChild(edit);
    this.editField = edit;


    document.body.appendChild(note);
    return this;
}

Note.prototype = {
    get id() {
        if (!("_id" in this))
            this._id = 0;
        return this._id;
    },

    set id(x) {
        this._id = x;
    },

    get text() {
        return this.editField.innerHTML;
    },

    set text(x) {
        this.editField.innerHTML = x;
    },

    get left() {
        return this.note.style.left;
    },

    set left(x) {
        this.note.style.left = x;
    },

    get top() {
        return this.note.style.top;
    },

    set top(x) {
        this.note.style.top = x;
    },

    get zIndex() {
        return this.note.style.zIndex;
    },

    set zIndex(x) {
        this.note.style.zIndex = x;
    },

    close: function (event) {
        this.cancelPendingSave();
        var note = this;
        console.log("removing postit with id ", this.id);
        removeNote(this.id);
        document.body.removeChild(this.note);
        removePostIt(note);
    },

    saveSoon: function () {
        this.cancelPendingSave();
        var self = this;
        this._saveTimer = setTimeout(function () { self.save() }, 1000);
    },

    cancelPendingSave: function () {
        if (!("_saveTimer" in this))
            return;
        clearTimeout(this._saveTimer);
        delete this._saveTimer;
    },

    save: function () {
        console.log("saving note", this);
        this.cancelPendingSave();

        if ("dirty" in this) {
            this.timestamp = new Date().getTime();
            delete this.dirty;
        }

        var note = this;
        updatePostIt(note);
    },

    onMouseDown: function (e) {
        console.log("mouse down");
        captured = this;
        this.startX = e.clientX - this.note.offsetLeft;
        this.startY = e.clientY - this.note.offsetTop;

        var self = this;
        if (!("mouseMoveHandler" in this)) {
            this.mouseMoveHandler = function (e) { return self.onMouseMove(e) }
            this.mouseUpHandler = function (e) { return self.onMouseUp(e) }
        }

        document.addEventListener('mousemove', this.mouseMoveHandler, true);
        document.addEventListener('mouseup', this.mouseUpHandler, true);

        return false;
    },

    onMouseMove: function (e) {
        if (this != captured)
            return true;

        this.left = e.clientX - this.startX + 'px';
        this.top = e.clientY - this.startY + 'px';
        return false;
    },

    onMouseUp: function (e) {
        document.removeEventListener('mousemove', this.mouseMoveHandler, true);
        document.removeEventListener('mouseup', this.mouseUpHandler, true);

        this.save();
        return false;
    },

    onNoteClick: function (e) {
        this.editField.focus();
        getSelection().collapseToEnd();
    },

    onKeyUp: function () {
        console.log("key up");
        this.dirty = true;
        this.saveSoon();
    },


    onBlur: function (e) {
        console.log("focus out");
        captured = null;
    }
}

function newNote(text = "") {
    var note = new Note();
    note.id = "postit_" + Math.floor(Math.random() * 1000000);
    note.left = Math.round(Math.random() * 400) + 'px';
    note.top = Math.round(Math.random() * 500) + 'px';
    GLOBAL_LIST_OF_POSTIT.set(note.id, note);
}


