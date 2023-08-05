/* 
create_figure_layout - takes in the button names. 

*/

// This now uses plotly
// We should initialize the layout before we do anything. 
// This is because we will need to read the whole file before 
var plotly_divs = [];


function create_figure_layout(layout, figureJson, dataJson){

    // Create rows while gathering info about the columns.
    plotly_divs = [];  
    var currentRowId = "";
    var rowcolinfo = {};
    //console.log(layout)
    document.getElementById('rightcol').innerHTML = '';    // First clear out the layout. 
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
                    create_plotly_barplot(figureMatch, dataArray, divid);
                    plotly_divs.push(divid);
                }
                if (figureMatch["figuretype"]=="title"){
                    create_title(figureMatch, dataArray, divid);
                }
                if (figureMatch["figuretype"]=="density"){
                    create_density(figureMatch, dataArray, divid);  
                    plotly_divs.push(divid);              
                }
                if (figureMatch["figuretype"]=="carousel"){
                    create_carousel(figureMatch, divid);
                }
                if (figureMatch["figuretype"]=="mdscatter"){
                    create_mdscatter(figureMatch, dataArray, divid);
                    plotly_divs.push(divid);
                }
                if (figureMatch["figuretype"]=="violin"){
                    create_violin(figureMatch, dataArray, divid);
                    plotly_divs.push(divid);
                }
                if (figureMatch["figuretype"]=="boxplot"){
                    create_boxplot(figureMatch, dataArray, divid);
                    plotly_divs.push(divid);
                }
            }
        }
    }
}



function create_d3_figure(figureKey, figureJson, dataJson) {
    
    d3.select(".figureSection")
    .append("svg")
    .attr("width", "400")
    .attr("height", "200")
    .attr("viewBox", "0 0 400 200")
    .attr("preserveAspectRatio", "xMinYMid");
    figureMatch = figureJson[figureKey];
    if (figureMatch["figuretype"] == "barplot") {
        create_barplot(figureMatch, dataJson);
    }
}