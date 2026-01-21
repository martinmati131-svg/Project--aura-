from omni.isaac.lab.envs import ManagerBasedRLEnv, ManagerBasedRLEnvCfg
from aura import SentinelBrain  # Your modular brain!

class AuraEnv(ManagerBasedRLEnv):
    """The RL Environment where GR00T is tuned."""
    
    def __init__(self, cfg: ManagerBasedRLEnvCfg, **kwargs):
        super().__init__(cfg, **kwargs)
        
        # Initialize the Aura Sentinel as the 'Supervisor'
        self.sentinel = SentinelBrain(self.sim.stage)

    def get_observations(self):
        """Feeding the robot its 'Aura' sensors."""
        obs = {
            "policy": self.robot.get_state(),
            "sentinel_signal": self.sentinel.process_frame(self.sim.current_time)
        }
        return obs

    def get_rewards(self):
        """Using the Sentinel to grade the robot."""
        # This calls the custom reward logic we discussed!
        return self.sentinel.calculate_reward()

from gr00t.eval.policy import Gr00tPolicy

class AuraGrootEnv(ManagerBasedRLEnv):
    def __init__(self, cfg):
        super().__init__(cfg)
        # Load the N1.6-3B weights from Hugging Face
        self.policy = Gr00tPolicy.from_pretrained("nvidia/GR00T-N1.6-3B")
        self.action_horizon = 8 # Process 8 frames of motion at once

    def get_action(self, obs):
        # N1.6 takes images + text instructions
        instruction = "Safely move the pallet to Zone A"
        action_chunks = self.policy.predict(obs['image'], instruction)
        
        # The Sentinel checks the ENTIRE chunk for safety violations
        safe_action = self.sentinel.verify_trajectory(action_chunks)
        return safe_action
