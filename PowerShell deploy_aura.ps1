# --- 1. PREREQUISITES & DOWNLOADS ---
Write-Host "1. Installing Prerequisites and Downloading Artifacts..." -ForegroundColor Green

# 1.1 Download the Python Backend Executable (The Brain)
# NOTE: This assumes you have used PyInstaller to package your prediction_api.py into an EXE.
$AuraExeUrl = "https://your-internal-repo.com/Aura/Aura_Brain.exe"
$AuraInstallDir = "C:\ProgramData\AuraDigitalTwin"
$AuraExePath = "$AuraInstallDir\Aura_Brain.exe"

If (-not (Test-Path $AuraInstallDir)) { New-Item -Path $AuraInstallDir -Type Directory }
Invoke-WebRequest -Uri $AuraExeUrl -OutFile $AuraExePath
