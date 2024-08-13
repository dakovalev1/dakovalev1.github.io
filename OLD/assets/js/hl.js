function updateClass() {
    max_index = 0
    last_index = 0

    $('.nav-link-section').each(function (index) {
        offset = $(document).scrollTop() + $('body').cssNumber('margin-top') - $($(this).attr('href')).offset().top
        if (offset >= -5 && max_index < index) {
            max_index = index
        }
        if (last_index < index) {
            last_index = index;
        }
    })

    bottom_offset = $(document).scrollTop() + window.innerHeight - $('.bottom').offset().top
    if (bottom_offset >= 0) {
        max_index = last_index;
    }
    

    $('.nav-link-section').each(function (index) {
        if (index == max_index) {
            $(this).addClass("active");
        } else {
            $(this).removeClass("active");
        }
    });
}

$(document).ready(function () {
    updateClass()
    $(document).scroll(function () {
        updateClass()
    });
});