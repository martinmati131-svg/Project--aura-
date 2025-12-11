import * as vscode from 'vscode';
// If you have issues with import, you can use 'const fetch = require("node-fetch");'
// or rely on the global fetch if using Node 18+ inside VS Code.
// For this snippet, we assume standard global fetch is available (VS Code 1.80+).

const API_URL = 'http://127.0.0.1:8000/predict_state/';
const POLL_INTERVAL = 60000; // 60 seconds

let myStatusBarItem: vscode.StatusBarItem;
let intervalId: NodeJS.Timeout | undefined;

export function activate(context: vscode.ExtensionContext) {
	console.log('🧠 Aura Digital Twin is active!');

	// 1. Create Status Bar Item
	myStatusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
	myStatusBarItem.text = "$(circle-outline) Aura: Initializing...";
	myStatusBarItem.show();
	context.subscriptions.push(myStatusBarItem);

	// 2. Start the Loop
	fetchPrediction(); // Run once immediately
	intervalId = setInterval(fetchPrediction, POLL_INTERVAL);

	// 3. Register Command for Manual Feedback (Neuroplasticity)
	let feedbackCmd = vscode.commands.registerCommand('aura.giveFeedback', async () => {
		const state = await vscode.window.showQuickPick(['focused', 'distracted', 'collaborating'], {
			placeHolder: 'What is your actual state right now?'
		});
		if (state) {
			sendFeedback(state);
		}
	});
	context.subscriptions.push(feedbackCmd);
}

async function fetchPrediction() {
	try {
		// Mock metrics - In a real build, you'd calculate these from vscode events
		const payload = {
			active_app: "VSCode",
			key_count: 300,        // Simple proxy: assume moderate activity
			mouse_distance: 100,   // Simple proxy
			calendar_state: "free" // Service will override this with real calendar data
		};

		const response = await fetch(API_URL, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify(payload)
		});

		if (!response.ok) throw new Error('Service Error');

		const data: any = await response.json();
		updateStatusBar(data.predicted_state, data.confidence);

	} catch (error) {
		myStatusBarItem.text = "$(warning) Aura: Offline";
		myStatusBarItem.tooltip = "Ensure AuraService.exe is running.";
	}
}

function updateStatusBar(state: string, confidence: number) {
	// Icons: https://code.visualstudio.com/api/references/icons-in-labels
	let icon = "$(circle-large-outline)";
	if (state === 'focused') icon = "$(rocket)";
	if (state === 'distracted') icon = "$(bell)";
	if (state === 'collaborating') icon = "$(organization)";

	const percent = Math.round(confidence * 100);
	myStatusBarItem.text = `${icon} Aura: ${state.toUpperCase()} (${percent}%)`;
	myStatusBarItem.tooltip = `AI Confidence: ${percent}%`;
}

async function sendFeedback(trueState: string) {
	// Neuroplasticity: Send correction to the brain
	// You would need to add a /feedback/ endpoint to your FastAPI service to handle this
	// For now, we just show a message.
	vscode.window.showInformationMessage(`🧠 Aura is learning that you are: ${trueState}`);
}

export function deactivate() {
	if (intervalId) clearInterval(intervalId);
}
// extension.ts

function updateStatusBar(state: string, confidence: number, risk: string, alerts: string[]) {
    
    // 🚨 PRIORITY 1: SECURITY ALERT
    if (risk === 'CRITICAL') {
        myStatusBarItem.text = "$(alert) Aura: SECURITY BREACH";
        myStatusBarItem.color = "#FF0000"; // Red text
        myStatusBarItem.tooltip = `⚠️ ALERTS:\n${alerts.join('\n')}`;
        myStatusBarItem.show();
        
        // Optional: Pop up a warning message box
        vscode.window.showErrorMessage(`🚨 SECURITY ALERT: ${alerts[0]}`);
        return;
    }

    // ⚠️ PRIORITY 2: SUSPICIOUS
    if (risk === 'medium') {
        myStatusBarItem.color = "#FFA500"; // Orange text
    } else {
        myStatusBarItem.color = undefined; // Default color
    }

    // NORMAL OPERATION
    let icon = "$(circle-large-outline)";
    if (state === 'focused') icon = "$(rocket)";
    if (state === 'distracted') icon = "$(bell)";
    if (state === 'collaborating') icon = "$(organization)";

    const percent = Math.round(confidence * 100);
    myStatusBarItem.text = `${icon} Aura: ${state.toUpperCase()} (${percent}%)`;
    myStatusBarItem.tooltip = `Risk Level: ${risk}\nVision: ${alerts.length > 0 ? alerts[0] : 'Normal'}`;
    myStatusBarItem.show();
}

// Update the fetchPrediction function to pass the new fields
async function fetchPrediction() {
    // ... (fetch logic) ...
    const data: any = await response.json();
    
    // Pass new security fields to the UI updater
    updateStatusBar(
        data.predicted_state, 
        data.confidence, 
        data.security_risk, 
        data.security_alerts
    );
}

// extension.ts (Example Registration Function)

const EMPLOYEE_ID = "TEST_USER_AURA_101"; // Placeholder for the real local ID

async function registerAuraUser() {
    try {
        const response = await fetch('http://localhost:8000/register_user/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ employee_id: EMPLOYEE_ID })
        });
        
        const data = await response.json();
        const anonymizedId = data.anonymized_id;
        
        // CRITICAL STEP: The client saves the HASH, not the raw ID.
        // This hash is then used for ALL subsequent calls (like /log_insight/)
        // in place of the raw ID.
        vscode.workspace.getConfiguration().update('aura.anonymizedId', anonymizedId, true);
        
        console.log(`User registered with safe ID: ${anonymizedId}`);
    } catch (error) {
        console.error("Aura Registration Failed:", error);
    }
}
