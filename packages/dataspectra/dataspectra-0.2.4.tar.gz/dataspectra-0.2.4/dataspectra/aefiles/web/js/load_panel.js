$(function () {
    // NOTE: USES GLOBALS
    defaultButtonKey = siteJson["defaultpanel"];


    create_sidebar(defaultButtonKey, searchTerm);
    update_layout(defaultButtonKey);


    $('.btn').click(function () {
        //Delete anything old
       // d3.select("svg").remove(); 
        // d3.select(".d3-tip").remove(); 

        // Activate button
        $('.active.btn').removeClass('active');
        btnKey = $(this).attr("name");
        $(this).addClass('active');

        update_layout(btnKey);
    })
});

function update_layout(btnKey){
    layout = panelJson[btnKey]["paramList"];
    create_figure_layout(layout, figureJson, dataJson)
    
    // Mark which button was clicked so that when a new gene is searched, it doesn't change to a new page. 
   // $('input[name=clickedButton]').val(btnKey) ;
    //clickedButtonKey = btnKey;

    //  Update tabs
    $('#infoText').html("<div class=\"row\"><strong>" + panelJson[btnKey]["setname"] +  
        "</strong></div> <div class=\"row\"> " +  panelJson[btnKey]["info"] + " </div>");  
    $('#citationText').html(panelJson[btnKey]["citetext"]);  
    $('#downloadData').html("");
    create_download_tabs(btnKey)
}


function window_resize(){
    if ($(window).width() < 500) {
        $(".mobile").show();
        $(".full").hide();

    } else{
        $(".mobile").hide();
        $(".full").show();
    }
}

$(window).resize(function() {                                                                                                     
window_resize();
console.log(plotly_divs);
for (i in plotly_divs){
    Plotly.Plots.resize(plotly_divs[i]);
}
});

