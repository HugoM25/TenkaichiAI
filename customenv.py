import gym
from gym import spaces
import dolphin_memory_engine as dme
from const import *
import numpy as np
from utils import read_bytes

import vgamepad as vg
import time

class CustomEnv(gym.Env):
    def __init__(self):
        super(CustomEnv, self).__init__()

        # Define your custom observation space and action space

        # The data used for the observation is 
        # The P1 infos : health, ki, full power, transfo, pos x, pos y, pos z, combo, attack base cnt, attack base flag, attack ki cnt
        # The P2 infos : health, ki, full power, transfo, pos x, pos y, pos z, combo, attack base cnt, attack base flag, attack ki cnt
        # The timer

        self.observation_space = spaces.Box(low=0, high=1, shape=(23,), dtype=float)

        # The action space represent the buttons pressed on the controller there are 10 buttons (0 not pressed, > 0.5 pressed)
        # First 2 are the joystick left (up and down, left and right)
        # Then the 4 buttons (A, B, X, Y)
        # Then the 4 triggers (L, R, Z (which is select on the emulator)) 
        # And finally the C button (the right stick going down)

        self.action_space = spaces.Box(low=-1.0, high=1.0, shape=(11,), dtype=float)

        self.state = None

        self.controller = vg.VX360Gamepad()

    def reset(self):
        '''
        Reset the environment and return the initial observation
        @return : observation
        '''

        return self._get_obs()

    def step(self, actions):
        ''' 
        Implement the custom logic for one step in the environment
        @param action : the action to take
        @return : observation, reward, done, info
        '''
        prev_state = self.state


        # Apply the action to the game
        # The action is a vector of 13 values between -1 and 1
        self._apply_action(actions)
        time.sleep(0.1)

        # Return the next observation, reward, whether the episode is done, and additional info
        self.state = self._get_obs()

        # Reward the player
        reward = self._compute_reward(prev_state, self.state)

        done = False
        # Check if the game is over (health of one of the players <= 0 or timer <= 0)
        if self.state[0] <= 0 or self.state[11] <= 0 or self.state[22] <= 0: 
            done = True

        info = {}

        return self.state, reward, done, info


    def render(self, mode='human') -> None:
        '''
        Implement rendering the environment (optional)
        @param mode : the mode to render the environment
        @return : None
        '''

        pass

    def close(self):
        '''
        Implement closing the environment (optional)
        @return : None
        '''

        pass

    def _apply_action(self, actions) -> None:

        '''
        Apply the actions to the game (press the buttons)
        @param actions : the actions to apply
        @return : None
        '''
        SENSI = 0.5

        # Left joystick
        self.controller.left_joystick_float_value = (actions[0], actions[1])

        # Buttons
        self.controller.button_a = actions[2] 
        self.controller.button_b = actions[3] 
        self.controller.button_x = actions[4] 
        self.controller.button_y = actions[5] 

        # Triggers
        self.controller.left_trigger_float_value = actions[6] 
        self.controller.right_trigger_float_value = actions[7]
        self.controller.button_select = actions[8]

        # Right joystick
        self.controller.right_joystick_float_value = (actions[9])

        # Apply the actions
        self.controller.update()

    def _compute_reward(self, prev_state, curr_state) -> float:
        '''
        Compute the reward between the last observation and the current observation
        @param prev_state : the last observation
        @param curr_state : the current observation
        @return : the reward
        '''

        reward = 0

        # Reward the player
        return reward

    def _get_obs(self) -> list : 
        '''
        Get the observation from the memory 
        @return : observation
        '''

        obs = [0] * 23

        # Add P1 infos
        obs[0] = read_bytes(HEALTH_P1_MEM)
        obs[1] = read_bytes(KI_P1)
        obs[2] = read_bytes(FULL_POWER_P1)
        obs[3] = read_bytes(TRANSFO_P1)
        obs[4] = dme.read_float(POS_X_P1)
        obs[5] = dme.read_float(POS_Y_P1)
        obs[6] = dme.read_float(POS_Z_P1)
        obs[7] = dme.read_byte(COMBO_P1)
        obs[8] = dme.read_byte(ATTACK_BASE_P1_CNT)
        obs[9] = dme.read_byte(ATTACK_BASE_P1_FLAG)
        obs[10] = dme.read_byte(ATTACK_KI_P1_CNT)

        # Add P2 infos
        obs[11] = read_bytes(HEALTH_P2_MEM)
        obs[12] = read_bytes(KI_P2)
        obs[13] = read_bytes(FULL_POWER_P2)
        obs[14] = read_bytes(TRANSFO_P2)
        obs[15] = dme.read_float(POS_X_P2)
        obs[16] = dme.read_float(POS_Y_P2)
        obs[17] = dme.read_float(POS_Z_P2)
        obs[18] = dme.read_byte(COMBO_P2)
        obs[19] = dme.read_byte(ATTACK_BASE_P2_CNT)
        obs[20] = dme.read_byte(ATTACK_BASE_P2_FLAG)
        obs[21] = dme.read_byte(ATTACK_KI_P2_CNT)
        
        # Add timer info
        obs[22] = dme.read_byte(TIMER_MEM)

        return obs
