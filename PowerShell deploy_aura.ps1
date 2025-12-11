# --- 1. PREREQUISITES & DOWNLOADS ---
Write-Host "1. Installing Prerequisites and Downloading Artifacts..." -ForegroundColor Green

# 1.1 Download the Python Backend Executable (The Brain)
# NOTE: This assumes you have used PyInstaller to package your prediction_api.py into an EXE.
$AuraExeUrl = "https://your-internal-repo.com/Aura/Aura_Brain.exe"
$AuraInstallDir = "C:\ProgramData\AuraDigitalTwin"
$AuraExePath = "$AuraInstallDir\Aura_Brain.exe"

If (-not (Test-Path $AuraInstallDir)) { New-Item -Path $AuraInstallDir -Type Directory }
Invoke-WebRequest -Uri $AuraExeUrl -OutFile $AuraExePath
# --- 2. CONFIGURE FIREWALL ---
Write-Host "2. Configuring Firewall Rule for Local Access..." -ForegroundColor Green

# Allows the Aura Agent to communicate with the local Aura Brain on Port 8000
New-NetFirewallRule -DisplayName "Aura Digital Twin Local API" `
    -Direction Inbound `
    -Program $AuraExePath `
    -Action Allow `
    -Protocol TCP `
    -LocalPort 8000 `
    -Profile Any
# --- 3. INSTALL VS CODE EXTENSION ---
Write-Host "3. Installing VS Code Client Extension..." -ForegroundColor Green

$VSCodeInstallPath = "C:\Program Files\Microsoft VS Code\bin\code.cmd"
$VSIXFilePath = "C:\DeploymentShare\aura-digital-twin-0.0.1.vsix" # Path to your VSIX installer

# This command installs the extension silently for the current user
& "$VSCodeInstallPath" --install-extension "$VSIXFilePath" --silent
# --- 4. CREATE PERSISTENT SERVICE/TASK (Recommended: Scheduled Task) ---
Write-Host "4. Ensuring Persistent Autostart..." -ForegroundColor Green

# Create a Scheduled Task to run the EXE on user logon and repeat on failure
$TaskName = "AuraDigitalTwinService"
$TaskAction = New-ScheduledTaskAction -Execute $AuraExePath
$TaskTrigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME

Register-ScheduledTask -TaskName $TaskName `
    -Action $TaskAction `
    -Trigger $TaskTrigger `
    -Description "Starts the Aura Digital Twin Background Monitoring Service."
# --- 5. VERIFICATION AND CLEANUP ---
Write-Host "5. Verification and Cleanup..." -ForegroundColor Green

# Start the service immediately after installation
Start-ScheduledTask -TaskName $TaskName

Write-Host "Deployment Complete! Aura Digital Twin is operational and running in the background." -ForegroundColor Yellow
# Creates a resilient, auto-restarting service on user logon
$TaskAction = New-ScheduledTaskAction -Execute $AuraExePath
$TaskTrigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME

Register-ScheduledTask -TaskName "AuraDigitalTwinService" -Action $TaskAction -Trigger $TaskTrigger
