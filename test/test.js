var Stomp = require('stomp-client');
var destination = '/topic/topic1';
var client = new Stomp('127.0.0.1', 61613);

client.connect(function(sessionId) {
    client.subscribe(destination, function(body, headers) {
      console.log('This is the body of a message on the subscribed queue:', body);
    });

    client.publish(destination, 'Oh herrow');
});
