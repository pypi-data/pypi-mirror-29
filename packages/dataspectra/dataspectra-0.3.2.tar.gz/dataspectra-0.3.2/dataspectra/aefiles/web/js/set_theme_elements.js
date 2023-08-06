
var themeElements = {
    "dark": {
        "paper_bgcolor": "black",
        "plot_bgcolor": "black",
        "marker_color": "white",
        "font_color": "white",
        "title_color": "white",
        "css_link": "/css/result_page_dark.css"
    },
    "bootstrap": {
        "paper_bgcolor": "white",
        "plot_bgcolor": "white",
        "marker_color": "black",
        "font_color": "black",
        "css_link": "/css/result_page.css"
    },
    "light": {
        "paper_bgcolor": "white",
        "plot_bgcolor": "white",
        "marker_color": "black",
        "font_color":  "black",
        "css_link": "/css/result_page_light.css"
    }
}

var selectedTheme = {};


if (siteJson["theme"]=="dark"){
    console.log("Activating dark theme");
    $(".bootstrap").hide();
    $(".light").hide();
    selectedTheme = themeElements["dark"];
}

else if (siteJson["theme"]=="bootstrap") {
    console.log("Activating bootstrap theme");
    $(".dark").hide();
    $(".light").hide();
    selectedTheme = themeElements["bootstrap"]
}

else if (siteJson["theme"]=="light"){
    console.log("Activating light theme");
    $(".dark").hide();
    $(".bootstrap").hide();
    selectedTheme = themeElements["light"]
}


var link = document.createElement( "link" );
link.href = selectedTheme["css_link"];
link.type = "text/css";
link.rel = "stylesheet";
link.media = "screen,print";
document.getElementsByTagName( "head" )[0].appendChild( link );



