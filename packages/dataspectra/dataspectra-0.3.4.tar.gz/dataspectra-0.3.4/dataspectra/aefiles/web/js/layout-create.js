/* 
create_figure_layout - takes in the button names. 


Because the plotly creates a plot-container that fills up the entire div. 
Unable to reduce the size of the plot-container, so instead will be putting a div inside of a div. 

#Working on setting an aspect ratio from the start. 
#The problem is trying to make it responsive at the same time. 
# Currently, responsiveness is set by setting only the height. When the window size is changed, 
the width will change. Then, the plotly.resize command is sent. 
#  To preserve the aspect ratio, we will need to know what the height should be given the current
window size. 
    #So, first, calculate current window size and the respective widths of the windows. 
    #Then, set the subdiv to be correct size given 
    #Then, 
*/


var plotly_divs = [];
var figureObjects = [];


function create_figure_layout(layout, figureJson, dataJson){
    
    // Create rows while gathering info about the columns.
    plotly_divs = [];  

    
    //console.log(layout)
    document.getElementById('rightcol').innerHTML = '';    // First clear out the layout.

    var rowcolinfo = fill_in_rowcolinfo(layout);
    figureObjects = create_figure_objects(layout);
    var rowObjects = create_row_objects(layout);
    figureObjects = update_figure_objects_positioning(figureObjects, rowObjects);
    
    // Create columns
    for (rowid in rowcolinfo){
        parentRow = document.getElementById(rowid);
        for (colid in rowcolinfo[rowid]){
            var newcol = document.createElement("div");
            newcol.id = rowcolinfo[rowid][colid]["figure"]
            newcol.className = "col-xs-" + rowcolinfo[rowid][colid]["width"];
            //newcol.style.width = rowcolinfo[rowid][colid]["width"]  + "%";
            newcol.style.height = rowcolinfo[rowid][colid]["height"] + "px";
            //newcol.style.float = "left";
            //newcol.style.backgroundColor = "red";
            parentRow.appendChild(newcol);
        }
    }
    
    // Fill in the figures
    //console.log(rowcolinfo);
    for (rowid in rowcolinfo){
        for (colid in rowcolinfo[rowid]){
            figureKey = rowcolinfo[rowid][colid]["figure"];
            //console.log(figureKey);
            divid = figureKey;
            if (figureKey=="breaker"){
                create_spacer(divid);
            }
            else {
                figureMatch = figureJson[figureKey];
                //console.log("match", figureMatch, figureKey);
                dataArray = dataJson[figureJson[figureKey]["datasetkey"]];
                if (figureMatch["figuretype"]=="barplot"){
                    //Create new plotly subdiv
                    var subdiv = create_subdiv(divid, figureObjects, figureKey)
                    create_plotly_barplot(figureMatch, dataArray, subdiv, figureObjects[figureKey]);
                    plotly_divs.push(subdiv);
                    update_borders(divid, figureObjects, figureKey)   
            
                }
                if (figureMatch["figuretype"]=="title"){
                    create_title(figureMatch, dataArray, divid);
                    
                }
                if (figureMatch["figuretype"]=="density"){
                    var subdiv = create_subdiv(divid, figureObjects, figureKey)

                    create_density(figureMatch, dataArray, divid);  
                    plotly_divs.push(subdiv);              
                    update_borders(divid, figureObjects, figureKey)   

                }
                if (figureMatch["figuretype"]=="carousel"){
                    var subdiv = create_subdiv(divid, figureObjects, figureKey)
                    create_carousel(figureMatch, subdiv);
                    update_borders(divid, figureObjects, figureKey)   

                }
                if (figureMatch["figuretype"]=="mdscatter"){
                    var subdiv = create_subdiv(divid, figureObjects, figureKey)
                    create_mdscatter(figureMatch, dataArray, subdiv);
                    plotly_divs.push(subdiv);
                    update_borders(divid, figureObjects, figureKey)   

                }
                if (figureMatch["figuretype"]=="violin"){
                    var subdiv = create_subdiv(divid, figureObjects, figureKey)
                    create_violin(figureMatch, dataArray, subdiv);
                    plotly_divs.push(subdiv);
                    update_borders(divid, figureObjects, figureKey)   

                }
                if (figureMatch["figuretype"]=="boxplot"){
                    var subdiv = create_subdiv(divid, figureObjects, figureKey)
                    create_boxplot(figureMatch, dataArray, subdiv);
                    plotly_divs.push(subdiv);
                    update_borders(divid, figureObjects, figureKey)   
                }
            }
        }
    }

    // Add the tabs. 
    add_tabs()
}

function create_subdiv(divid, figureObjects, figureKey){
//Set the width and the height:
// If it is in 

    var subdiv = document.createElement("div");
    subdiv.className = "subdiv";
    subdiv.id = divid +"sub";
    if (figureObjects[figureKey]["aspectRatio"]=="NA"){
        subdiv.style.height = figureObjects[figureKey]["height"]-20 + "px";
    }
    currentWidth = $('#' + divid ).width();
    if (figureObjects[figureKey]["height"]=="NA"){
        subdiv.style.height = Number(figureObjects[figureKey]["aspectRatio"]) * currentWidth +"px";
    }
    document.getElementById(divid).appendChild(subdiv);
    return subdiv.id
}

