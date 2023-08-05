function create_violin_old(figureInfo, dataArray, divid){

    // There are problems when calculating the violin span here. 
    // Perhaps this is because there are too many 0's? 
    // One way to solve this is to randomly choose small numbers for the 0's. 
    // I think this may work, if we create a new trace for each value. 
    
    
        if (dataArray==null){ 
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
                    b:bottommargin,
                    r:50,
                    t:20,
                }
            };
            if (figureInfo["title"]!="None"){
                layout.title = figureInfo["title"];
                layout.titlefont = {family: 'Helvetica', size:18};
                }
            Plotly.newPlot(divid, [trace],layout, {displayModeBar: false} );
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
            subobj.line = {color: 'blue'};
            groupobj.value = subobj;
            styleList.push(groupobj);
        }
        
        /* Adding a fix to get rid of the values that are near 0. */
        for (i in yList){
            if (yList[i]==0){
                yList[i] = Math.random()/10.0  - 0.05
        }
        }
    
        var data = [{
            type: 'violin',
            x: xList,
            y: yList,
            points: 'all',
            pointpos: 0,
            marker: {
                color: 'black',
                size:1,
            },
            box: {
                visible: false,
            },
            span: [0],
            meanline: {
                visible: true
            },
            transforms: [{
                type: 'groupby',
                groups: xList,
                styles: styleList,
                }]
            }]
    
            var maxlabellength = d3.max(labelList, x => x.length);
            var bottommargin = d3.max([maxlabellength*8,100]);
    
    var layout = {
      yaxis: {
        zeroline: false
      },
      violingap: 0,
      violingroupgap: 0,
      boxgap: 0,
      boxgroupgap: 0,
      violinmode: "overlay",
      xaxis: {
        tickvals: labelXList,
        ticktext: labelList,
        tickangle:90,
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
    
        Plotly.plot(divid, data, layout);
    };
    
    
    
    