var badgeName = ["Newbie","Goal","33","44","55","66","77","88","99"];
var badgeDesc = ["Signed up for Hercubit!", "Set your first goal!","","","","","","",""];

$(document).ready(function () {

    /* If first time use */
    /************************************************************************/

    // TODO: set cookie to detect if it's first time use
    var firstTimeUse = 1;
    
    if ($("#username").val()!='') {
        $("header div.header-action").hide();
        $("#white-overlay").show();
        $("#signup-form").show();
    }

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
    var goalArray = ["10 curls", "10 curls + 10 pushups"];

    // Get goals from the database
    for (var i=1; i<goalArray.length+1; i++) {
        $("section.main div.card div#add-goal").before('<div class="goal lines clear" data-state="neutral" id="goal-'+i+'"><div class="num">Goal '+i+'</div><div class="desc">'+goalArray[i-1]+'</div><div class="edit"><img src="../static/img/edit.png"></div></div>');
    };
    // Set the number for new goal
    var goalArrayAddone = goalArray.length+1;
    $("#modal-goal h1").text("Goal "+ goalArrayAddone);


	// Hover goal to see edit button
	$("div.goal").hover(
		function() {
			$(this).children(".edit").attr('data-state', 'hover');
		},
		function() {
			$(this).children(".edit").attr('data-state', 'neutral');
		}
	);
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

        e.preventDefault();
    });


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
        $("section.social div.card").append('<div class="friend lines clear"><div class="num">'+i+'</div><div class="icon"><img src="../static/img/'+friendArray[i-1]+'.png"></div><div class="desc">'+friendDesc[i-1]+'</div><div class="menu"><button>Message</button><button>Challenge</button></div></div>');
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
}































