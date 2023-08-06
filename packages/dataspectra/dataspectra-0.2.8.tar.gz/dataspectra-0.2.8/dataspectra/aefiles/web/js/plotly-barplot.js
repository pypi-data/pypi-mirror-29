// Activate defaults by 
//



function create_plotly_barplot(figureInfo, dataArray, divid){

    //defaults for barplot
    if ('xtickfontsize' in figureInfo){
        xtickfontsize = figureInfo['xtickfontsize'];
    }
    else {
        xtickfontsize = 18;
    }
    if ('xtickangle' in figureInfo){
        xtickangle = figureInfo['xtickangle'];
    }
    else {
        xtickangle = 0;
    }


    if ('valuelabel' in figureInfo){
        valuelabel = figureInfo['valuelabel']
    }
    else {
        valuelabel = "";
    }
    if ('title' in figureInfo){
        figuretitle = figureInfo['title'];
    }
    else {
        figuretitle = "None";
    }

    console.log(figureInfo, dataArray, divid);


    //If tick angle is specified - then add a tick angle info. 
    if (dataArray==null){ 
       console.log("Empty Data Array found for barplot", figureInfo, dataArray)
       empty_figure(figureInfo, divid);
       return;
    }
    
    factorMat = figureInfo["paramList"];
    //Calculate mean, sd, labels, 
    xList = [];
    yList = [];
    errList = [];
    labelList = [];
    colorList = [];
    xloc=0;
    for (i in factorMat){
        rowtype = factorMat[i][0];
        if (rowtype=="SPACE"){
            xloc +=1;
        }
        if (rowtype=="BAR"){
            cols = factorMat[i][2];
            colArray = cols.split("$");
            data = colArray.map(x => Number(dataArray[Number(x) - 1]));
            mean = d3.mean(data);
            sd = d3.deviation(data);
            labelList.push(factorMat[i][1]);
            yList.push(mean);
            xList.push(xloc);
            errList.push(sd/Math.sqrt(colArray.length)); //Standard error of the mean. 
            colorList.push(factorMat[i][4]);
            xloc +=1
        }
    }

    var trace1 = {
            x: xList,
            y: yList,
            type: 'bar',
            error_y: {
                type: 'data',
                array: errList,
                visible: true
            },
            marker: {
                color: colorList
            }
    };

    var data = [trace1];

    var maxlabellength = d3.max(labelList, x => x.length);
    if (xtickangle > 30) {
        var bottommargin = d3.max([maxlabellength*8,100]);
    }
    else {
        var bottommargin = 50;
    }
    var layout={
        xaxis: {
            tickvals: xList,
            ticktext: labelList,
            tickangle:xtickangle,
            tickfont: {family:'Helvetica', size:xtickfontsize}
            
        }, 
        yaxis: {
                fixedrange: true,
                title: valuelabel,
                titlefont: {family: 'Helvetica', size:18},
            },
        margin: {
            l:50,
            b:bottommargin,
            r:50,
            t:50,
        },
        font:{
            color: selectedTheme["font_color"],
        },
        paper_bgcolor: selectedTheme["paper_bgcolor"],
        plot_bgcolor: selectedTheme["plot_bgcolor"],
    };

    if (figuretitle!="None"){
        layout.title = figuretitle;
        layout.titlefont = {family: 'Helvetica', size:18};
        };
    Plotly.newPlot(divid, data, layout, {displayModeBar: false});
}
