//I DON"T THINK THIS IS USED ANYMORE!!!!
//
//
// [START] fill_in_page 
function fill_in_page(){
        var imgSrc = $('.active.btn').data('img');
        var metaData = $('.active.btn').data('dict');
        console.log(imgSrc);
        $('#figure').html('<img id="figure_img" src="'+imgSrc+'" width="95%" class="img-responsive" alt="Generic placeholder thumbnail">');
        $('.active.btn').disabled= true; // Make the active button unclickable
        $('#infoText').html("<div class=\"row\"><strong>" + metaData['setNameLong'] +  "</strong></div> <div class=\"row\"> " +  metaData['info'] + " </div>");  
        $('#citationText').html(metaData['citation']);  
}
// [END] fill_in_page


// [START] main load function - Run once everything is loaded. 
$(function(){
    $('.btn').click(  function(){

        $('.active.btn').removeClass('active');
        setkey = $(this).data('setkey');
        $(".btn[data-setkey='" + setkey +"']").addClass('active');
//        $(this).addClass('active'); // We changed this to accomodate new buttons. 
//
// Mark which button was clicked so that when a new gene is searched, it doesn't change to a new page. 
        $('input[name=clickedButton]').val(setkey) ;
        fill_in_page();    
    });
    fill_in_page()
   
    // Fill in the button name 
    $('.btn').each( function(){
    var metaData = $(this).data('dict');
    $(this).html(metaData['buttonName']);
    $(this).hide();  // HIDE FOR SINGLE USE
    });
    window_resize();
    $(document).ready(function() { //Once page is loaded show the hidden elements
        $(".hidden").removeClass("hidden");
    });
});
// [END] first load function
//
//
function window_resize(){
  if ($(window).width() < 500) {
    $('#rightcol').hide();
    $('#leftcol').removeClass('col-xs-10');
    $('#leftcol').addClass('col-xs-12');
    $('#search-top').show();
    $('#figcol').removeClass('col-xs-10');
  } else {
    $('#rightcol').show();
    $('#leftcol').removeClass('col-xs-12');
    $('#leftcol').addClass('col-xs-10');
    $('#search-top').hide();
  }
}

$(window).resize(function() {
window_resize();
});
