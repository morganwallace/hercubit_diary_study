$(document).ready(function(){
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');


    // How these websockets work: 
    // 1. Start button clicked triggers the bluetooth_conn function on app.py 
    $('#startbtn').click(function(event) {
        if ($('#startbtn').html()=='Done'){
            // console.log($("#chosen-goal .goal_count").text());
            // console.log($("#count_denomenator").html());
            $("#count_denomenator").text("/"+$("#chosen-goal .goal_count").text());
            socket.emit('bluetooth_conn');
        }
        return false;
    });

    //Device is connected now so request data from server at the sample rate
    socket.on('connection established', function(msg) {
        $('#log').append('<p>Bluetooth Connection Established</p>');
        fetch_data = setInterval( function() { 
            socket.emit('get_sample');
            if ($('#startbtn').html()=='Start'){
                clearInterval(fetch_data);
                finished_exercising()
            }
        }, msg.sample_rate);
    });
    var goal_completed = function(){
        var goal_num=$("#chosen-goal .goal_count").text()*1;
        var count= $("#count_numerator").html()*1;
        if (count>=goal_num){
            $("#count_numerator").css("color",'green')
        }
    }
    // Show output of device in DOM
    socket.on('device response', function(msg) {
        $("#count_numerator").html(msg.data)
        goal_completed()
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
        if (count>=goal_num){
            console.log('goal completed');
            goal_complete="1";
        }
        var username= $("#username").text();
        var exercise_data={'username':username,count:count,"type":type,"weight":weight,"goal_complete":goal_complete};
        socket.emit('stop',exercise_data);
        $("#count_numerator").text(0);
        $("#count_numerator").css("color",'black')
    }
    //


    
});