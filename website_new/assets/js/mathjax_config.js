window.MathJax = {
    options: {
        ignoreHtmlClass: ".*",
        processHtmlClass: "arithmatex",
        menuOptions: {
            settings: {
                speech: false,
                braille: false,
                assistiveMml: true
            }
        }
    },
    startup: {
        ready() {
            MathJax.startup.defaultReady();

            const macros = document.getElementById("latex-macros");

            if (macros) {
                MathJax.tex2mml(macros.textContent);
            }
        }
    }
};