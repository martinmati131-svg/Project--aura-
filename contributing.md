Project Aura: Contribution Guide
​Welcome to the Aura Sentinel research team! We are building a safety-first future for robotics, and we value your input.
​1. How to Contribute
​Bug Reports: If the Sentinel API fails to catch a voltage drop or a ROS 2 node crashes, please open an Issue with your hardware specs (e.g., Pi 5, 8GB) and a snippet of the motor logs.
​Feature Requests: Want to add support for Jetson Orin or new VLA action chunks? Start a Discussion before submitting a PR.

Code Contributions:
​Fork the repository.
​Create a feature branch (git checkout -b feature/aura-upgrade).
​Ensure your Python code follows PEP8 and includes docstrings for any new Sentinel logic.
​Submit a Pull Request (PR) with a clear description of the changes.

Development Standards
​To maintain the integrity of our safety-governance layer:
​Testing: All new bridge nodes must be tested in NVIDIA Isaac Sim using the aura_layout_switcher before being committed.
​Commit Messages: Use descriptive titles like fix: resolve GPIO pin conflict or feat: add Vertex AI telemetry sync.