function create_sidebar(defaultButtonKey, defaultTerm){
    //defaultButtonKey variable sets which button is initially labeled as active.
    document.getElementById('leftcol').innerHTML = '';    // First clear out the layout. 
    /*
    var termrow = document.createElement("div");
    termrow.id = "search-term";
    termrow.innerHTML = defaultTerm + "<br/><br/>";
    termrow.style="font-size:25px; font-weight:bold;"
    document.getElementById('leftcol').appendChild(termrow);
    */
    var start = "TRUE";
    console.log("sidebarJson:", sidebarJson);
    sidebarArray = sidebarJson["paramList"]
    for (i in sidebarArray){

        if (sidebarArray[i][0]=="LABEL"){
            var labelrow = document.createElement("div");
            labelrow.innerHTML = sidebarArray[i][1];     
            document.getElementById('leftcol').appendChild(labelrow);
        }
        
        if (sidebarArray[i][0]=="SEARCH"){
            add_search_box(); 
        }

        if (sidebarArray[i][0]=="SPACE"){
            var labelrow = document.createElement("div");
            labelrow.innerHTML = "<br/>";     
            document.getElementById('leftcol').appendChild(labelrow);
        }

        if (sidebarArray[i][0]=="SPACE"){
            var labelrow = document.createElement("div");
            labelrow.innerHTML = "<br/>";     
            document.getElementById('leftcol').appendChild(labelrow);
        }

        if (sidebarArray[i][0]=="PANEL" && start=="TRUE"){
            create_btn_group()
            start = "FALSE";
        }

        if (sidebarArray[i][0]=="PANEL"){
            buttonkey = sidebarArray[i][2]
            buttonname = sidebarArray[i][1]
            var active = "False";
            if (buttonkey == defaultButtonKey) active= "True";
            create_button(buttonkey, buttonname, active);
        }
    }
}
 
 function create_button(buttonkey, buttonname, active){
    var newbutton = document.createElement("button");
    newbutton.name = buttonkey;
    newbutton.type = "button";
    newbutton.className = "btn btn-default";
    newbutton.innerHTML = buttonname;
    if (active=="True") newbutton.className = "btn btn-default active"
    document.getElementById('btn-group').appendChild(newbutton);
}

function add_search_box(){
    var newrow = document.createElement("div");
    newrow.innerHTML= `
        <form action="/search" method="post">
            <div class="side-bar-search-box">
                <input name="searchTerm" type="text" class="form-control input autocomplete_terms" placeholder="Search..." ></input>
                <input type="hidden" name="clickedButton" id="clickedButton" value="` + clickedButtonKey  + `"></input>
            </div>
        </form>`;
    document.getElementById('leftcol').appendChild(newrow);
}

function create_btn_group(){
    var buttonGroupDiv = document.createElement("div");
    buttonGroupDiv.className = "btn-group-vertical btn-block";
    buttonGroupDiv.role = "group";
    buttonGroupDiv.id = "btn-group";
    document.getElementById('leftcol').appendChild(buttonGroupDiv);
}