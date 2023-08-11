import gymnasium as gym
from gymnasium import spaces
import subprocess
import time
import dolphin_client_api as dca
from controller_class import GCInputs


class TenkaichiEnv(gym.Env):
    def __init__(self):
        super(TenkaichiEnv, self).__init__()

        # Define your custom observation space and action space

        # The data used for the observation is 
        # timer, Health Player 1, Health Player 2, X Player 1, Y Player 1, Z Player 1, X Player 2, Y Player 2, Z Player 2, 
        # Attack base cnt P1, Attack base cnt P2, Attack ki cnt P1, Attack ki cnt P2, Damage combo taken by P1, Damage combo taken by P2
        self.observation_space = spaces.Box(low=-1.0, high=1.0, shape=(15,), dtype=float)

        # The action space represent the buttons pressed on the controller there are 13 buttons
        # Stick X, Stick Y, C-Stick X, C-Stick Y, L-Analog, R-Analog, L, R, A, B, X, Y, Z

        self.action_space = spaces.Box(low=-1.0, high=1.0, shape=(13,), dtype=float)

        self.state = None

        self.controller = GCInputs()

        #Start dolphin using command line
        cmd = 'D:\Jeux\Dolphins\dolphin-scripting-preview2-x64\Dolphin.exe --script D:\ProjetsPersos\TenkaichiAI\dolphinSide\dolphin_server.py --e "D:\Roms\Dragon Ball Z - Budokai Tenkaichi 3 (Europe) (En,Fr,De,Es,It).rvz"'
        subprocess.Popen(cmd, shell=True)

        #Wait for dolphin to start
        time.sleep(3)


    def reset(self, seed=None, return_info=None, options=None):
        '''
        Reset the environment and return the initial observation
        @return : observation
        '''
        dca.reset()

        self.state = self._get_obs()

        return self.state, None

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

        self.controller =  GCInputs()

        reward = 0
        # Reward the player 
        if prev_state is not None:
            reward = self._compute_reward(prev_state, self.state)

        done = False

        # Check if the game is over (health of one of the players <= 0 or timer <= 0)
        if self.state[0] <= 0 or self.state[1] <= 0 or self.state[2] <= 0: 
            done = True


        info = {}
        truncated = False

        return self.state, reward, done, truncated, info


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
        try : 
            # The action is a vector of 13 values between -1 and 1
            # The joystick is at rest at 128 and can go from 0 to 255
            self.controller.StickX = int((actions[0] + 1) * 127.5)
            self.controller.StickY = int((actions[1] + 1) * 127.5)

            # The C button is the same as the joystick
            self.controller.CStickX = int((actions[2] + 1) * 127.5)
            self.controller.CStickY = int((actions[3] + 1) * 127.5)

            # The triggers can go from 0 to 255
            self.controller.TriggerLeft = int((actions[4] + 1) * 127.5)
            self.controller.TriggerRight = int((actions[5] + 1) * 127.5)

            self.controller.L = int(actions[6] > 0.5)
            self.controller.R = int(actions[7] > 0.5)

            self.controller.A = int(actions[8] > 0.5)
            self.controller.B = int(actions[9] > 0.5)
            self.controller.X = int(actions[10] > 0.5)
            self.controller.Y = int(actions[11] > 0.5)
            self.controller.Z = int(actions[12] > 0.5)

            # Send the controller inputs to dolphin
            dca.send_inputs(self.controller)
        except:
            print("Error while applying actions")
            print(actions)

    def _compute_reward(self, prev_state, curr_state) -> float:
        '''
        Compute the reward between the last observation and the current observation
        @param prev_state : the last observation
        @param curr_state : the current observation
        @return : the reward
        '''
        reward = 0

        # If the player took damage, reward him with -1
        if prev_state[13] < curr_state[13] :
            reward = -10
        
        # If the player dealt damage, reward him with 1
        if  prev_state[14] < curr_state[14]:
            reward = 10

        # If the game is over, reward the player with 1000 if he won, -1000 if he lost
        if curr_state[0] <= 0 or curr_state[1] <= 0 or curr_state[2] <= 0:
            # If P1 health <= P2, P2 won
            if curr_state[1] <= curr_state[2]:
                reward = -1000
            else:
                reward = 1000

        return reward

    def _get_obs(self) -> list : 
        '''
        Get the observation from the memory 
        @return : observation
        '''
        obs = dca.get_observation()
        return obs
