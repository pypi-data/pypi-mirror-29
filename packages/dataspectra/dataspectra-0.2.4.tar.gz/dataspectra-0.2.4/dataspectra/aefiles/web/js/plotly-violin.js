function create_violin(figureInfo, dataArray, divid){

// There are problems when calculating the violin span here. 
// Perhaps this is because there are too many 0's? 
// One way to solve this is to randomly choose small numbers for the 0's. 
// I think this may work, if we create a new trace for each value. 

    if (dataArray==null){ 
        empty_figure(figureInfo, divid);
        return;
    }
    
    factorMat = figureInfo["paramList"];
  
    //Calculate mean, sd, labels, 
    xList = [];
    yList = [];
    labelList = [];
    colorList = [];
    xloc=0;
    labelXList = [];
    
    console.log(factorMat);

    for (i in factorMat){
        rowtype = factorMat[i][0];
        if (rowtype=="SPACE"){
            xloc +=1;
        }
        if (rowtype=="BAR"){
            cols = factorMat[i][2];
            colArray = cols.split("$");
            data = colArray.map(x => Number(dataArray[Number(x) - 1]));
            labelList.push(factorMat[i][1]);
            labelXList.push(xloc);
            yList = yList.concat(data);
            var xvals = data.map(i => xloc);
            xList = xList.concat(xvals);  
            colorList.push(factorMat[i][4]);
            xloc +=1
        }
    }
 

    styleList = [];
    for (i in labelList){
        var groupobj = {};
        groupobj.target = i;
        var subobj = {};
        subobj.line = {color: colorList[i]};
        groupobj.value = subobj;
        styleList.push(groupobj);
    }
    
    /* Adding a fix to get rid of the values that are near 0. */
    for (i in yList){
        if (yList[i]==0){
            yList[i] = Math.random()/10.0 
    }
    }




    var trace1 = {
        type: 'violin',
        x: xList,
        y: yList,
        points: 'all',
        pointpos: 0,
        marker: {
            color: 'black',
            size:figureInfo["markersize"],
        },
        box: {
            visible: false,
        },
        spanmode: 'hard',
        bandwidth: 1,
        meanline: {
            visible: true
        },
        transforms: [{
            type: 'groupby',
            groups: xList,
            styles: styleList,
            }]
        }
    if (figureInfo["showpoints"]=="TRUE") { 
        trace1["points"] = "all";
    }
    else {
        trace1["points"] = "none";
    }
    var data = [trace1];

        var maxlabellength = d3.max(labelList, x => x.length);

        if (figureInfo["xtickangle"] > 30) {
            var bottommargin = d3.max([maxlabellength*8,100]);
        }
        else {
            var bottommargin = 50;
        }

var layout = {
  yaxis: {
    zeroline: false,
    title: figureInfo["valuelabel"],
    titlefont: {family: 'Helvetica', size:18},
  },
  violingap: 0,
  violingroupgap: 0,
  boxgap: 0,
  boxgroupgap: 0,
  violinmode: "overlay",
  xaxis: {
    tickvals: labelXList,
    ticktext: labelList,
    tickangle:figureInfo["xtickangle"],
    tickfont: {family:'Helvetica', size:figureInfo["xtickfontsize"]}
}, 
  showlegend: false,
  margin: {
    l:50,
    b:bottommargin,
    r:50,
    t:50,
}
}


if (figureInfo["title"]!="None"){
    layout.title = figureInfo["title"];
    layout.titlefont = {family: 'Helvetica', size:18};
    };

    Plotly.plot(divid, data, layout, {displayModeBar: false});
};



