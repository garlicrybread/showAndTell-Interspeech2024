import {audioToJson, navigateToRoute, toggleText} from "./myJS.js";
import {drawVowelChart, drawVowels} from "./vwlChart.js";
// import {openTab} from "./practice.js";

homeNavBtn.addEventListener('click', function () {
    navigateToRoute('')
});

function playSound(audioFileId) {
    var audio = document.getElementById(audioFileId);
    console.log(audio)
    audio.play();
}


// export function showImg(evt, vwlName) {
//     // get image specific to vowel pressed
//     // Get all elements with class="tab-content" and hide them
//     const tabcontent = document.getElementsByClassName("tab-content");
//     for (let i = 0; i < tabcontent.length; i++) {
//         tabcontent[i].style.display = "none";
//     }
//
//     // Get all elements with class="tab" and remove the class "active-tab"
//     var tablinks = document.getElementsByClassName("tab");
//     for (var i = 0; i < tablinks.length; i++) {
//         tablinks[i].className = tablinks[i].className.replace(" active-tab", "");
//     }
//
//     // Show the current tab, and add an "active-content" class to the button that opened the tab
//     document.getElementById(tabName).style.display = "flex";
//     evt.currentTarget.className += " active-tab";
//     // load vowel chart for tab
//     drawVowelChart(tabName);
//     var spaPath = `/Users/hearth/PycharmProjects/showAndTell-SP24/flaskr/static/participantData/spaM0/${tabName}0/spaM0-${tabName}`;
//     var data = `{"gotAudio": "${spaPath}0-p0.wav"}`;
//     audioToJson(data,tabName,true);
//     spaPath = `/Users/hearth/PycharmProjects/showAndTell-SP24/flaskr/static/participantData/spaM0/${tabName}1/spaM0-${tabName}`;
//     data = `{"gotAudio": "${spaPath}1-p1.wav"}`;
//     audioToJson(data,tabName,true);
//
// };

document.addEventListener('DOMContentLoaded', (event) => {
    const svgId = document.getElementsByTagName('svg')[0].id;
    const id  = svgId.replace('svg-','')
    drawVowelChart(id); // Change 'pair1' to the ID of the first tab content
    const path = '../../static/audio'
    const fhPath = `${path}/frontHigh.json`;
    const bhPath = `${path}/backHigh.json`;
    const flPath = `${path}/frontLow.json`;
    const blPath = `${path}/backLow.json`;
    // var data = `{"gotAudio": "${spaPath}0-p0.wav"}`;
    try {
        drawVowels(fhPath, id);
        drawVowels(bhPath, id);
        drawVowels(flPath, id);
        drawVowels(blPath, id);
        // messageElement.textContent = ''; // Clear message or provide a success message
    } catch (error) {
        console.error('Error drawing vowels:', error);
        messageElement.textContent = 'Failed to process the file. Please check the console for more details.';
    }
});

window.playSound = playSound
window.navigateToRoute = navigateToRoute
