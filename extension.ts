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
