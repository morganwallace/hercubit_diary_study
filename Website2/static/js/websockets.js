$(document).ready(function(){
    // var connected = false;
    var stopped =false;
    var samples = {};
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    

    //Receivers for Web Sockets
    socket.on('connect', function(msg) {
        $('#log').append('<p>Web Socket Established</p>');
    });
    socket.on('connection established', function(msg) {
        $('#log').append('<p>Bluetooth Connection Established</p>');
        setInterval( function() { 
            socket.emit('get_sample');
        }, msg.sample_rate);
    });
    socket.on('device response', function(msg) {
        // $('#debug-output').html('<p>Accelerometer data: ' + msg.data + '</p>');
        $("#count_numerator").html(msg.data)
    });
    socket.on('Bluetooth Connection Stopped', function(msg) {
        $('#log').append('<p>Bluetooth connection Stopped</p>');
    });

    //
    //Triggers for Web Socket
    //

    //
    $('#startbtn').click(function(event) {
        if ($('#startbtn').html()=='Done'){
            socket.emit('bluetooth_conn');
            $('#debug-output').show()
        }
        else {
            socket.emit('stop');
            $('#debug-output').hide()
        }
        return false;
    });
    $('form#stop').submit(function(event) {
        socket.emit('stop');
        return false;
    });
    
    $('form#signup-form').submit(function(event) {
        socket.emit('signup');
        return false;
    });
});