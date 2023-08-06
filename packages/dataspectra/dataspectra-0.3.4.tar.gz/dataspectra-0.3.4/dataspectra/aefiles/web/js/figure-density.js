function create_density(figureInfo, dataArray, divid){
    
    //densityDict is a global variable

    var geneCol = figureInfo["gene"];
    if (dataArray!=null){
        var geneName = dataArray[geneCol-1];
    }
    else {
        var geneName = "no match found"
    }
    
   if (dataArray==null){
        var trace = {
        x:[1],
        y:[1],
        mode: 'text',
        text: ["No data found"],
        textposition: 'bottom'
        };
    
        var layout={
            font: {size:10},
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
    
    var figurecolor = figureInfo["paramList"][0][4]
    var totalheight = $('#' + divid).height();

    var densityArray = densityDict[figureInfo["figurekey"]]["density"];
    var percentileArray = densityDict[figureInfo["figurekey"]]["percentile"];
    xvals = densityArray.map(x => Number(x[0]))
    yvals = densityArray.map(x => Number(x[1]))
    maxY = Math.max.apply(Math, yvals);
    colArray = figureInfo["paramList"][0][2].split("$");
    data = colArray.map(x => Math.log10(Math.max(Number(dataArray[Number(x)-1]), 0.1)));
    mean = d3.mean(data);
    pct = 0;
    for (i in percentileArray){
        if (mean >= Number(percentileArray[i])){
            pct = i
        }
    }
    var plotlydivid = divid + 'plotly';
    
    // Center it - --- allocate 40px for the text, 200 for the figure.  40 +20
    margintop = (totalheight - 240)/2;

    document.getElementById(divid).innerHTML = `
    <div class="row" id="` + plotlydivid + `" style="height: 200px; margin-top: `+ margintop + `px;" ></div>
    <div class="row" style="font-size:11px">Distribution of mean expression for all genes</div>
    <div class="row" style="font-size:11px"> ` + geneName + ` is ` + pct + ` percentile.</div>
    `;

    var trace1 = {
        x: xvals,
        y: yvals,
        yaxis: 'y1',
        fill: 'tozeroy',
        type: 'scatter',
        fillcolor: figurecolor,
        line: {
            color: 'white'
        }
    };
 

    var layout={  
        xaxis: {
            tickvals: [-1, 0, 1, 2, 3],
            ticktext: ["0.1", "1", "10", "100", "1000+"],
            tickangle:45,
            tickwidth: 1,
            tickfont: {
                size:10,
            },
            range:[-1,3],
            showgrid: true,
            showline: true,
            title: "FPKM",
            zeroline: false,
            titlefont: {family: 'Helvetica', size:10}
        }, 
        hovermode: !1,
        yaxis: {
                range: [0, maxY],
                fixedrange: true,
                ticks: '',
                showgrid: true,
                zeroline: false,
                showline: true,
                showticklabels: false,
                title: "Density",
                titlefont: {family: 'Helvetica', size:10},
        },
        annotations: [{
            x: mean,
            y: 0,
            ax:0,
            ay: -100,
            showarrow: true,
            arrowwidth:1,
            arrowhead:6,
            arrowcolor: "rgb(194,30,32)",
            text:"",
        }],
        margin: {
            l:20,
            b:50,
            r:50,
            t:50,
        }
    };
    
    Plotly.newPlot(plotlydivid, [trace1], layout, {displayModeBar: false});
}


