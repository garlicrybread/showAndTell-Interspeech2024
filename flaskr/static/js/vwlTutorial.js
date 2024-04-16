import {navigateToRoute, toggleText} from "./myJS.js";

document.getElementById("recordWord").addEventListener("click", function () {
    toggleText("recordWord");
});

homeNavBtn.addEventListener('click', function () {
    navigateToRoute('')
});