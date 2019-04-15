function scroll(elem){
    if (elem.length == 1){
        var offset = elem.offset().top - parseInt($("body").css("margin-top"), 10);

        $("html, body").stop();
        $("html, body").animate({
            scrollTop: offset
        }, 800);
    }
}

function process_hash(){
    var hash = window.location.hash;
    window.location.hash = "";
    scroll($(hash));
}



$(document).ready(function(){
    
    //console.log($.now());
    
    process_hash();

    $(window).on('hashchange',function(){ 
        process_hash();
    });
    
    $(".nav-link").click(function(event){
        if ($(".navbar-toggler").css("display") != "none"){
            $(".navbar-toggler").trigger("click");
        }
        $(this).addClass("active");
    });
    
    $("a").click(function(event){
        var href = $(this).attr("href");
        
        if (href.length > 0 && href[0] == '#'){
            var elem = $(href);
            
            if (elem.length == 1){
                event.preventDefault();
                scroll(elem);
            }
        }   
    });
});