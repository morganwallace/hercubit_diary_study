// Backend info
var exerciseTableId = "1OBObNVqy3kHdpdDaGaC1xH5sfmGWb-oGBNfosOMo";
var goalTableId = "1R8s9_P6t9IH8DOG3rBieAh05W9_H5C2K4MdQCuRG";
var scopes = 'https://www.googleapis.com/auth/fusiontables';
var clientId = '755998331131-jsf1f67tj7ojvlc9bai1p6273qidsbn5.apps.googleusercontent.com';
// var apiKey = 'AIzaSyD1nrNVFFr6z0_S9vOryX9kF7U-7pVZDBU'; //charles
var apiKey = "AIzaSyA8juHC7LiH4pY4HM3XPIUTuFFt6y2jWqU"
var username = "kate";
var token = "";

var badgeName = ["Newbie","Goal","33","44","55","66","77","88","99"];
var badgeDesc = ["Signed up for Hercubit!", "Set your first goal!","","","","","","",""];

function auth() {
    var config = {
        'client_id': clientId,
        'scope': scopes
    };
    gapi.auth.authorize(config, function() {
      console.log('login complete');
      // console.log(gapi.auth.getToken());
      token = gapi.auth.getToken().access_token;
      console.log(token);
    });
}

$(document).ready(function () {

    /* If first time use */
    var firstTimeUse = 1;

    if ($("#username").html()!='') {
        console.log('user already logged in as:')
        console.log($("#username").html());
        firstTimeUse=false;
    }
    if (firstTimeUse) {

        $("#white-overlay").show();
        $("#signup-form").show();
        $("header div.header-action").hide();
        
        $("#signup").submit(function(e){
            $("#white-overlay").hide();
            $("#signup-form").hide();
            $("header div.header-action").show();
            e.preventDefault();

            // getNewbadge(0);
            auth();   
        });
    }
    
    // getNewbadge(0);


    $("#signup").submit(function(e){
        $("#white-overlay").hide();
        $("#signup-form").hide();
        $("header div.header-action").show();
        e.preventDefault();
        signup()
        getNewbadge(0);
    });


    function signup(){
            $.post("./signup",
                $("#signup").serialize(),
                function(data){
                    console.log(data);
                    console.log(data.username);
                    // if(data.success == true){
                    //     $("#username").text(data.username);
                    //     $("#signup-wrapper").hide();
                    //     $("#welcome-wrapper").show();
                    //     $("#error-message").text("");
                    // }
                    // else {
                    //     console.log(data.reason);
                    //     // $("#error-message").text(data.reason);
                    // }

                }
        );
        return false;
    }

    //When the user clicks logout call logout in app.py and delete cookie
    // then refresh when python sends the success response
    $("#logout").click(function(){
        logout();
    });
    function logout(){
            $.post("./logout",
                function(data){
                    console.log('successful logout');

                    //send the user back to the log in screen by refreshing.
                    window.location.href ="/";
                }
                
        );
        
        return false;

    }

    /* Start */
    /************************************************************************/

	// Click Start to see count
	$("#startbtn").on('click', function(){
		if ($("section.metadata").attr('data-state') === 'neutral') {
            $("section.metadata").attr('data-state', 'slide-out');
            $("section.social").attr('data-state', 'slide-out');
            $("section.main .card").attr('data-state', 'slide-out');
            $("section.main #count").attr('data-state', 'slide-out');
            $("#startbtn").attr('data-state', 'slide-out');
            $("#startbtn").text("Done");
        } 
        else {
            $("section.metadata").attr('data-state', 'neutral');
            $("section.social").attr('data-state', 'neutral');
            $("section.main .card").attr('data-state', 'neutral');
            $("section.main #count").attr('data-state', 'neutral');
            $("#startbtn").attr('data-state', 'neutral');
            $("#startbtn").text("Start");
        }
	});

    /* Goal */
    /************************************************************************/

    // TODO: Loop through database to get goals
    getAllGoals();
    // selectGoalData();

    /* Activity */
    /************************************************************************/
    // TODO: Get activity freq from database
    var activityArray = [0,1,2,0,0,1,1, 3,3,2,0,0,0,0, 0,0,0,0,0,0,0, 0,0,0,0,0,0,0, 0,0];
    // var activityArray = [0,0,0,0,0,0,0, 0,0,0,0,0,0,0, 0,0,0,0,0,0,0, 0,0,0,0,0,0,0, 0,0];

    for (var i=1; i<activityArray.length+1; i++) {
        var code = '<div class="code" id="code-'+i+'"></div>';
        $("#activity-map").append(code);
        $("#code-"+i).addClass("level-"+activityArray[i-1]);
    }


    /* Friends */
    /************************************************************************/
    // TODO: Loop through database to get friend list
    var friendArray = ["Morgan", "Charles", "Shaohan", "Kate"];
    var friendDesc = ["Accomplished 3 goals", "Achieved 1500 lbs", "Accomplished 2 goals", "Accomplished 1 goals"]

    // Get goals from the database
    for (var i=1; i<friendArray.length+1; i++) {
        $("section.social div.card").append('<div class="friend lines clear"><div class="num">'+i+'</div><div class="icon"><img src="../static/img/'+friendArray[i-1]+'.png"></div><div class="desc">'+friendDesc[i-1]+'</div><div class="menu"><button class="button-small">Message</button><button class="button-small">Challenge</button></div></div>');
    };


    $("html").on("click", function(){
        $("div.friend").css("height", "80px");
        $("div.friend").find("div.menu").hide();
    })
    $("div.friend").on("click", function(e){
        e.stopPropagation();
        $("div.friend").css("height", "80px");
        $("div.friend").find("div.menu").hide();
        $(this).css("height","160px");
        $(this).find("div.menu").show();
    });


    /* Achievements */
    // TODO: Loop through database to get badge list
    var badgeArray = [1,1,0,0,0,0,0,0,0];
    

    for (var i=0; i<badgeArray.length; i++){
        if (badgeArray[i]==1) {
            $("#achievements").append('<div class="achievement lines clear"><div class="icon"><img src="../static/img/'+badgeName[i]+'.png"></div><div class="desc"><h1>'+badgeName[i]+'</h1><h4>'+badgeDesc[i]+'</h4></div></div>');
        }
    }

});


