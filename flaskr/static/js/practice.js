 import {drawVowelChart, drawVowels} from "../../static/js/vwlChart.js";
 import {audioToJson, navigateToRoute, toggleText} from "./myJS.js";

 if (window.location.href.includes("/practice")) {
     document.addEventListener('DOMContentLoaded', (event) => {
         const tabName = 'pair1';
         drawVowelChart(tabName); // Change 'pair1' to the ID of the first tab content
         practiceTabOpen(tabName);
         // var spaPath = `/Users/hearth/PycharmProjects/showAndTell-SP24/flaskr/static/participantData/spaM0/${tabName}0/spaM0-${tabName}`;
         // var data = `{"gotAudio": "${spaPath}0-p0.wav"}`;
         // audioToJson(data,tabName,'NA',true);
         // spaPath = `/Users/hearth/PycharmProjects/showAndTell-SP24/flaskr/static/participantData/spaM0/${tabName}1/spaM0-${tabName}`;
         // data = `{"gotAudio": "${spaPath}1-p1.wav"}`;
         // audioToJson(data,tabName,'NA',true);
     });
     window.openTab = openTab

     // home nav button
     const homeNavBtn = document.getElementById('homeNavBtn');
     homeNavBtn.addEventListener('click', function () {
         navigateToRoute('')
     });
     const tutNavBtn = document.getElementById('tutorialNavBtn')
     tutNavBtn.addEventListener("click", function() {
         navigateToRoute('tutorial/vowelP1');
     });

     const p11btn = 'p11'
     const p21btn = 'p21'
     const p31btn = 'p31'
     // define strings for svg ids
     const svgP1 = 'pair1'
     const svgP2 = 'pair2'
     const svgP3 = 'pair3'
     document.getElementById(p11btn).addEventListener("click", function () {
         toggleText('the word', p11btn, svgP1,false,0);
     });
     // document.getElementById(p12btn).addEventListener("click", function () {
     //     toggleText(p12btn, svgP1);
     // });

     document.getElementById(p21btn).addEventListener("click", function () {
         toggleText('the word',p21btn, svgP2, false, 1);
     });
     // document.getElementById(p22btn).addEventListener("click", function () {
     //     toggleText(p22btn, svgP2);
     // });

     document.getElementById(p31btn).addEventListener("click", function () {
         toggleText('the word',p31btn, svgP3, false, 2);
     });
 }
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
    if (window.location.href.includes('/practice')) {
        evt.currentTarget.className += " active-tab";
        practiceTabOpen(tabName);
    };
};


export function practiceTabOpen(svgId) {
    // load vowel chart for tab
    drawVowelChart(svgId);
    const homeDirPath = '../../static/participantData/spaM0/'
    var spaPath = `${homeDirPath}${svgId}0/spaM0-${svgId}0.json`;
    // var data = `{"gotAudio": "${spaPath}0-p0.wav"}`;
    drawVowels(spaPath,svgId,true);
    spaPath = `${homeDirPath}${svgId}1/spaM0-${svgId}1.json`;
    // data = `{"gotAudio": "${spaPath}1-p1.wav"}`;
    drawVowels(spaPath,svgId,true);
}
 // Optionally open the first tab by default on page load