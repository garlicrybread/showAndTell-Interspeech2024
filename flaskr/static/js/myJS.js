import {drawVowels} from "./vwlChart.js";
import {changeCircleColor} from "./calibrate.js";

let mediaRecorders = []; // Array to store multiple media recorders
let chunks = []; // Array to store chunks for each recorder
let audioURLs = []; // Array to store multiple audio URLs
let recordingIndex = 0;
let stateIndex = 0;
let stream;
let recordingPath;
let processingPath;
export let urlPath;
export let calPath;
const sigProcName = 'signalProcessing'
const vwlName = 'vowelCalibration'
if (window.location.href.includes("/pronunciationVis/")) {
    const remote = '/pronunciationVis'
    recordingPath = `${remote}/audio`; // Set for remote
    processingPath = `${remote}/${sigProcName}`; // Set for remote
    urlPath = `${remote}/`;
    calPath = `${remote}/${vwlName}`
} else {
    recordingPath = "/audio"; // Set for local
    processingPath = "/"+sigProcName; // Set for local
    urlPath = `/`;
    calPath = `/${vwlName}`
}

export async function navigateToRoute(location) {
    // Retrieve the value of the input field with id "userId"
    console.log(location)
    const path = `${urlPath}${location}`
    window.location.href = path
}

export async function toggleText(buttonId,svgId='NA',cal=false) {
    console.log(`toggle Text cal ${cal}`, typeof  cal)
    var button = document.getElementById(buttonId);
    var loader_number;
    if (buttonId == "myButton") {
        loader_number = 1;
    } else {
        loader_number = 2;
    }

    function changeToRecording() {
        button.value = "Recording...";
        button.style.backgroundColor = "#78a9eb";
        startAnimation(loader_number);
        //{showWaves && <div className="wave-animation"></div>}
    }
    // Check the current text content of the button
    if (button.value !== "Recording...") {
        // Change the text content to "Don't click"
        button.value = "Calibrating...";
        startRecording(buttonId,cal,buttonId, svgId);
        console.log('Microphone Being used', stream);
        setTimeout(changeToRecording,1250)
        //{showWaves && <div className="wave-animation"></div>}
    } else {
        stopRecording(buttonId);
        // Change the text content to "Click me!"
        console.log('Stopped Using mic:', stream);
        //addNewAudioBar(buttonId);
        button.value = "Start Recording";
        button.style.backgroundColor = "";
        stopAnimation(loader_number);
    }
    console.log('end of toggling')
    return 'done'
}

function startRecording(word,cal,btnID,svgId) {
    const messageElement = document.getElementById('message');
    messageElement.textContent = "";
    // Prepare the data to be sent to the server
    var requestData = {
        word: word, // Provide the word you want to record
        debug: false, // Set debug mode if needed
        cal: cal
    };

    // Make a fetch request to your server endpoint where the Python function is executed
    // const path = window.location.href
    fetch(`${recordingPath}/api/record`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text();
    })
    .then(filePath => {
        // put the text back to record
        toggleText(btnID)
        console.log(`startRecording finished, cal ${cal}`)
        audioToJson(filePath, svgId,false, cal)
    })
    .catch(error => {
        // Handle errors
        console.error('Error recording file:', error);
    });
}

export function audioToJson(filePath, svgId,spa=false,cal=false) {
    const messageElement = document.getElementById('message');
    const obj = JSON.parse(filePath);
    // Check if "gotAudio" is "Quiet"
    if (obj["gotAudio"] === "Quiet") {
        messageElement.textContent = "We weren't able to hear anything! Try speaking louder."; // Display a user-friendly message
        return 'empty'; // You might not need to return 'empty' unless it's used elsewhere
    }

    var requestData = {
        filePath: obj['gotAudio'], // Provide the word you want to record
        cal: cal
    };

    fetch(`${processingPath}/api/processVwlData`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text();
    })
    .then(async data => {
        // Handle success
        const obj = JSON.parse(data)
        const [relfilepath, location] = obj['data']
        if (!cal) {
            console.log('Formants extracted successfully:', relfilepath);
            plotJson(relfilepath, svgId, spa)
        } else {
            console.log(`calibration, ${cal}, location: ${location}, ${relfilepath}`)
            await changeCircleColor('#svg-calibrate', location, 'green');
        }
    })
    .catch(error => {
        // Handle errors
        console.error('Error recording file:', error);
    });
}

