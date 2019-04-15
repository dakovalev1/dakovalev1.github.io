$(document).ready(function(){
    $(".nav-link").click(function(event){
        if ($(".navbar-toggler").css("display") != "none"){
            $(".navbar-toggler").trigger("click");
        }
    });
    
    $("a").click(function(event){
        var href = $(this).attr("href");
        
        if (href.length > 0 && href[0] == '#'){
            var elem = $(href);
            
            if (elem.length == 1){
                event.preventDefault();
                
                var offset = elem.offset().top - parseInt($("body").css("margin-top"), 10);
                
                $("html, body").stop();
                $("html, body").animate({
                    scrollTop: offset
                }, 800);
            }
        }   
    });
});