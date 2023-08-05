function create_boxplot(figureInfo, dataArray, divid){
    
        if (dataArray==null){ 
            empty_figure(figureInfo, divid);
            return;
        }
        
        factorMat = figureInfo["paramList"];
      
        //Calculate mean, sd, labels, 
        xList = [];
        yList = [];
        var labelList = [];
        var colorList = [];
        xloc=0;
        var yData = [];
    
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
                xList.push(xloc);
                yData.push(data)
                colorList.push(factorMat[i][4]);
                xloc +=1
            }
        }
     


        var data = [];
        for (var i = 0; i< yData.length; i++){
            var result = {
                type: 'box',
                y: yData[i], 
                name: labelList[i],
                marker:{
                    size: figureInfo["markersize"],
                }
            };
            if (figureInfo["showpoints"]=="TRUE") { 
                result["boxpoints"] = "all";
            }
            else {
                result["boxpoints"] = "none";
            }
            data.push(result);
        };
 
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
      xaxis: {
        tickvals: xList,
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
    
    
    