function getNewbadge (num) {
    console.log("bkj"+num);
    $("#modal-badge").find("h1").text(badgeName[num]);
    $("#modal-badge").find("img").attr("src","../static/img/"+badgeName[num]+".png");
    $("#modal-badge").find("span").text("You've " + badgeDesc[num]);
    $("#modal-overlay").show();
    $("#modal-badge").show();
    $("#modal-badge").addClass("animated bounceIn");
    // $("#modal-badge img").addClass("animated tada");
}

function getAllGoals () {
    var q = "SELECT * FROM " + goalTableId + " WHERE username='" + username+"'";
    var queryText = encodeURI(q);
    var query = "https://www.googleapis.com/fusiontables/v1/query?sql=" + queryText + "&key=" + apiKey;

    $.ajax({
        type: "get",
        url: query,
        success: function(data){
            console.log("succcccess");
            console.log(data);

            var goalArray = [];
            goalArray = data.rows;
            var goalArrayAddone = 0;

            // Get goals from the database
            // Clear the container first
            $("section.main div.card").empty();
            if (data.rows) {
                for (var i=1; i<goalArray.length+1; i++) {
                    $("section.main div.card").append('<div class="goal lines clear" data-state="neutral" id="goal-'+i+'"><div class="num">Goal '+i+'</div><div class="desc">'+goalArray[i-1][1]+" ("+goalArray[i-1][3]+"lbs) x"+goalArray[i-1][2]+'</div><div class="trash"><img src="../static/img/trash.png"></div></div>');
                };
                // Set the number for new goal
                goalArrayAddone = goalArray.length+1;
            }
            else {
                goalArrayAddone = 1;
            }
            $("section.main div.card").append('<div class="goal lines clear" data-state="neutral" id="add-goal"><div class="num">+</div><div class="desc">Add New Goal</div></div>');
            
            $("#modal-goal h1").text("Goal "+ goalArrayAddone);


            // Hover goal to see trash button
            $("div.goal").hover(
                function() {
                    $(this).children(".trash").attr('data-state', 'hover');
                },
                function() {
                    $(this).children(".trash").attr('data-state', 'neutral');
                }
            );
            // Click to delete the goal
            $("div.goal .trash").on('click', function(){
                // console.log($(this).parent()[0].id);
                $(this).parent()[0].remove();
                // TODO: Delete this goal from database
            });
            // Click to choose the goal
            $("div.goal").on('click', function(){
                if (this.id!=="add-goal") {
                    $("#chosen-goal span").text($(this).find('div.num').text() +": "+ $(this).find('div.desc').text());
                }
            });

            // Pop up Modal after clicking on Add goal
            $("#add-goal").on('click', function(){
                $("#modal-overlay").show();
                $("#modal-goal").show();
            });
            $("#modal-overlay").on('click', function(){
                $("#modal-overlay").hide();
                $("#modal-goal").hide();
                $("#modal-badge").hide();
            });
            $("#modal-add-goal").submit(function(e){
                $("#modal-overlay").hide();
                $("#modal-goal").hide();

                // TODO: update database & refresh this page to show new goal list
                // addNewGoal($("#modal-add-goal select[name='type']").val(), $("#modal-add-goal input[name='count']").val(), "12");
                // addNewGoal();
                // updateTable();
                // insertData();
                e.preventDefault();
                insertGoalData();
            });
        }
    });
}

