function scroll(sec_id) {
    console.log('scroll', sec_id);
    element = $(sec_id)
    if (element.length != 1) {
        return
    }
    offset = element.offset().top - $('body').cssNumber('margin-top');
    $('html, body').stop();
    $('html, body').animate({
        scrollTop: offset
    }, 800);
}

$(document).ready(function () {
    $('.nav-link').click(function (event) {
        scroll($(this).attr('href'));
        if ($('.navbar-toggler').css('display') != 'none'){
            $('.navbar-toggler').trigger('click');
        }
        return false;
    });
})