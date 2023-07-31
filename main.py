import dolphin_memory_engine as dme
import time 
from const import * 
import numpy as np
from pynput.keyboard import Key, Controller

MAX_STEPS_PER_EPISODE = 100000
NUM_EPISODES = 100

LEARNING_RATE = 0.1
DISCOUNT_RATE = 0.99

EXPLORATION_RATE = 1
MAX_EXPLORATION_RATE = 1
MIN_EXPLORATION_RATE = 0.01
EXPLORATION_DECAY_RATE = 0.001


rewards_all_episodes = []
episodes_done = 0 

def main() : 
    pass
       
if __name__ == "__main__" :
    main()