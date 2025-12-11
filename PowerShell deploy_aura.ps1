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
