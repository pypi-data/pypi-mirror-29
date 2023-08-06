function create_mdscatter(figureInfo, dataArray, divid){

/* Creates a color dimensional scatter plot. 

dataArray1 [x values]
dataArray2 [y values]
dataArray3 [color values]

//Positions of the x and the y values are determined by the. 

*/
figurekey = figureInfo["figurekey"]
for (i in figureInfo["paramList"]){
    if (figureInfo["paramList"][i][3]!="data"){
        metaTerm = figureInfo["paramList"][i][3].split("meta.")[1];
        metaDictKey = figureInfo["metakey"].concat(".", metaTerm);
        data = metaDataDict[metaDictKey];
    }
    else{
        data = dataArray;
    }
    if (data==null){
        empty_plot(figureInfo, divid)
        return;
    }
    cols = figureInfo["paramList"][i][2].split("$")
    datavals = cols.map(i => data[Number(i)-1])
    if (figureInfo["paramList"][i][0] == "SCATTERX"){
        var xval = datavals
    }
    if (figureInfo["paramList"][i][0] == "SCATTERY"){
        var yval = datavals
    }
    if (figureInfo["paramList"][i][0] == "SCATTERZ"){
        var zval = datavals
    }
}


//var colorVal = colnum.map(i => dataArray[i]);
var colorVal = zval;
var trace1 = {
    x: xval,
    y: yval,
    type: 'scatter',
    mode: 'markers',
    marker: {
      colorscale: 'Reds',
      size: 3,
      color: colorVal,
      colorbar:{
          thickness:10,
        title: figureInfo["valuelab"],
      }
    },

  };
  
  var data = [trace1];

  var layout = {
    margin: {
        l:0,
        b:0,
        r:0,
        t:0,
    }
  };
  
  Plotly.newPlot(divid, data, layout, {displayModeBar: false});


    
}


function empty_plot(figureInfo, divid){

    var trace = {
        x:[1],
        y:[1],
        mode: 'text',
        text: ["No data found"],
        textposition: 'bottom'
    };
    
    var layout={
  
        font: {size:18},
        xaxis: { showticklabels: false, ticks:'', fixedrange: true }, 
        yaxis: { showticklabels: false, ticks: '', fixedrange: true },
        margin: {
            l:50,
            b:50,
            r:50,
            t:50,
        }
    };
    if (figureInfo["title"]!="None"){
        layout.title = figureInfo["title"];
        layout.titlefont = {family: 'Helvetica', size:18};
        }
    Plotly.newPlot(divid, [trace],layout, {displayModeBar: false} );
    return;
}