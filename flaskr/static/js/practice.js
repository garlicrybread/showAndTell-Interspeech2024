 import {drawVowelChart} from "../../static/js/vwlChart.js";

// JavaScript function to open a tab
export function openTab(evt, tabName) {
    // Get all elements with class="tab-content" and hide them
    const tabcontent = document.getElementsByClassName("tab-content");
    for (let i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Show the current tab, and add an "active-content" class to the button that opened the tab
    document.getElementById(tabName).style.display = "flex";
    evt.currentTarget.className += " active-content";
    // load vowel chart for tab
    console.log(tabName)
    drawVowelChart(tabName);

};

 // Optionally open the first tab by default on page load
 document.addEventListener('DOMContentLoaded', (event) => {
     openTab(event, 'pair1'); // Change 'pair1' to the ID of the first tab content
 });
window.openTab = openTab