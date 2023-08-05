# TenkaichiAI
An RL Agent made to play against in the game Dragon Ball Budokai Tenkaichi 3

***This project is currently in work.*** 

Goal of this project : 

- Create a RL agent capable of winning against the CPU of the game.
- Create a program to allow players to fight against the AI in P1 V P2 mode.

Challenges of this project : 

- Connect an AI to the dolphin and making it able to play.
- Make this environment ready for RL training.
- Find out the rights parameters to make the AI learns.

(I'm not really experienced with RL training and it's my first time setting up a real-time environment. So any contribution or advice is welcome)

Work currently done : 

- I've found some of the game variable adresses by reverse engineering it, those are listed [here](https://github.com/HugoM25/TenkaichiAI/blob/main/const.py). If anyone wants to add other adresses that could be useful to the training, it would be great !

- I've setup a socket server designed to run on the dolphin's fork. It allows other the AI to interact with the emulator using the custom client API. 

- I'm currently creating the AI setup for training.




