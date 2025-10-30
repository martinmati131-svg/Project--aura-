

index.html
<!DOCTYPE html>
<html>
<head>
    <title>User Activity Tracker</title>
</head>
<body>
    <script src="script.js"></script>
</body>
</html>


script.js
let mouseData = [];
let keyboardData = [];
let tabData = {
    visible: true,
    focus: true
};

// Track mouse movement
document.addEventListener('mousemove', (event) => {
    mouseData.push({
        x: event.clientX,
        y: event.clientY,
        timestamp: Date.now()
    });
});

// Track mouse clicks
document.addEventListener('click', (event) => {
    mouseData.push({
        type: 'click',
        x: event.clientX,
        y: event.clientY,
        timestamp: Date.now()
    });
});

// Track keyboard input
document.addEventListener('keydown', (event) => {
    keyboardData.push({
        key: event.key,
        timestamp: Date.now()
    });
});

// Track tab visibility
document.addEventListener("visibilitychange", function() {
    if (document.visibilityState === "visible") {
        tabData.visible = true;
    } else {
        tabData.visible = false;
    }
});

// Track tab focus
window.onfocus = function() {
    tabData.focus = true;
};

window.onblur = function() {
    tabData.focus = false;
};

// Send data to API at regular intervals
setInterval(() => {
    sendDataToAPI();
}, 10000); // Send data every 10 seconds

function sendDataToAPI() {
    if (mouseData.length > 0 || keyboardData.length > 0) {
        fetch('/track', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                mouse: mouseData,
                keyboard: keyboardData,
                tab: tabData
            })
        })
        .then((response) => response.json())
        .then((data) => console.log(data))
        .catch((error) => console.error(error));

        // Clear data arrays
        mouseData = [];
        keyboardData = [];
    }
}