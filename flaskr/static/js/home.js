import {navigateToRoute} from './myJS.js'
import {urlPath} from './myJS.js'

const calNavBtn  = document.getElementById('calibrationNavBtn')
const pracNavBtn = document.getElementById('practiceNavBtn')

calNavBtn.addEventListener("click", function() {
    navigateToRoute('vowelCalibration');
});
pracNavBtn.addEventListener("click", function() {
    navigateToRoute('practice/chart');
});



