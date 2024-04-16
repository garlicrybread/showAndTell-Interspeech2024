import {navigateToRoute} from './myJS.js'
import {urlPath} from './myJS.js'

const calNavBtn  = document.getElementById('calibrationNavBtn')
const tutNavBtn = document.getElementById('tutorialNavBtn')
const pracNavBtn = document.getElementById('practiceNavBtn')

calNavBtn.addEventListener("click", function() {
    navigateToRoute('vowelCalibration');
});
tutNavBtn.addEventListener("click", function() {
    navigateToRoute('tutorial/vowelP1');
});
pracNavBtn.addEventListener("click", function() {
    navigateToRoute('practice/chart');
});



