$(document).ready(function(){
    
    $("a").click(function(event){
        var href = $(this).attr("href");
        
        if (href.length > 0 && href[0] == '#'){
            var elem = $(href);
            
            if (elem.length == 1){
                event.preventDefault();
                
                var offset = elem.offset().top - parseInt($(".navbar").css("height"), 10);
            
                $("html, body").animate({
                    scrollTop: offset
                }, 800);
            }
        }   
    });
});