window.MathJax = {
    options: {
        ignoreHtmlClass: ".*",
        processHtmlClass: "arithmatex"
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