var log = document.getElementById('login-btn');
var sign = document.getElementById('signup-btn');
window.onclick = function (event) {
    if (event.target == log) {
        log.style.display = "none";
    }
    if (event.target == sign) {
        sign.style.display = "none";
    }
}