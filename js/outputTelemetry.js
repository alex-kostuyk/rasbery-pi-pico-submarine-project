var dataDisplay = document.getElementById("telemetry");


function updateDataDisplay() {
    var formattedString = "     ";

    for (var key in myObject) {
        if (myObject.hasOwnProperty(key)) {
            formattedString += key + ": " + myObject[key] + "     ";
        }
    }
    console.log(formattedString)

    dataDisplay.innerText = formattedString;   
    updateJSFIle("telemetry.js");

}

function updateJSFIle(src){
    var scriptElement = document.querySelector('script[src="'+src+'"]');

    // Remove and reinsert the script element to force a reload
    var parent = scriptElement.parentNode;
    parent.removeChild(scriptElement);

    var newScriptElement = document.createElement("script");
    newScriptElement.src = src;
    parent.appendChild(newScriptElement);
}


setInterval(updateDataDisplay, 200);