function create_download_tabs(btnKey){

    // First get the dataset for the respective button. 

    var layout = panelJson[btnKey]["paramList"];
    var figureKeyArray = [];
    for (i in layout){
        if (layout[i][0]=="FIGURE"){
            figureKeyArray.push(layout[i][1])
        }
    }
    var datasetKeyArray = [];
    for (i in figureKeyArray){
        datasetkey = figureJson[figureKeyArray[i]]["datasetkey"]
        datasetKeyArray.push(datasetkey);
    }
    var uniqueDatasets = ArrNoDupe(datasetKeyArray);

    var fileInfoArray = [];
    for (i in uniqueDatasets){
        for (j in datasetJson){
            if (datasetJson[j]["datasetkey"]== uniqueDatasets[i]){
                fileInfoArray.push(datasetJson[j]["datasetfile"]);
            }
        }
    }

    for (i in fileInfoArray){
        tmparray = fileInfoArray[i].split("/");
        filename = tmparray[tmparray.length-1];
        src = "https://storage.googleapis.com/" + siteJson["appid"] + ".appspot.com/" + filename;
        var link= document.createElement("div");
        link.innerHTML = `
        <a href="` + src + `" >Download dataset link` + `</a>
        `
        document.getElementById('downloadData').appendChild(link);
    }
}

function ArrNoDupe(a) {
    var temp = {};
    for (var i = 0; i < a.length; i++)
        temp[a[i]] = true;
    var r = [];
    for (var k in temp)
        r.push(k);
    return r;
}