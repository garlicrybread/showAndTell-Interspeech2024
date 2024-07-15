import {navigateToRoute, calPath, audioToJson} from "./myJS.js";
import {toggleText} from './myJS.js';
import {drawVowelChart, getSvgCoordinates} from "./vwlChart.js";


if (window.location.href.includes("/vowelCalibration")) {
    console.log('in vowelCalibration')
    const notCalColor = "#AF6868"
    const homeNavBtn = document.getElementById('homeNavBtn');
    const frontHighBtn = document.getElementById('frontHigh');
    const backHighBtn = document.getElementById('backHigh');
    const frontLowBtn = document.getElementById('frontLow');
    const backLowBtn = document.getElementById('backLow');
    const calibrateBtn = document.getElementById('calibrateBtn')
    const button = document.getElementById('btnUserId')

    document.addEventListener('DOMContentLoaded', async (event) => {
        const name = 'calibrate';
        drawVowelChart(name); // Change 'pair1' to the ID of the first tab content
        await circlesOnEdges(name, notCalColor);
    });


    homeNavBtn.addEventListener('click', function () {
        navigateToRoute('')
    });
    button.addEventListener("click", saveUserId);
    // get user id from url param
    const urlParams = new URLSearchParams(window.location.search);
    const userId = urlParams.get('userId')

    // make sure user is registered
    if (userId !== null) {
        frontHighBtn.disabled = false;
        backHighBtn.disabled = false;
        frontLowBtn.disabled = false;
        backLowBtn.disabled = false;
        const svgName = '#svg-calibrate';
        frontHighBtn.addEventListener('click', async function () {
            await toggleText('frontHigh', 'NA', true);
        });
        backHighBtn.addEventListener('click', async function () {
            await toggleText('backHigh', 'NA', true);
        });
        frontLowBtn.addEventListener('click', async function () {
            await toggleText('frontLow', 'NA', true);
        });
        backLowBtn.addEventListener('click', async function () {
            await toggleText('backLow', 'NA', true);
        });
    }
}

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

async function circlesOnEdges(svgId, color) {
    const svg = d3.select(`#svg-${svgId}`);
    const coordinates = await getSvgCoordinates();
    const circleRadius = 5;
    const circleColor = color;

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
    const circle = svg.select(name);
    const disabledColor = circle.attr('fill');
    circle.attr("fill", newColor);
    svg.select(`#location-${location}`)
        .attr("fill", newColor);

    // check to see if all circles have been colored in
    const loc = '#location-'
    for (let i = 0; i <= 3; i++) {
        var cir = svg.select(loc+i);
        if (cir.size() === 0) {
            return false
        }
        if (cir.attr('fill') === disabledColor) {
            return false
        }
    }
    const calibrateBtn = document.getElementById('calibrateBtn')
    calibrateBtn.disabled = false;
    calibrateBtn.addEventListener('click', function () {
        processCoordinateData()
        processCoordinateData(true)
    });
}
