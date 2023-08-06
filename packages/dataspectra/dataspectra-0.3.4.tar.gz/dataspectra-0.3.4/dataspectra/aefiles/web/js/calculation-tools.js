
function calc_mean_and_sd_from_mat(factorMat, dataArray) {
    // factorMat should be an array - with each element as a separate column
    // For each element in factorMat, the 3rd element should have the indices to average for dataJson
    // We could turn this into a mapping function later. That will save space (and maybe time too?)
    var meanList = [];
    var sdList = [];
    console.log(factorMat);
    for (i = 0; i < factorMat.length; i++) {
        if (factorMat[i][0]=="BAR"){
        cols = factorMat[i][2];
        colArray = cols.split("$");
        data = colArray.map(x => dataArray[x])
        mean = d3.mean(data)
        sd = d3.deviation(data)
        meanList.push(mean)
        sdList.push(sd)
        }
    }
    return [meanList, sdList];
}