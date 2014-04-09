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
        fetch_data = setInterval( function() { 
            socket.emit('get_sample');
            // console.log('rate to fetch data from server/device: '+msg.sample_rate)
            if ($('#startbtn').html()=='Start'){
                clearInterval(fetch_data);
                finished_exercising()
            }
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
    var finished_exercising= function(){
        //Gather data about exercise session for insertion into database
        var thisgoal=$("#chosen-goal span").html();
        var type=$("#chosen-goal .exercise_type").text();
        var weight=$("#chosen-goal .goal_weight").text();
        var goal_num=$("#chosen-goal .goal_count").text()*1;
        var count= $("#count_numerator").html()*1;
        var goal_complete= "0";
        console.log(count+" "+goal_num)
        if (count>=goal_num){
            console.log(' yay, goal completed');
            goal_complete="1";
        }
        var username= $("#username").text();
        var exercise_data={'username':username,count:count,"type":type,"weight":weight,"goal_complete":goal_complete};
        socket.emit('stop',exercise_data);
        $("#count_numerator").text(0);
    }
    //
    $('#startbtn').click(function(event) {
        if ($('#startbtn').html()=='Done'){
            socket.emit('bluetooth_conn');
        }
        //finished exercising
        // else {
        //     finished_exercising()

        // }
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