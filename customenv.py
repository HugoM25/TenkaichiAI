import gym
from gym import spaces
import dolphin_memory_engine as dme
from const import *
from utils import read_bytes

import vgamepad as vg
import time
import subprocess

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
        # First 2 are the joystick left (x, y)
        # Then the 4 buttons (A, B, X, Y)
        # Then the 4 triggers (L, R, Z (which is select on the emulator)) 
        # And finally the C button (the right stick going down)

        self.action_space = spaces.Box(low=-1.0, high=1.0, shape=(11,), dtype=float)

        self.state = None

        self.controller = vg.VX360Gamepad()

        self.life_to_lose_save = 15000
        self.life_to_lose = self.life_to_lose_save


        #Start dolphin using command line
        cmd = 'D:\Jeux\Dolphins\dolphin-scripting-preview2-x64\Dolphin.exe --script D:\Jeux\Dolphins\dolphin-scripting-preview2-x64\loop.py --e "D:\Roms\Dragon Ball Z - Budokai Tenkaichi 3 (Europe) (En,Fr,De,Es,It).rvz"'
        subprocess.Popen(cmd, shell=True)

        #Wait for dolphin to start
        time.sleep(10)


        #Hook dolphin 
        dme.hook()

        #Check the hook
        if dme.is_hooked() != True :
            print("Could not hook")
            return

    def reset(self):
        '''
        Reset the environment and return the initial observation
        @return : observation
        '''
        self.life_to_lose = self.life_to_lose_save
        # Reset should be automatic when the episode is done (thanks to the python script inside dolphin)
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

        reward = 0
        # Reward the player 
        if prev_state is not None:
            reward = self._compute_reward(prev_state, self.state)

        done = False
        # # Check if the game is over (health of one of the players <= 0 or timer <= 0)
        
        # if self.state[0] <= 0 or self.state[11] <= 0 or self.state[22] <= 0: 
        #     done = True

        # For the training, the agent is done when it lost too much life
        if self.life_to_lose <= 0 :
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

        # Left joystick
        self.controller.left_joystick_float(x_value_float=actions[0], y_value_float=actions[1])
        self.controller.right_joystick_float(x_value_float=0, y_value_float=actions[8])


        # Press a 
        if actions[2] > 0.5:
            self.controller.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        else:
            self.controller.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)

        # Press b
        if actions[3] > 0.5 :
            self.controller.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
        else:
            self.controller.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
        
        # Press x
        if actions[4] > 0.5 :
            self.controller.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
        else:
            self.controller.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)

        # Press y
        if actions[5] > 0.5 :
            self.controller.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
        else:
            self.controller.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)

        # Press L
        if actions[6] > 0.5 :
            self.controller.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
        else:
            self.controller.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)

        # Press R
        if actions[7] > 0.5 :
            self.controller.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
        else:
            self.controller.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)

        # Press select (correspond to z on the emulator)
        if actions[8] > 0.5 :
            self.controller.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK)
        else:
            self.controller.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK)

        self.controller.update()


    def _compute_reward(self, prev_state, curr_state) -> float:
        '''
        Compute the reward between the last observation and the current observation
        @param prev_state : the last observation
        @param curr_state : the current observation
        @return : the reward
        '''
        reward = 0

        # If the other player took damage, reward the player with 1
        if prev_state[11] > curr_state[11]:
            reward += 1 * (prev_state[11] - curr_state[11])/100

        # If the player took damage, reward the player with -1
        if prev_state[0] > curr_state[0]:
            reward -= 1 * (prev_state[0] - curr_state[0])/100
        
        # If the player does a combo > 2, reward the player with 10 * combo
        if prev_state[7] < curr_state[7] and curr_state[7] > 2:
            reward += 10 * (curr_state[7] - prev_state[7])/10


        # # Because of how the training env works sometimes it will start with the player almost dead so
        # # we need to reward based on life loss

        # # If the game is over, reward the player with 1000 if he won, -1000 if he lost
        # if curr_state[0] <= 0 or curr_state[11] <= 0 or curr_state[22] <= 0:
        #     # If P1 health <= P2, P2 won
        #     if curr_state[0] <= curr_state[11]:
        #         reward = -1000
        #     else:
        #         reward = 1000

        return reward

    def _get_obs(self) -> list : 
        '''
        Get the observation from the memory 
        @return : observation
        '''

        obs = [0] * 23

        # Add P1 infos
        obs[0] = read_bytes(HEALTH_P1_MEM, 2)
        obs[1] = read_bytes(KI_P1, 2)
        obs[2] = read_bytes(FULL_POWER_P1, 2)
        obs[3] = read_bytes(TRANSFO_P1, 3)
        obs[4] = dme.read_float(POS_X_P1)
        obs[5] = dme.read_float(POS_Y_P1)
        obs[6] = dme.read_float(POS_Z_P1)
        obs[7] = dme.read_byte(COMBO_P1)
        obs[8] = dme.read_byte(ATTACK_BASE_P1_CNT)
        obs[9] = dme.read_byte(ATTACK_BASE_P1_FLAG)
        obs[10] = dme.read_byte(ATTACK_KI_P1_CNT)

        # Add P2 infos
        obs[11] = read_bytes(HEALTH_P2_MEM, 2)
        obs[12] = read_bytes(KI_P2, 2)
        obs[13] = read_bytes(FULL_POWER_P2, 2)
        obs[14] = read_bytes(TRANSFO_P2, 3)
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
