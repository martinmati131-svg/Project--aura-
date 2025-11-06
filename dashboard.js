// dashboard.js
// This script powers the Aura Platform Dashboard

// --- 1. Get references to our HTML elements ---
const statusElement = document.getElementById("status-display");
const confidenceElement = document.getElementById("confidence");
const rssContentElement = document.getElementById("rss-content");
const shieldButton = document.getElementById("shield-toggle");

// --- 2. Configuration ---
const AURA_API_URL = "http://127.0.0.1:5000/api/v1/aura/status";
const AURA_COMMAND_URL = "http://127.0.0.1:5000/api/v1/aura/command";

// RSS Feed (Using a CORS proxy to avoid security errors)
const RSS_FEED_URL = "https://feeds.arstechnica.com/arstechnica/index";
const CORS_PROXY_URL = "https://api.allorigins.win/raw?url=";


// --- 3. Function to get Aura Brain status ---
async function getAuraStatus() {
    try {
        // This "fetches" the data from our local Python API
        const response = await fetch(AURA_API_URL);
        const data = await response.json();
        
        const state = data.prediction || 'initializing';
        const confidence = (data.confidence * 100).toFixed(1);

        // Update the HTML text
        statusElement.textContent = state.toUpperCase();
        confidenceElement.textContent = confidence;

        // Update the CSS class to change the color
        statusElement.className = state; // We'll add a base class in the CSS

    } catch (error) {
        // If the Python "brain" isn't running
        console.error("Could not connect to Aura brain:", error);
        statusElement.textContent = "DISCONNECTED";
        statusElement.className = "distracted"; // Use a danger color
        confidenceElement.textContent = "??";
    }
}

// --- 4. Function to get the RSS News Feed ---
async function getRssFeed() {
    rssContentElement.innerHTML = "Loading feed...";
    try {
        const response = await fetch(CORS_PROXY_URL + encodeURIComponent(RSS_FEED_URL));
        const str = await response.text();
        const data = new window.DOMParser().parseFromString(str, "text/xml");

        let html = "";
        const items = data.querySelectorAll("item");

        // Loop through the first 5 news items
        for (let i = 0; i < 5; i++) {
            const item = items[i];
            if (!item) continue;

            const title = item.querySelector("title").textContent;
            const link = item.querySelector("link").textContent;
            
            html += `
                <div class="news-item">
                    <a href="${link}" target="_blank" rel="noopener noreferrer">${title}</a>
                </div>
            `;
        }
        rssContentElement.innerHTML = html;

    } catch (error) {
        console.error("Could not fetch RSS feed:", error);
        rssContentElement.innerHTML = "Error loading news feed.";
    }
}

// --- 5. Function to send a command to the Brain ---
async function sendAuraCommand(command) {
    try {
        const response = await fetch(AURA_COMMAND_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'command': command })
        });
        const data = await response.json();
        console.log("Command response:", data);

    } catch (error) {
        console.error("Could not send command to Aura brain:", error);
    }
}

// --- 6. Run Everything ---

// Add a click listener to our new button
shieldButton.addEventListener('click', () => {
    console.log("Toggle Shield button clicked!");
    sendAuraCommand("TOGGLE_SHIELD");
});

// Check the brain status every 3 seconds
setInterval(getAuraStatus, 3000);

// Run both functions once immediately when the page loads
getAuraStatus();
getRssFeed();
