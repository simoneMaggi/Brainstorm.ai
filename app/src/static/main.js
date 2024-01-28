

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

function publishData(data) {
    console.log("the object sent is ", data);
    console.log("last sync data is ", this.lastSyncData);
    syncStream.publishMessage(data);
};

function debugPyScript(data){
    console.log("the object sent is ", data);
    console.log("last sync data is ", this.lastSyncData);
};
