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
            labelrow.classList.add("row")
            labelrow.classList.add("sidebar-label")
            document.getElementById('leftcol').appendChild(labelrow);
        }
        
        if (sidebarArray[i][0]=="SEARCH"){
            add_search_box(); 
        }

        if (sidebarArray[i][0]=="SPACE"){
            var labelrow = document.createElement("div");
            labelrow.innerHTML = "<br/>";     
            labelrow.classList.add("row")
            document.getElementById('leftcol').appendChild(labelrow);
        }

        if (sidebarArray[i][0]=="SPACE"){
            var labelrow = document.createElement("div");
            labelrow.innerHTML = "<br/>"; 
            labelrow.classList.add("row")    
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
    <div class="row" id="searchrow">
        <form action="/search" method="post">
                <input id="search-box-text" name="searchTerm" type="text" class="form-control input autocomplete_terms" placeholder="SEARCH" ></input>
                <input type="hidden" name="clickedButton" id="clickedButton" value="` + clickedButtonKey  + `"></input>
        </form>
    </div>
      `;
    document.getElementById('leftcol').appendChild(newrow);
}

function create_btn_group(){
    var buttondiv = document.createElement("div")
    buttondiv.classList.add("row")
    buttondiv.id = "btnrow"
    document.getElementById('leftcol').appendChild(buttondiv);

    var buttonGroupDiv = document.createElement("div");
    buttonGroupDiv.classList.add("btn-group-vertical");
    buttonGroupDiv.classList.add("btn-block");
    buttonGroupDiv.role = "group";
    buttonGroupDiv.id = "btn-group";
    
    document.getElementById('btnrow').appendChild(buttonGroupDiv);

}