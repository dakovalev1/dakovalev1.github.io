function updateClass(){
    $(".nav-link-section").each(function(index){
        section = $($(this).attr("href"))
        offset = section.offset().top - $(window).scrollTop() - parseInt($("body").css("margin-top"), 10);

        if (offset <= 3){
            $(".nav-link-section").removeClass("active");
            $(this).addClass("active");
        } else {
            $(this).removeClass("active");
        }
    });
    
    if($(window).scrollTop() + $(window).height() >= $(document).height()){
        $(".nav-link-section").removeClass("active");
        $(".nav-link-section").last().addClass("active");
    }
}

$(document).ready(function(){
    updateClass();
    $(document).scroll(function(){
        updateClass();
    });
});