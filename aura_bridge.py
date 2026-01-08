import sys
import os
from omni.isaac.kit import SimulationApp

# 1. Start the App
simulation_app = SimulationApp({"headless": False})

# 2. Add the path to your 'Project--aura-' repo so Python can find the brain
# Update this path to where your aura repo is located
AURA_REPO_PATH = "../Project--aura-" 
sys.path.append(AURA_REPO_PATH)

# Import your brain (assuming the file has a class or main logic)
try:
    import sanitel_api # Note: Python imports use underscore, check your filename
except ImportError:
    print(">> Error: Could not find sanitel-api.py in the provided path.")

from omni.isaac.core import World

# 3. Initialize Simulation
world = World(stage_units_in_meters=1.0)
stage = world.stage

# 4. The Main Loop (The Bridge)
print(">> Aura Intelligence: Brain Sync Active.")
while simulation_app.is_running():
    world.step(render=True)
    
    # CALL BACK TO THE BRAIN:
    # Example: Pass current simulation data to your Sentinel API
    # logic_state = sanitel_api.process_frame(stage) 
    
    # If the brain triggers an 'Alert', change the Sentinel light to Red
    # if logic_state == "ALERT":
    #    trigger_visual_alert(stage)

simulation_app.close()
