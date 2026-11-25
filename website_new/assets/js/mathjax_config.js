window.MathJax = {
    options: {
        ignoreHtmlClass: ".*",
        processHtmlClass: "arithmatex"
    },
    startup: {
        ready() {
            MathJax.startup.defaultReady();
            MathJax.tex2mml({{ macros | default('') | tojson }});
        }
    }
};