$(document).ready(function () {

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
    $("#modal-window h1").text("Goal "+ goalArrayAddone);


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
        $("#modal-window").show();
    });
    $("#modal-overlay").on('click', function(){
        $("#modal-overlay").hide();
        $("#modal-window").hide();
    });
    $("#modal-add-goal").submit(function(e){
        $("#modal-overlay").hide();
        $("#modal-window").hide();

        // TODO: update database & refresh this page to show new goal list

        e.preventDefault();
    });


    /* Activity */
    /************************************************************************/

    // TODO: Get activity freq from database
    var activityArray = [0,1,2,0,0,1,1,3,3,2,0,0,0,0,0];
    // var activityArray = [0,0,0,0,0,0,0, 0,0,0,0,0,0,0, 0,0,0,0,0,0,0, 0,0,0,0,0,0,0, 0,0];

    for (var i=1; i<activityArray.length+1; i++) {
        var code = '<div class="code" id="code-'+i+'"></div>';
        $("#activity-map").append(code);
        $("#code-"+i).addClass("level-"+activityArray[i-1]);
    }
    

});
































