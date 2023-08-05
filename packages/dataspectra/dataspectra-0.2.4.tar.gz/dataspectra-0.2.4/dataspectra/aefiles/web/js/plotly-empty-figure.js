function empty_figure(figureInfo, divid){

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
}