//  using this as template for sliding panels:
//  http://plnkr.co/edit/GGQLn519tPCrqjwHER4W?p=preview

$(document).ready(function () {


    //open progress panel
    // Click handler
    $('#open-progress').on('click', function () {

        // State checker
        if ($("#feedback").attr('data-state') === 'neutral') {
            $("#feedback").attr('data-state', 'slide-right')
            console.log('slide-right');
        } 
        else {
            $("#feedback").attr('data-state', 'neutral')
        }
    });

    $('#social-button-wrapper').on('click', function () {

        // State checker
        if ($("#feedback").attr('data-state') === 'neutral') {
            $("#feedback").attr('data-state', 'slide-left')
        } 
        else {
            $("#feedback").attr('data-state', 'neutral')
        }
    });
    $("#social-button-wrapper").hover(function(){
        
    });

});
