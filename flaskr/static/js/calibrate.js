import {navigateToRoute} from "./myJS.js";
import {toggleText} from './myJS.js';

console.log('in vowelCalibration')
const homeNavBtn = document.getElementById('homeNavBtn');
const frontHighBtn = document.getElementById('frontHigh');
const backHighBtn = document.getElementById('backHigh');
const frontLowBtn = document.getElementById('frontLow');
const backLowBtn = document.getElementById('backLow');
const calibrateBtn = document.getElementById('calibrateBtn')

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

calibrateBtn.addEventListener('click', function () {
    processCoordinateData()
});

function processCoordinateData() {
    fetch(`coordinates/api/processCoordinateData`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text();
    })
    .then(result => {
        // Handle success
        console.log('Formants extracted successfully:',result);
    })
    .catch(error => {
        // Handle errors
        console.error('Error processing data:', error);
    });
}