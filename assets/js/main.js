$(document).ready(function () {
});

function navbar_link_click() {
    let navbar_toggler = document.querySelector(".navbar-toggler");
    if (getComputedStyle(navbar_toggler).getPropertyValue("display") != 'none') {
        navbar_toggler.click();
    }
}