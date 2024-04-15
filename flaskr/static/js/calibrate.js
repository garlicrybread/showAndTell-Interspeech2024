import {navigateToRoute} from "./myJS.js";
import {toggleText} from './myJS.js';

console.log('in vowelCalibration')
const homeNavBtn = document.getElementById('homeNavBtn');
const frontHighBtn = document.getElementById('frontHigh');
const backHighBtn = document.getElementById('backHigh');
const frontLowBtn = document.getElementById('frontLow');
const backLowBtn = document.getElementById('backLow');

homeNavBtn.addEventListener('click', function () {
    navigateToRoute('')
});

frontHighBtn.addEventListener('click', function () {
    toggleText('frontHigh','True')
});
backHighBtn.addEventListener('click', function () {
    toggleText('backHigh', 'True')
});
frontLowBtn.addEventListener('click', function () {
    toggleText('frontLow', 'True')
});
backLowBtn.addEventListener('click', function () {
    toggleText('backLow', 'True')
});

