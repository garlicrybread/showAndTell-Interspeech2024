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
    const calibrateBtn = document.getElementById('calibrateBtn');
    const buttonUserId = document.getElementById('btnUserId');
    const userIDDiv = document.getElementById('userIdDiv');

    document.addEventListener('DOMContentLoaded', async (event) => {
        const name = 'calibrate';
        drawVowelChart(name); // Change 'pair1' to the ID of the first tab content
        await circlesOnEdges(name, notCalColor);
    });


    // homeNavBtn.addEventListener('click', function () {
    //     navigateToRoute('')
    // });
    buttonUserId.addEventListener("click", function () {
        saveUserId();
        // Hide the form
        document.getElementById('userIdDiv').style.display = 'none';

        // Show the success message
        const successDiv = document.getElementById('successMessage')
        successDiv.style.display = 'flex';
        // Hide the success message after 3 seconds
        setTimeout(function() {
            successDiv.style.display = 'none';
        }, 3000);
    });

    // get user id from url param
    const urlParams = new URLSearchParams(window.location.search);
    const userId = urlParams.get('userId')

    // make sure user is registered
    // if (userId !== null) {
    //     frontHighBtn.disabled = false;
    //     backHighBtn.disabled = false;
    //     frontLowBtn.disabled = false;
    //     backLowBtn.disabled = false;
    //     const svgName = '#svg-calibrate';
    //     frontHighBtn.addEventListener('click', async function () {
    //         await toggleText('frontHigh', 'NA', true);
    //     });
    //     backHighBtn.addEventListener('click', async function () {
    //         await toggleText('backHigh', 'NA', true);
    //     });
    //     frontLowBtn.addEventListener('click', async function () {
    //         await toggleText('frontLow', 'NA', true);
    //     });
    //     backLowBtn.addEventListener('click', async function () {
    //         await toggleText('backLow', 'NA', true);
    //     });
    // }
}

function processCoordinateData(btn,spa=false) {
    const messageElement = document.getElementById('calMessage')
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
        const successColor = '#34eba4';
        btn.value = 'Success!';
        btn.style.backgroundColor = successColor;
        messageElement.textContent = '';
    })
    .catch(error => {
        // Handle errors
        console.error('Error processing data:', error);
        messageElement.textContent = 'Unable to calibrate. Please try re-recording the words!'
        btn.value = 'Calibrate!';
        btn.style.backgroundColor = "";
        btn.disabled = true;
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
        .attr("fill", newColor)
        .attr('r',10);

    // Get the circle's center coordinates
    const cx = +circle.attr('cx');
    const cy = +circle.attr('cy');

    // Remove any existing checkmarks (if any)
    circle.selectAll("text").remove();

    // Add a checkmark inside the circle
    d3.select("svg").append("text")
        .attr("x", cx) // Center the text horizontally at the circle's center
        .attr("y", cy) // Center the text vertically at the circle's center
        .attr("dy", ".35em") // Adjust vertical alignment
        .attr("text-anchor", "middle") // Center align the text
        .attr("font-size", 10) // Adjust font size as needed
        .attr("fill", "black") // Adjust color as needed
        .text("✔");

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
        processCoordinateData(calibrateBtn)
        processCoordinateData(calibrateBtn,true)
    });
}
