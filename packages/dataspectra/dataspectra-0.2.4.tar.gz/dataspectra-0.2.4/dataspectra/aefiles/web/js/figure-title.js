function create_title(figureInfo, dataArray, divid){
    var geneCol = figureInfo["gene"];

    document.getElementById(divid).style.height = "60px";
    document.getElementById(divid).style.marginTop="0px";
    //document.getElementById(divid).style.marginBottom="20px"; #Only when margin bottom is specified.
    var matchingTerm = "no match found"


    paramList =  figureInfo["paramList"];
    console.log(paramList[0]);
    color = paramList[0][4];
    dataset = paramList[0][3];
    column = Number(paramList[0][2]);
    if (dataArray==null){
        matchingTerm = "No matching term"
    }
    else{
        if (dataset=="data"){
            matchingTerm = dataArray[column-1];
        }
    }   

    document.getElementById(divid).innerHTML = `
        <div class="col-xs-12 text-left"  style="color: ` + color + `" >
            <h2> Search Term: ` + searchTerm + `</h2>
        </div>
        `
}


function create_title_homology(figureInfo, dataArray, divid){
    var geneCol = figureInfo["gene"];
    document.getElementById(divid).style.height = "60px";
    document.getElementById(divid).style.marginTop="0px";
    //document.getElementById(divid).style.marginBottom="20px"; #Only when margin bottom is specified.
    if (dataArray!=null){
    var geneName = dataArray[geneCol-1];
    }
    else {var geneName = "no match found"}
    document.getElementById(divid).innerHTML = `
        <div class="col-xs-10">
            <h2>` + geneName + `</h2>
        </div>
        <div class="col-xs-2" >
            <img src="/images/` + figureInfo["image"]   + `" style="height: 40px; margin-top:10px" ></img>
        </div>`;
}