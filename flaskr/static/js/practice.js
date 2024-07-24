 import {drawVowelChart, drawVowels} from "../../static/js/vwlChart.js";
 import {audioToJson, navigateToRoute, toggleText} from "./myJS.js";

 // home nav button
 const homeNavBtn = document.getElementById('homeNavBtn');
 homeNavBtn.addEventListener('click', function () {
     navigateToRoute('')
 });


 const p11btn = 'p11'
 const p12btn = 'p12'
 const p21btn = 'p21'
 const p22btn = 'p22'
 const p31btn = 'p31'
 const p32btn = 'p32'
 // define strings for svg ids
 const svgP1 = 'pair1'
 const svgP2 = 'pair2'
 const svgP3 = 'pair3'
 document.getElementById(p11btn).addEventListener("click", function () {
     toggleText(p11btn, svgP1);
 });
 // document.getElementById(p12btn).addEventListener("click", function () {
 //     toggleText(p12btn, svgP1);
 // });

 document.getElementById(p21btn).addEventListener("click", function () {
     toggleText(p21btn, svgP2);
 });
 // document.getElementById(p22btn).addEventListener("click", function () {
 //     toggleText(p22btn, svgP2);
 // });

 document.getElementById(p31btn).addEventListener("click", function () {
     toggleText(p31btn, svgP3);
 });
 // document.getElementById(p32btn).addEventListener("click", function () {
 //     toggleText(p32btn, svgP3);
 // });

// JavaScript function to open a tab
export function openTab(evt, tabName) {
    // Get all elements with class="tab-content" and hide them
    const tabcontent = document.getElementsByClassName("tab-content");
    for (let i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tab" and remove the class "active-tab"
      var tablinks = document.getElementsByClassName("tab");
      for (var i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active-tab", "");
      }

    // Show the current tab, and add an "active-content" class to the button that opened the tab
    document.getElementById(tabName).style.display = "flex";
    evt.currentTarget.className += " active-tab";
    // load vowel chart for tab
    drawVowelChart(tabName);
    var spaPath = `/Users/hearth/PycharmProjects/showAndTell-SP24/flaskr/static/participantData/spaM0/${tabName}0/spaM0-${tabName}`;
    var data = `{"gotAudio": "${spaPath}0-p0.wav"}`;
    audioToJson(data,tabName,'NA',true);
    spaPath = `/Users/hearth/PycharmProjects/showAndTell-SP24/flaskr/static/participantData/spaM0/${tabName}1/spaM0-${tabName}`;
    data = `{"gotAudio": "${spaPath}1-p1.wav"}`;
    audioToJson(data,tabName,'NA',true);
};

 // Optionally open the first tab by default on page load
 document.addEventListener('DOMContentLoaded', (event) => {
     const tabName = 'pair1';
     drawVowelChart(tabName); // Change 'pair1' to the ID of the first tab content
     var spaPath = `/Users/hearth/PycharmProjects/showAndTell-SP24/flaskr/static/participantData/spaM0/${tabName}0/spaM0-${tabName}`;
     var data = `{"gotAudio": "${spaPath}0-p0.wav"}`;
     audioToJson(data,tabName,'NA',true);
     spaPath = `/Users/hearth/PycharmProjects/showAndTell-SP24/flaskr/static/participantData/spaM0/${tabName}1/spaM0-${tabName}`;
     data = `{"gotAudio": "${spaPath}1-p1.wav"}`;
     audioToJson(data,tabName,'NA',true);
 });
window.openTab = openTab