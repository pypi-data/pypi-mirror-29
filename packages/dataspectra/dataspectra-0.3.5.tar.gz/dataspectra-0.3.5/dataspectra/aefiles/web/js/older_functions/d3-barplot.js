
function draw_barplot(labelList, meanList, sdList, maxList) {
    var svg = d3.select("svg");
    var margin = { top: 20, right: 20, bottom: 50, left: 50 };
    var width = +svg.attr("width") - margin.left - margin.right;
    var height = +svg.attr("height") - margin.top - margin.bottom;
    var maxVal = d3.max(maxList);

    var x = d3.scaleBand()
        .rangeRound([0, width])
        .padding(0.1)
        .domain(labelList);

    var y = d3.scaleLinear()
        .rangeRound([height, 0])  // THIS IS INVERTED
        .domain([0, d3.max(maxList)]); // CONVENTIONAL

    var g = svg.append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var tip = d3.tip()
        .attr('class', 'd3-tip')
        .offset([-10, 0])
        .html(function (d, i) {
            return "<strong>Mean:</strong> <span style='color:red'>" + meanList[i] +
                "<br></br></span> <strong>SD:</strong><span style='color:red'>" + Math.round(sdList[i] * 100) / 100 + "</span>";
        });

    svg.call(tip);

    g.append("g")
        .attr("class", "axis axis-x")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x))
        .append("text")
        .attr("y", 0)
        .attr("dy", "2.7em")
        .attr("x", width / 2)
        .style("text-anchor", "middle")
        .text("Age");

    g.append("g")
        .attr("class", "axis axis-y")
        .call(d3.axisLeft(y))
        .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0)
        .attr("x", 0 - (height / 2))
        .attr("dy", "-2.3em")
        .style("text-anchor", "middle")
        .text("FPKM");

    var t = d3.transition()
        .duration(500);

    g.selectAll("rect")
        .data(labelList)
        .enter().append("rect")
        .transition(t)
        .ease(d3.easePoly)
        .attr("x", function (d, i) { return x(labelList[i]); })
        .attr("y", function (d, i) { return y(meanList[i]) }) //THIS IS INVERTED
        .attr("width", x.bandwidth())
        .attr("height", function (d, i) { return height - y(meanList[i]) }) //ALSO INVERTED
  
    g.selectAll("rect")
        .on('mouseover', tip.show)
        .on('mouseout', tip.hide)

}


function create_barplot(figureMatch, dataJson) {

    factorMat = figureMatch["figureMat"];

    //Go through each factor and calculate
    labelList = factorMat.map(function (d) { return d[1] });

    var result = calc_mean_and_sd_from_mat(factorMat, dataJson);
    var meanList = result[0], sdList = result[1]
    var maxList = sdList.map(function (d, i) { return meanList[i] + d })

    draw_barplot(labelList, meanList, sdList, maxList);

    var aspect = 960 / 500, chart = d3.select('#chart');
    d3.select(window)
        .on("resize", function () {
            var targetWidth = chart.node().getBoundingClientRect().width;
            chart.attr("width", targetWidth);
            chart.attr("height", targetWidth / aspect);
        });
}