function update_borders(divid, figureObjects, figureKey){
    element = document.getElementById(divid);
    element.classList.add("plot");
    if (figureObjects[figureKey]["leftmost"]==true){
        element.style.borderLeft = "0px";
    }
    if (figureObjects[figureKey]["rightmost"]==true){
        element.style.borderRight= "0px";
    }
}

function add_tabs(){
    var newrow = document.createElement("div");
    newrow.innerHTML = `
    <!-- [START] Tabs  -->
    <!-- Nav tabs -->
    <div class="row tab-tabs" id="panel-tabs"> 
        <ul class="nav nav-tabs" role="tablist">
            <li role="presentation" id="notesTab" class="active navtabClass"><a class="navtabtext" href="#infoText
    " aria-controls="datasetNotes" role="tab" data-toggle="tab">INFO</a></li>
            <li role="presentation" class="navtabClass"><a class="navtabtext" href="#citationText" aria-controls="citation" role="tab" data-toggle="tab">CITATION</a></li>
            <li role="presentation" class="navtabClass"><a class="navtabtext" href="#downloadData" aria-controls="citation" role="tab" data-toggle="tab">DOWNLOAD</a></li>
        </ul>
    </div>

    <!-- Tab panes -->
    <div class="row tab-text" id="panel-tabs-text">
        <div class="tab-content">
            <div role="tabpanel" class="tab-pane fade in active" id="infoText"></div>
            <div role="tabpanel" class="tab-pane fade" id="citationText"></div>
            <div role="tabpanel" class="tab-pane fade" id="downloadData"></div>
        </div> <!-- tab-content -->
    </div>
<!-- [END] Tabs -->    
    `
    document.getElementById('rightcol').appendChild(newrow);

}


function fill_in_rowcolinfo(layout){
    var rowcolinfo = {};
    var currentRowId = "";
    for (i in layout){
        if (layout[i][0]=="FIGURE" || layout[i][0]=="TITLE" || layout[i][0]=="BREAKER"){
            figureKey = layout[i][1]
            rowNum = layout[i][4]
            colNum = layout[i][5]
            colid = "col" + colNum;
            colWidth = layout[i][2]
            colHeight = layout[i][3]
            rowid = "row" + rowNum;    
            if (rowid!=currentRowId){
                var newrow = document.createElement("div");
                newrow.className = "row";
                newrow.id = rowid;
                rowcolinfo[rowid] = {};
                document.getElementById('rightcol').appendChild(newrow);
            }
            rowcolinfo[rowid][colid] = {}
            //rowcolinfo[rowid][colid]["width"] = colWidth;
            rowcolinfo[rowid][colid]["width"] = Math.round(Number(colWidth)/100*12);
            rowcolinfo[rowid][colid]["height"] = colHeight;
            rowcolinfo[rowid][colid]["figure"] = figureKey;
            
            currentRowId = rowid
        }
    }
    return rowcolinfo;
}

function create_figure_objects(layout){
    var figureObjects = {};
    for (i in layout){
        figureKey = layout[i][1];
        rowNum = layout[i][4];
        colNum = layout[i][5];
        colWidth = layout[i][2];
        colHAR = layout[i][3];
        if (colHAR[0]=="R"){
            console.log("ASPECT RATIO DETECTED");
            var aspectRatio = colHAR.split("(")[1].split(")")[0];
            var colHeight = "NA";
        }
        else{
            var colHeight = colHAR;
            var aspectRatio = "NA";
        }
        figureObject = {}
        figureObject["row"]  = rowNum;
        figureObject["col"]  = colNum;
        figureObject["width"]  = colWidth;
        figureObject["height"]  = colHeight;
        figureObject["aspectRatio"] = aspectRatio;
        figureObjects[figureKey]  = figureObject;
    }
    return figureObjects;
}

function create_row_objects(layout){
    var rowObjects = {};
    for (i in layout){
        figureKey = layout[i][1];
        rowNum = layout[i][4];
        colNum = layout[i][5];
        colWidth = layout[i][2];
        colHeight = layout[i][3];
        if (!(rowNum in rowObjects)){
            var rowObject = {};
            rowObject["numcols"] = 0;
            rowObject["colwlist"] = [];
            rowObjects[rowNum] = rowObject;
        }
        rowObjects[rowNum]["numcols"] +=1;
        rowObjects[rowNum]["colwlist"].push(colWidth);
    }
    return rowObjects;
}


function update_figure_objects_positioning(figureObjects, rowObjects){
// Adds the leftmost, rightmost flags. 
    for (figureKey in figureObjects){
        rowNum = figureObjects[figureKey]["row"];
        numcols = rowObjects[rowNum]["numcols"].toString();
        colNum = figureObjects[figureKey]["col"];
        if (colNum=="1"){
            figureObjects[figureKey]["leftmost"]= true;
        }
        else{
            figureObjects[figureKey]["leftmost"] = false;
        }
        if (colNum==numcols){
            figureObjects[figureKey]["rightmost"] = true;
        }
        else{
            figureObjects[figureKey]["rightmost"] = false;
        }
    }

    return figureObjects;

}
