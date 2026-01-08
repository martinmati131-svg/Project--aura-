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