function plotJson(filePath, svgId,spa=false) {
    const messageElement = document.getElementById('message');
    if (filePath === 'empty') {
        messageElement.textContent = 'No vowels detected.'; // Display a user-friendly message
        return 'empty'; // You might not need to return 'empty' unless it's used elsewhere
    }

    try {
        drawVowels(filePath, svgId, spa);
        messageElement.textContent = ''; // Clear message or provide a success message
    } catch (error) {
        console.error('Error drawing vowels:', error);
        messageElement.textContent = 'Failed to process the file. Please check the console for more details.';
    }
}
// function startRecording() {
//     navigator.mediaDevices.getUserMedia({
//         audio: true
//     }).then(stream => {
//         mediaRecorders[recordingIndex] = new MediaRecorder(stream);
//
//         mediaRecorders[recordingIndex].ondataavailable = (e) => {
//             chunks.push(e.data);
//         };
//
//         mediaRecorders[recordingIndex].start();
//
//         stateIndex = 1; //meaning that i have started recording.
//     }).catch(error => {
//         console.log('Following error has occurred: ', error);
//     });
// }
function startAnimation(loaderNumber) {
    var animationElement = document.querySelector(`.loader${loaderNumber}`);
    if (animationElement) {
        animationElement.classList.add('active');
    }
}


function stopAnimation(loader_number) {
    var animationElement = document.querySelector(`.loader${loader_number}`);
    if (animationElement) {
        animationElement.classList.remove('active');
    }
}

function addNewAudioBar(buttonId) {
    // Check if the audio URL for the current recording index is not null

    if (audioURLs[recordingIndex] != null) {
        console.log('Button ID:', buttonId);
        
        // Get the parent container for the button that was clicked
        var parentContainer = document.querySelector(`#${buttonId}`).closest('.flex-col');

        // Create a new AudioBar container
        var audioContainer = document.createElement('div');
        
        audioContainer.classList.add('audio-container');

        // Create a new audio element
        var audioElement = document.createElement('audio');
        audioElement.id = `audio${recordingIndex}`
        audioElement.controls = true;
        audioElement.src = audioURLs[recordingIndex];

        // Append the AudioBar container to the parent container
        
        parentContainer.appendChild(audioContainer);
        // Append the audio element to the AudioBar container
        audioContainer.appendChild(audioElement);
        var deleteButton = document.createElement('button');
        deleteButton.textContent = 'Delete Recording';
        deleteButton.id = `deleteButton${recordingIndex}`
        deleteButton.addEventListener('click', function () {
            // Call a function to handle the deletion
            deleteRecording(audioElement.id, audioContainer);
        });

        // Append the delete button to the AudioBar container
        audioContainer.appendChild(deleteButton);
        recordingIndex++;
    } else {
        console.log('There is no recording at this index', stream);
    }
    
}

function deleteRecording(audioId, audioContainer) {
    // Identify the audio element associated with the delete button
    //var audioContainer = document.querySelector(`#${buttonId}`).closest('.audio-container');

    if (audioContainer) {
        audioContainer.remove();
        var deleteId = numericPart = parseInt(audioId.match(/\d+/)[0], 10);
        mediaRecorders.splice(deleteId, 1);
        audioURLs.splice(deleteId, 1);
    }

    console.log(`Deleted recording for audio ID: ${audioId}`);
}

function stopRecording(buttonId) {
    // if (mediaRecorders[recordingIndex] && stateIndex === 1) {
    //     mediaRecorders[recordingIndex].ondataavailable = (e) => {
    //         chunks.push(e.data);
    //     };
    //
    //     mediaRecorders[recordingIndex].onstop = () => {
    //         const blob = new Blob(chunks, { 'type': 'audio/ogg; codecs=opus' });
    //         audioURLs[recordingIndex] = window.URL.createObjectURL(blob);
    //
    //         // Add the new AudioBar after the audio URL is updated
    //         // addNewAudioBar(buttonId);
    //
    //         // Clear the chunks array for the next recording
    //         chunks = [];
    //     };
    //
    //     mediaRecorders[recordingIndex].stop();
    // } else {
    //     console.error('mediaRecorders[recordingIndex] is undefined');
    // }
    console.log('stopped recording')
    stateIndex = 0; // stopped recording
}




// document.getElementById("myButton").addEventListener("click", function () {
//     toggleText("myButton");
// });

// document.getElementById("myButton2").addEventListener("click", function () {
//     toggleText("myButton2");
// });
