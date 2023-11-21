$(document).ready(function(){
    $('.a-dark-light').click(function(event){
        mode = $('html').attr('data-bs-theme');
        if (mode == 'light'){
            $('html').attr('data-bs-theme', 'dark');
        }else{
            $('html').attr('data-bs-theme', 'light');
        }
        return false;
    })
});