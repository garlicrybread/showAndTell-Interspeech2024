import {navigateToRoute, calPath, audioToJson} from "./myJS.js";
import {toggleText} from './myJS.js';
import {drawVowelChart, getSvgCoordinates} from "./vwlChart.js";
import {openTab} from "./practice.js";


if (window.location.href.includes("/vowelCalibration")) {
    console.log('in vowelCalibration')
    const notCalColor = "#AF6868"
    const homeNavBtn = document.getElementById('homeNavBtn');
    const frontHighBtn = document.getElementById('frontHighTab').getElementsByClassName('btnVwlCal')[0];
    const backHighTab = document.getElementById('backHighTab');
    const frontLowTab = document.getElementById('frontLowTab');
    const backLowTab = document.getElementById('backLowTab');
    const calibrateBtn = document.getElementById('calibrateBtn');
    const buttonUserId = document.getElementById('btnUserId');
    const userIDDiv = document.getElementById('userIdDiv');
    console.log('fronthigh ', document.getElementById('frontHigh'))

    document.addEventListener('DOMContentLoaded', async (event) => {
        const name = 'calibrate';
        drawVowelChart(name); // Change 'pair1' to the ID of the first tab content
        await circlesOnEdges(name, notCalColor);
    });


    homeNavBtn.addEventListener('click', function () {
        navigateToRoute('')
    });

    buttonUserId.addEventListener("click", handleUserClick);
    document.getElementsByClassName('btnVwlCal')[0].addEventListener('click', function () {
        var tab = 0;
        let yesBtn = document.getElementsByClassName('yesBtn')[tab];
        recordingVwlCal('heat','frontHigh',tab,yesBtn);
        yesBtn.addEventListener('click', function () {
            openTab('na','backHighTab');
        });
    })

    document.getElementsByClassName('btnVwlCal')[1].addEventListener('click', function () {
        var tab = 1;
        let yesBtn = document.getElementsByClassName('yesBtn')[tab];
        recordingVwlCal('hoot','backHigh',tab,yesBtn);
        yesBtn.addEventListener('click', function () {
            openTab('na','frontLowTab');
        });
    })

    document.getElementsByClassName('btnVwlCal')[2].addEventListener('click', function () {
        var tab = 2;
        let yesBtn = document.getElementsByClassName('yesBtn')[tab];
        recordingVwlCal('hat','frontLow',tab,yesBtn);
        yesBtn.addEventListener('click', function () {
            openTab('na','backLowTab');
        });
    })

    document.getElementsByClassName('btnVwlCal')[3].addEventListener('click', function () {
        var tab = 3;
        let yesBtn = document.getElementsByClassName('yesBtn')[tab];
        recordingVwlCal('awe','backLow',tab,yesBtn);
        yesBtn.addEventListener('click', function () {
            processCoordinateData(calibrateBtn,false);
            navigateToRoute('');
        });
    })

    function handleUserClick() {
        saveUserId();
        // Show the success message
        const successDiv = document.getElementById('successMessage')
        successDiv.style.display = 'flex';
        // Hide the success message after 3 seconds
        setTimeout(function() {
            successDiv.style.display = 'none';
        }, 3000);
        document.getElementById('userIdDiv').style.display = 'none';
        frontHighBtn.disabled = false;
    }
}

async function recordingVwlCal(word,btnName,tab,yesBtn) {
    const btn = document.getElementById(btnName);
    const divmessage = document.getElementsByClassName('recordingInstructions')[tab];
    divmessage.style.display = 'none';
    toggleText(word,btnName, 'NA', true, tab);
    const noBtn = document.getElementsByClassName('noBtn')[tab];
    const qPara = document.getElementsByClassName('questionQual')[tab];
    console.log('frontbtn ',yesBtn);
    noBtn.addEventListener('click', function () {
        btn.style.display = 'flex';
        btn.value = "Start";
        btn.disabled = false;
        yesBtn.style.display = 'none';
        noBtn.style.display = 'none';
        qPara.style.display = 'none';
    });
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