// function addNewGoal () {
//     // console.log("type: "+t+" count: "+c);
//     // var q = "INSERT INTO " + goalTableId;
//     // var q = "SELECT * FROM " + goalTableId + " WHERE username='" + username+"'";
//     // var queryText = encodeURI(q);
//     var query = "https://www.googleapis.com/fusiontables/v1/query";

//     $.ajax({
//         type: "POST",
//         url: query,
//         data: {
//                 "sql": "INSERT "+goalTableId+" (username, exercise) VALUES (test, type)",
//         },
//         success: function(data){
//             console.log("Successfully addNewGoal");
//             console.log(data);
//         }
//     });
// }


// function updateTable() {
//     var URL = "https://www.googleapis.com/fusiontables/v1/query";

//     $.ajax({
//         type: "post",
//         url: URL,
//         dataType: "jsonp",

//         data: {
//             featureClass: "P",
//             style: "full",
//             'key': apiKey,
//             'sql': "INSERT "+goalTableId+" (username, exercise) VALUES ('test', 'type')",
//             // maxRows: 12,
//             //name_startsWith: request.term
//         },
//         beforeSend: function(xhr) {
//             xhr.setRequestHeader("Authorization", "GoogleLogin auth=" + token);
//         },
//         success: function (data) {
//             console.log("suc");
//             console.log(data);
//         },


//     });
// }

// ===================================


// Run a request to INSERT data.
function insertData() {
  var count = document.getElementById('count').value;
  var weight = document.getElementById('weight').value;
  var today = new Date();
  var dd = today.getDate();
  var mm = today.getMonth()+1; //January is 0!
  var yyyy = today.getFullYear();
  var hour = today.getHours();
  var minute = today.getMinutes();
  var second = today.getSeconds();
  if(dd<10){dd='0'+dd} if(mm<10){mm='0'+mm} if(hour<10){hour='0'+hour} if(minute<10){minute='0'+minute} if(second<10){second='0'+second}
  var date = yyyy + '-' + mm + '-' + dd + " " + hour + ":" + minute + ":" + second;
  var e = document.getElementById("sex");
  var f = document.getElementById("exerciseType");
  var exerciseType = f.options[f.selectedIndex].text;
  console.log("date: " + date);
  console.log("exerciseType: " + exerciseType);
  var insert = [];
  insert.push('INSERT INTO ');
  insert.push(exerciseTableId);
  insert.push(' (username, age, sex, exercise, goal_exercise, goal_count, goal_weight, exercise_count, exercise_weight, email, date) VALUES (');
  insert.push("'" + user + "', ");
  insert.push("'" + age + "', ");
  insert.push("'" + sex + "', ");
  insert.push("'" + exerciseType + "', ");
  insert.push("'" + exerciseGoal + "', ");
  insert.push(countGoal + ", ");
  insert.push(weightGoal + ", ");
  insert.push(count + ", ");
  insert.push(weight + ", ");
  insert.push("'" + email + "', ");
  insert.push("'" + date + "'");
  insert.push(')');
  console.log(insert.join(''));
  query(insert.join(''), "exercise");
}

