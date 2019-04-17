function updateClass(){
    max_index = 0;
    
    $(".nav-link-section").each(function(index){
        section = $($(this).attr("href"))
        offset = section.offset().top - $(window).scrollTop() - parseInt($("body").css("margin-top"), 10);

        if (offset <= 3 && max_index < index){
            max_index = index;
        }
        
    });
    
    $(".nav-link-section").each(function(index){
        if(index== max_index){
            $(this).addClass("active");
        }else{
            $(this).removeClass("active");
        }
    });
    
    if ($('.bottom').offset().top <= $(window).scrollTop() + (window.innerHeight || $(window).height())){
        $(".nav-link-section").removeClass("active");
        $(".nav-link-section").last().addClass("active");
    }
}

$(document).ready(function(){
    updateClass();
    $(document).scroll(function(){
        updateClass();
    });
    //$(".footer").css("height", $(window).height() - parseInt($("body").css("margin-top"), 10));
    //$(".footer").css("min-height", $(window).height());
});