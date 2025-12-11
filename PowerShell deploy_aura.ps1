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
