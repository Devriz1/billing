document.addEventListener("DOMContentLoaded", function () {

    const sidebar = document.getElementById("sidebar");
    const main = document.getElementById("mainContent");
    const toggle = document.getElementById("sidebarToggle");

    if (!sidebar || !main || !toggle) return;

    function applyState(collapsed){

        sidebar.classList.toggle("collapsed", collapsed);
        main.classList.toggle("expanded", collapsed);

        localStorage.setItem(
            "sidebar",
            collapsed ? "collapsed" : "expanded"
        );

    }

    applyState(
        localStorage.getItem("sidebar") === "collapsed"
    );

    toggle.addEventListener("click", function(){

        applyState(
            !sidebar.classList.contains("collapsed")
        );

    });

});

/* fullscreen */

const fullscreenBtn=document.getElementById("fullscreenBtn");

if(fullscreenBtn){

    function updateFullscreenIcon(){
        const icon=fullscreenBtn.querySelector("i");
        if(document.fullscreenElement){
            icon.classList.remove("bi-arrows-fullscreen");
            icon.classList.add("bi-fullscreen-exit");
        }else{
            icon.classList.remove("bi-fullscreen-exit");
            icon.classList.add("bi-arrows-fullscreen");
        }
    }

    function enterFullscreen(){
        document.documentElement.requestFullscreen().then(()=>{
            localStorage.setItem("fullscreen","true");
            updateFullscreenIcon();
        }).catch(()=>{
            localStorage.setItem("fullscreen","false");
            updateFullscreenIcon();
        });
    }

    function exitFullscreen(){
        if(document.fullscreenElement){
            document.exitFullscreen();
        }
        localStorage.setItem("fullscreen","false");
        updateFullscreenIcon();
    }

    fullscreenBtn.onclick=function(){
        if(document.fullscreenElement){
            exitFullscreen();
        }else{
            enterFullscreen();
        }
    };

    document.addEventListener("fullscreenchange",updateFullscreenIcon);

    document.addEventListener("keydown",function(e){
        if(e.key==="Escape"){
            if(document.fullscreenElement){
                e.preventDefault();
                if(e.ctrlKey){
                    exitFullscreen();
                }
            }
        }
        if(e.key==="Escape"&&e.ctrlKey){
            if(document.fullscreenElement){
                exitFullscreen();
            }
        }
    });

    if(localStorage.getItem("fullscreen")==="true"){
        enterFullscreen();
    }

}