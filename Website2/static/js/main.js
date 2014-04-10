// Backend info
// var username = "kate";

var badgeName = ["Newbie","Goal","Strike3","Strike7","Five","Completion"];
var badgeDesc = ["Signed up for Hercubit!", "Set your first goal!","3-day Strike!","7-day Strike!","Five sessions!","Complete your first exercise!"];
var badgeArray = [0,0,0,0,0,0];

$(document).ready(function () {

    /* If first time use */
    var firstTimeUse = 1;

    if ($("#username").html()!='') {
        console.log('user already logged in as: '+ $("#username").text())
        firstTimeUse=false;
    }
    if (firstTimeUse) {
        $("#white-overlay").show();
        $("#signup-form").show();
        $("header div.header-action").hide();
    }


    $("#signup").submit(function(e){
        $("#white-overlay").hide();
        $("#signup-form").hide();
        $("header div.header-action").show();
        e.preventDefault();
        $("#username").text($("#username").text().toLowerCase());
        signup();
        
    });


    function signup(){
      $.post("./signup",
        $("#signup").serialize(),
        function(data){
            console.log('signup');
            console.log(data.new_user);
          if(data.new_user == false){
            window.location.href= "/";
          }
          else{
            getNewBadge(0);
          }
      
          return false;
        }
      )}

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
    updateGoals();

    /* Activity */
    /************************************************************************/
    // TODO: Get activity freq from database
    var activityArray = [0,1,2,0,3,2,1];

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

    for (var i=1; i<friendArray.length+1; i++) {
        $("section.social div.card").append('<div class="friend lines clear"><div class="num">'+i+'</div><div class="icon"><img src="../static/img/'+friendArray[i-1]+'.png"></div><div class="desc">'+friendDesc[i-1]+'</div><div class="menu"><button class="button-small">Message</button><button class="button-small">Challenge</button></div></div>');
    };

    /* Comment off for hiding the Message & Challenge buttons */
    // $("html").on("click", function(){
    //     $("div.friend").css("height", "80px");
    //     $("div.friend").find("div.menu").hide();
    // })
    // $("div.friend").on("click", function(e){
    //     e.stopPropagation();
    //     $("div.friend").css("height", "80px");
    //     $("div.friend").find("div.menu").hide();
    //     $(this).css("height","160px");
    //     $(this).find("div.menu").show();
    // });


    /* Achievements */
    // TODO: Loop through database to get badge list
    checkBadge();


});


function updateGoals() {
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
    
      $.post ("/deleteGoal",
        { id: $(this).parent()[0].id },
        // $("#modal-add-goal").serialize(),
        function(data) {
          console.log("delete goal");
          window.location.href = "/";
        }
      );
      // e.preventDefault();

  });
  // Click to choose the goal
  $("div.goal").on('click', function(){
      if (this.id!=="add-goal") {
          $("#chosen-goal span").html($(this).find('div.num').text() +": "+ $(this).find('div.desc').html())
          $("#startbtn").removeClass("disable");
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

      $.post ("/addGoal",
        $("#modal-add-goal").serialize(),
        function(data) {
          console.log("post addGoal");
          // TODO: FIX the disappearing modal window
          window.location.href = "/";
          getNewBadge(1);
        }
      );

      e.preventDefault();

  });
}

function checkBadge() {
  $.post("/checkBadge",
    function(data) {
      for (var i=1; i<7; i++) {
        badgeArray[i-1] = data['userInfo']['badge'+i];
      }
      updateBadge(); 
    }
  )
};

function updateBadge() {
  for (var i=1; i<7; i++) {
    // badge already get
    if (badgeArray[i-1]==1) { 
      $("#badge"+i+" img").attr("src","../static/img/"+badgeName[i-1]+".png");
    }
    else { 

    }
    $("#badge"+i).hover((function(i){
      return function(){
        $(".tooltip").html("<p>"+badgeName[i-1]+"</p><p>"+badgeDesc[i-1]+"</p>");
        $(".tooltip").css("top", $(this).position().top+20);
        $(".tooltip").css("left", $(this).position().left);
        $(".tooltip").show();
      }
    })(i),
    (function(i){
      return function(){
        $(".tooltip").hide();
      }
    })(i));
  }
}


function getNewBadge (badgeNum) {
  checkBadge();

  if (badgeArray[badgeNum]==0) {
    $("#modal-badge").find("h1").text(badgeName[badgeNum]);
    $("#modal-badge").find("img").attr("src","../static/img/"+badgeName[badgeNum]+".png");
    $("#modal-badge").find("span").text("You've " + badgeDesc[badgeNum]);
    $("#modal-overlay").show();
    $("#modal-badge").show();
    $("#modal-badge").addClass("animated bounceIn");

    insertBadge(badgeNum);
  }

    
}

function insertBadge(badgeNum) {
  badgeNum = badgeNum + 1;

  $.post("/insertBadge",
    { badgeNum: badgeNum },
    function(data) {
      checkBadge();
    }
  )
};

function forTooltip(i) {
  return function() {
    return badgeName[i-1];
  }
}


// window.onbeforeunload = confirmExit;
// function confirmExit() {
//     return "Please instead click 'Quit' in the top right to exit and allow the application to shutdown as well. Thank you.";
// }
