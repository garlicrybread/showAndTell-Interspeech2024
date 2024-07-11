import {navigateToRoute, calPath, audioToJson} from "./myJS.js";
import {toggleText} from './myJS.js';
import {drawVowelChart, getSvgCoordinates} from "./vwlChart.js";


console.log('in vowelCalibration')
const homeNavBtn = document.getElementById('homeNavBtn');
const frontHighBtn = document.getElementById('frontHigh');
const backHighBtn = document.getElementById('backHigh');
const frontLowBtn = document.getElementById('frontLow');
const backLowBtn = document.getElementById('backLow');
const calibrateBtn = document.getElementById('calibrateBtn')
const button = document.getElementById('btnUserId')

document.addEventListener('DOMContentLoaded', (event) => {
    const name = 'calibrate';
    drawVowelChart(name); // Change 'pair1' to the ID of the first tab content
    circlesOnEdges(name);
});

homeNavBtn.addEventListener('click', function () {
    navigateToRoute('')
});

frontHighBtn.addEventListener('click', function () {
    toggleText('frontHigh','NA',true)
});
backHighBtn.addEventListener('click', function () {
    toggleText('backHigh', 'NA',true)
});
frontLowBtn.addEventListener('click', function () {
    toggleText('frontLow', 'NA',true)
});
backLowBtn.addEventListener('click', function () {
    toggleText('backLow', 'NA',true)
});

calibrateBtn.addEventListener('click', function () {
    processCoordinateData()
    processCoordinateData(true)
});
button.addEventListener("click", saveUserId);

function processCoordinateData(spa=false) {
    fetch(`${calPath}/api/processCoordinateData`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'spa':spa})
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
async function saveUserId() {
    const userId = document.getElementById("textInputId").value;
    fetch(`${calPath}/api/saveUserId`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'userId':userId})
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text();
    })
    .then(result => {
        // Handle success
        console.log('userid saved successfully:',result);
    })
    .catch(error => {
        // Handle errors
        console.error('Error saving userid:', error);
    });
}

async function circlesOnEdges(svgId) {
    const svg = d3.select(`#svg-${svgId}`);
    const coordinates = await getSvgCoordinates();
    console.log('coordinates');
    console.log(coordinates)
    const circleRadius = 5;
    const circleColor = "#AF6868";

    // location goes from right to left top to bottom start at 0 and ending at 3
    coordinates.forEach(([x, y],index) => {
        svg.append("circle")
            .attr("cx", x)
            .attr("cy", y)
            .attr("r", circleRadius)
            .attr("fill", circleColor)
            .attr("id", `location-${index}`);
    });
}

// Function to change the color of a specific circle based on the location attribute
export async function changeCircleColor(svgId, location, newColor) {
    const svg = d3.select(`${svgId}`);
    const name = `#location-${location}`
    console.log(name, svgId)
    const circle = svg.select(name);

    // Debugging: Check if any circles are selected
    console.log(`Selected circles: ${circle.size()}`);

    circle.attr("fill", newColor);
    svg.select(`#location-${location}`)
        .attr("fill", newColor);
}

