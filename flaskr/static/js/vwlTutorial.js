import {navigateToRoute, toggleText} from "./myJS.js";
// import {openTab} from "./practice.js";

homeNavBtn.addEventListener('click', function () {
    navigateToRoute('')
});

function playSound(audioFileId) {
    var audio = document.getElementById(audioFileId);
    audio.play();
}

window.playSound = playSound
window.navigateToRoute = navigateToRoute
