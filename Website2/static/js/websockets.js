$(document).ready(function(){
    // var connected = false;
    var stopped =false;
    var samples = {};
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    
    //
    //    Receivers for Web Sockets
    //
    socket.on('connect', function(msg) {
        $('#log').append('<p>Web Socket Established</p>');
    });

    //Device is connected now so request data from server at the sample rate
    socket.on('connection established', function(msg) {
        $('#log').append('<p>Bluetooth Connection Established</p>');
        setInterval( function() { 
            socket.emit('get_sample');
        }, msg.sample_rate);
    });
    
    // Show output of device in DOM
    socket.on('device response', function(msg) {
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
        }
        else {
            socket.emit('stop',"hi");
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