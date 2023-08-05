// Script to add announcements. 

function add_announcement(mainJson){
    var anndata = mainJson["paramList"][0];
    var message = anndata[1];
    var linksrc = anndata[2];
    var announcement= document.createElement("div");
    announcement.innerHTML = `
    <div class="wrap header-top"  style="background-color: grey;">
        <div class="container header-top-container">
            <div class="row">
                <div class="col-xs-12 text-center" style="font-size: 14px"><a href="` + linksrc +  `" style="color: white;">` + message + `
                </a></div>
            </div> <!-- row -->
        </div>
    </div>
    `
    document.getElementById('announcementlocation').appendChild(announcement);
}