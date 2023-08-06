// I DON'T THINK THIS IS USED ANYMORE!!!

//https://stackoverflow.com/questions/17377973/javascript-or-jquery-change-different-images-on-different-button-clicks
//https://stackoverflow.com/questions/13423646/using-jquery-with-jinja2-to-provide-onclick-event-inside-a-loop-on-each-element
$(function(){
        
//On click, remove the active class from whatever has it, and activate the new class
//#navlinks - 
        $('a#navlinks').click( function(e){ 
                //Remove the active class from whatever has it.  
                $(".active, .navbarClass").removeClass("active");
                var imgKey = $(this).data('key');
                e.preventDefault();
                $('#' + imgKey).addClass("active");
                var imgSRC = $('.active.navbarClass').data('src');
                var metaJson = $('.active.navbarClass').data('json');
                if (imgSRC =="NA"){
                    $('#buttonimage').html('<p> No data found </p>') ;
                } else {
                    $('#buttonimage').html('<img id="dataimg" src="'+imgSRC+'" width="1000" height="1000" class="img-responsive" alt="Generic placeholder thumbnail">'); 
                }
                
                $('#datasetHeader').html(metaJson['name']); 
                $('#citation').html(metaJson['citation']);
                $('#datasetNotes').html(metaJson['note']);

                //Set default in navTabs
                $('#notesTab').addClass("active");

        });

// Run the first time this is loaded. 
       var imgSRC = $('.active.navbarClass').data('src');
       var metaJson = $('.active.navbarClass').data('json');
       if (imgSRC =="NA"){
           $('#buttonimage').html('<p> No data found </p>') ;
       } else {
           $('#buttonimage').html('<img id="dataimg" src="'+imgSRC+'" width="1000" height="1000" class="img-responsive" alt="Generic placeholder thumbnail">'); 
       }
        // Put this information in as tabs. 
        $('#datasetHeader').html(metaJson['name']);
        $('#citation').html(metaJson['citation']);
        $('#datasetNotes').html(metaJson['note']);
});




