const name = ''
let urlPath;
if (window.location.href.includes("/pronunciationVis/")) {
    urlPath = `/pronunciationVis/${name}`; // Set for remote
} else {
    urlPath = "/"+name; // Set for local
}

var button = document.getElementById('btnUserId')
const calNavBtn  = document.getElementById('calibrationNavBtn')
const tutNavBtn = document.getElementById('tutorialNavBtn')
const pracNavBtn = document.getElementById('practiceNavBtn')

button.addEventListener("click", saveUserId);
calNavBtn.addEventListener("click", function() {
    navigateToRoute('vowelCalibration');
});
tutNavBtn.addEventListener("click", function() {
    navigateToRoute('tutorial/vowelP1');
});
pracNavBtn.addEventListener("click", function() {
    navigateToRoute('practice/chart');
});


async function saveUserId() {
    // Retrieve the value of the input field with id "userId"
    const userId = document.getElementById("textInputId").value;
    const path = `${urlPath}api/saveUserId`
    fetch(path, {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify(userId)
    })
}

async function navigateToRoute(location) {
    // Retrieve the value of the input field with id "userId"
    console.log(location)
    const path = `${urlPath}${location}`
    window.location.href = path
}
