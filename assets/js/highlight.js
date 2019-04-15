function updateClass(){
    max_index = 0;
    
    $(".nav-link-section").each(function(index){
        section = $($(this).attr("href"))
        offset = section.offset().top - $(window).scrollTop() - parseInt($("body").css("margin-top"), 10);

        if (offset <= 0 && max_index < index){
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
}

$(document).ready(function(){
    updateClass();
    $(document).scroll(function(){
        updateClass();
    });
});