function insertGoalData() {
  var name = "kate";
  var count = "40";
  var weight = "35";
  // var e = "";
  var exerciseType = "curl";
  var today = new Date();
  var dd = today.getDate();
  var mm = today.getMonth()+1; //January is 0!
  var yyyy = today.getFullYear();
  var hour = today.getHours();
  var minute = today.getMinutes();
  var second = today.getSeconds();
  exerciseGoal = name;
  countGoal = count;
  weightGoal = weight;
  console.log("exercise: " + exerciseGoal);
  console.log("count:" + countGoal);
  console.log("weight:" + weightGoal);
  if(dd<10){dd='0'+dd} if(mm<10){mm='0'+mm} if(hour<10){hour='0'+hour} if(minute<10){minute='0'+minute} if(second<10){second='0'+second}
  var date = yyyy + '-' + mm + '-' + dd + " " + hour + ":" + minute + ":" + second;
  var insert = [];
  insert.push('INSERT INTO ');
  insert.push(goalTableId);
  insert.push(' (username, exercise, count, weight, date) VALUES (');
  insert.push("'" + name + "', ");
  insert.push("'" + exerciseType + "', ");
  insert.push(count + ", ");
  insert.push(weight + ", ");
  insert.push("'" + date + "'");
  insert.push(')');
  console.log(insert.join(''));

  query(insert.join(''), "goal");
  // var body = 'sql=' + encodeURIComponent(insert.join(''));
  // $.ajax({
  //     type: "POST",
  //     url: 'https://www.googleapis.com/fusiontables/v1/query',
  //     data: {
  //             "sql": encodeURIComponent(insert.join('')),
  //     },
  //     beforeSend: function(xhrObj){
  //               xhrObj.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
  //     },
  //     success: function(data){
  //         console.log("Successfully addNewGoal");
  //         console.log(data);
  //     }
  // });
  
}

// Run a request to SELECT data.
function selectData() {
  query('SELECT * FROM ' + exerciseTableId, "exercise");
}

// Run a request to SELECT data.
function selectGoalData() {
  // console.log("user: " + user);
  query('SELECT * FROM ' + goalTableId + " WHERE username='" + username + "'", "goal"); 

}

// Send an SQL query to Fusion Tables.
function query(query, table) {
  var lowerCaseQuery = query.toLowerCase();
  var path = '/fusiontables/v1/query';
  var callback = function(element) {
    return function(resp) {
      var output = JSON.stringify(resp);
      // document.getElementById(element).innerHTML = output;
      // console.log("element: "+element);
      getAllGoals();
      if (element=="select-data-output-goal") {
        console.log("in if");
        // getAllGoals();
      }
    };
  }
  if (lowerCaseQuery.indexOf('select') != 0 &&
      lowerCaseQuery.indexOf('show') != 0 &&
      lowerCaseQuery.indexOf('describe') != 0) {

    var body = 'sql=' + encodeURIComponent(query);
    if (table == "exercise") {
        runClientRequest({
          path: path,
          body: body,
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': body.length
          },
          method: 'POST'
        }, callback('insert-data-output'));
    }
    else {
      runClientRequest({
          path: path,
          body: body,
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': body.length
          },
          method: 'POST'
        }, callback('insert-data-output-goal'));
    }

  } else {
    if (table == "exercise") {
        runClientRequest({
          path: path,
          params: { 'sql': query }
        }, callback('select-data-output'));
    }
    else {
       runClientRequest({
          path: path,
          params: { 'sql': query }
        }, callback('select-data-output-goal'));
    } 
  }
}

// Execute the client request.
function runClientRequest(request, callback) {
  var restRequest = gapi.client.request(request);
  restRequest.execute(callback);
}


  


