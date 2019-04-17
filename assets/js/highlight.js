function getDocHeight() {
    var D = document;
    return Math.max(
        D.body.scrollHeight, D.documentElement.scrollHeight,
        D.body.offsetHeight, D.documentElement.offsetHeight,
        D.body.clientHeight, D.documentElement.clientHeight
    );
}

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
    
    if($(window).scrollTop() + $(window).height() >= getDocHeight()) {
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