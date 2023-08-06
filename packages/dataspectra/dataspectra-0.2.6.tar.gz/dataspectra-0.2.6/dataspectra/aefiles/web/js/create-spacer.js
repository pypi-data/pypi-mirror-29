function create_spacer(divid){

    // 
    console.log("adding breaker")
    document.getElementById(divid).style.height = "60px";
    document.getElementById(divid).style.marginTop="0px";
    //document.getElementById(divid).style.marginBottom="20px"; #Only when margin bottom is specified.

    document.getElementById(divid).innerHTML = `
    <div class="row"><hr></div>
    `
}