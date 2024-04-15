const name = ''
let urlPath;
if (window.location.href.includes("/pronunciationVis/")) {
    urlPath = `/pronunciationVis/${name}`; // Set for remote
} else {
    urlPath = "/"+name; // Set for local
}

var button = document.getElementById('btnUserId')

button.addEventListener("click", saveUserId);
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