
# Project Aura: Intelligence Governed 🤖🛡️
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![NVIDIA Isaac Sim](https://img.shields.io/badge/Simulation-Isaac_Sim_2024.1-green.svg)](https://developer.nvidia.com/isaac-sim)
[![AdSense Ready](https://img.shields.io/badge/Status-Review_Ready-orange.svg)](#)

**Project Aura** is a next-generation robotics governance framework designed to bridge the "Sim-to-Real" gap. By integrating the **GR00T N1.6** foundation model with our proprietary **Sentinel API**, Aura provides proactive safety and agentic reasoning for humanoid and industrial robots.


---

## 🚀 Quick Start (GitHub Codespaces)

Get a fully configured Aura environment running in seconds. No local drivers required.

1. **Click the Button:** Click `Code` > `Codespaces` > `Create codespace on main`.
2. **Auto-Install:** The `.devcontainer` will automatically install Python 3.11, CUDA headers, and the requirements from `requirements.txt`.
3. **Launch Simulation:**
   ```bash
   python aura_env.py --headless

# Aura Intelligence: Project Aura 🤖
> Research into Edge-AI, ROS 2 Jazzy, and VLA model integration.

## 🚀 Overview
Project Aura focuses on deploying the **GR00T N1.6-3B** model on **Raspberry Pi 5** for precision pallet handling. This repository contains the hardware configurations, telemetry sync logic, and LoRA fine-tuning parameters.

## 🛠 Tech Stack
* **Hardware:** Raspberry Pi 5, NEMA 17 Stepper Motors.
* **Middleware:** ROS 2 Jazzy, Sentinel API.
* **Cloud:** Google Cloud (GCS & Vertex AI).
* **AI:** NVIDIA GR00T-N1.6-3B (Vision-Language-Action).

## 📂 Key Documentation
For detailed engineering logs and business strategy (M2M), visit our official research blog:
👉 [Aura Intelligence Blog](https://auraintelligence1.blogspot.com/)

## 📜 License
Licensed under the **Apache License 2.0**. See the `LICENSE` file for details.

## ## Project Aura API: Getting Started
To run the local backend for hardware telemetry:

1. Install dependencies: `pip install fastapi uvicorn`
2. Start the server:
   ```bash
   uvicorn sanitel-api:app --port 3000



