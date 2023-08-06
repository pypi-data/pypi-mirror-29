$(function () {
    // NOTE: USES GLOBALS
    defaultButtonKey = siteJson["defaultpanel"];
    if (clickedButtonKey != "None"){
        var activatedButtonKey = clickedButtonKey
    }
    else {
        var activatedButtonKey = defaultButtonKey;
    }
    create_sidebar(activatedButtonKey, searchTerm);
    update_layout(activatedButtonKey);


    $('.btn').click(function () {
        //Delete anything old
       // d3.select("svg").remove(); 
        // d3.select(".d3-tip").remove(); 

        // Activate button
        $('.active.btn').removeClass('active');
        btnKey = $(this).attr("name");
        $(this).addClass('active');
        $('input[name=clickedButton]').val(btnKey); // Mark which button was clicked so that when a new gene is searched, it doesn't change to a new page. 

        update_layout(btnKey);
    })

    window_resize()
});

function update_layout(btnKey){
    layout = panelJson[btnKey]["paramList"];
    create_figure_layout(layout, figureJson, dataJson)
    
    // Mark which button was clicked so that when a new gene is searched, it doesn't change to a new page. 
   // $('input[name=clickedButton]').val(btnKey) ;
    //clickedButtonKey = btnKey;

    //  Update tabs
    $('#infoText').html("<div id=\"navtabtextheader\" class=\"row\"><strong>" + panelJson[btnKey]["setname"] +  
        "</strong></div> <div class=\"row\"> " +  panelJson[btnKey]["info"] + " </div>");  
    $('#citationText').html(panelJson[btnKey]["citetext"]);  
    $('#downloadData').html("");
    create_download_tabs(btnKey);
}


function window_resize(){
    if ($(window).width() < 768) {
        $(".mobile").show();
        $(".full").hide();
        document.getElementById("rightcol").classList.remove("rightcol_full")
        document.getElementById("rightcol").classList.add("rightcol_mobile")

    } else{
        $(".mobile").hide();
        $(".full").show();
        document.getElementById("rightcol").classList.remove("rightcol_mobile")
        document.getElementById("rightcol").classList.add("rightcol_full")
       
    }
}

$(window).resize(function() {                                                                                                     
window_resize();
for (i in plotly_divs){
    subdivid = plotly_divs[i]
    figureKey = subdivid.split("sub")[0];
    currentWidth = $("#" + subdivid).width()
    document.getElementById(subdivid).style.height = Number(figureObjects[figureKey]["aspectRatio"]) * currentWidth +"px";

    Plotly.Plots.resize(subdivid);
}
});
