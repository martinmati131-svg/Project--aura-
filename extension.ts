import * as vscode from 'vscode';
// Use node-fetch if global fetch is unavailable or for wider compatibility
import fetch from 'node-fetch'; 

const API_URL = 'http://127.0.0.1:8000/predict_state/';
const POLL_INTERVAL_MS = 60000; // Poll every 60 seconds

let predictionStatusBarItem: vscode.StatusBarItem;

// --- 1. CORE PREDICTION FUNCTION ---
async function fetchPrediction(context: vscode.ExtensionContext) {
    try {
        // A. Gather VS Code Context (Active App and Activity Proxy)
        const currentActivity = getActivityMetrics();

        // B. Prepare the Payload (Must match the FastAPI Pydantic Model)
        const payload = {
            active_app: currentActivity.active_app, // Always 'VSCode' in this context
            key_count: currentActivity.key_count,
            mouse_distance: currentActivity.mouse_distance,
            calendar_state: "unknown", // The Python service handles the Calendar API call
        };

        // C. Fetch Prediction from Local Service
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });

        if (!response.ok) {
            throw new Error(`API returned status ${response.status}`);
        }

        // D. Process the Response (e.g., { "predicted_state": "focused", "confidence": 0.92 })
        const data = await response.json();
        
        // E. Update the UI
        updateStatusBar(data.predicted_state, data.confidence);

    } catch (error) {
        console.error('Aura Prediction Error:', error);
        updateStatusBar('⚠️ Aura Disconnected', 0); // Show error if service is down
    }
}


// --- 2. ACTIVITY PROXY (Simple Implementation) ---
function getActivityMetrics() {
    // VS Code extensions cannot directly read low-level OS key/mouse events.
    // We use proxies: total text in the active file as a rough proxy for "work being done."
    let keyCountProxy = 0;
    let mouseDistanceProxy = 0;

    const editor = vscode.window.activeTextEditor;
    if (editor) {
        // Simple proxy: Longer file size = more effort/activity
        keyCountProxy = editor.document.getText().length;
        
        // Another proxy: The last time the document was saved or changed
        // (For simplicity here, we'll just return a base value)
        mouseDistanceProxy = 500; 
    }
    
    return {
        active_app: 'VSCode',
        key_count: keyCountProxy,
        mouse_distance: mouseDistanceProxy
    };
}


// --- 3. STATUS BAR UI UPDATE ---
function updateStatusBar(state: string, confidence: number) {
    const icon = state === 'focused' ? '🧠' : state === 'distracted' ? '☕' : '👥';
    const confidencePercent = Math.round(confidence * 100);
    
    predictionStatusBarItem.text = `${icon} Aura: ${state} (${confidencePercent}%)`;
    predictionStatusBarItem.tooltip = `Prediction powered by Attention and Memory.`;
    predictionStatusBarItem.show();
}


// --- 4. EXTENSION ACTIVATION (The Loop Starter) ---
export function activate(context: vscode.ExtensionContext) {
    console.log('Aura Digital Twin Extension is now active!');

    // Create the status bar item (UI)
    predictionStatusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    context.subscriptions.push(predictionStatusBarItem);
    
    // Initial display
    updateStatusBar('Loading Aura...', 0);

    // Run the prediction function immediately
    fetchPrediction(context); 

    // Set the continuous prediction loop using setInterval
    const intervalId = setInterval(() => fetchPrediction(context), POLL_INTERVAL_MS);
    
    // Ensure the interval is cleaned up when the extension is deactivated
    context.subscriptions.push({
        dispose: () => clearInterval(intervalId)
    });
}
// ------------------------------------------------------------------
