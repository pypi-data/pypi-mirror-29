function create_carousel(figureMatch, divid){
  images = figureMatch["paramList"]
  
  document.getElementById(divid).removeAttribute("style");
  console.log(images);
  var a = `
    <div id="carousel-example-generic" class="carousel slide" data-ride="carousel" data-interval="false">
    <!-- Indicators -->
      <ol class="carousel-indicators">
        <li data-target="#carousel-example-generic" data-slide-to="0" class="active"></li>
        <li data-target="#carousel-example-generic" data-slide-to="1"></li>
        <li data-target="#carousel-example-generic" data-slide-to="2"></li>
      </ol>

  <!-- Wrapper for slides -->
      <div class="carousel-inner" role="listbox">`

      imgList = [];
  for (i in images){
    if (i==0){
      var imghtml = `<div class="item active"><img src="/images/` + images[i][1]  + `" alt="..." ></img></div>`
      imgList.push(imghtml);
    }
    else{
    var imghtml = `<div class="item"><img src="/images/` + images[i][1]  + `" alt="..." ></img></div>`
    imgList.push(imghtml);
    }
  }
  
    var b =  `
    </div>
    <!-- Controls -->
    <a class="left carousel-control" href="#carousel-example-generic" role="button" data-slide="prev">
      <span class="glyphicon glyphicon-chevron-left" aria-hidden="true"></span>
      <span class="sr-only">Previous</span>
    </a>
    <a class="right carousel-control" href="#carousel-example-generic" role="button" data-slide="next">
      <span class="glyphicon glyphicon-chevron-right" aria-hidden="true"></span>
      <span class="sr-only">Next</span>
    </a>
  </div>`

  document.getElementById(divid).innerHTML = a+ imgList.join(' ') + b
}