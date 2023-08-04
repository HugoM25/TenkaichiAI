# TenkaichiAI
An RL Agent made to play against in the game Dragon Ball Budokai Tenkaichi 3

***This project is currently in work.*** 

Challenges of this project : 

- Connect an AI to the dolphin and making it able to play.
- Make this environment ready for RL training.
- Find out the rights parameters to make the AI learns.

(I'm not really experienced with RL training and it's my first time setting up an real-time environment. So any contribution or advice is welcome)



Work currently done : 

- I've found some of the game variable adresses, those are listed [here](https://github.com/HugoM25/TenkaichiAI/blob/main/const.py). If anyone wants to add other adresses that could be useful to the training, it would be great !

- The way the program will interact with the emulator is currently using `dolphin-memory-engine` to retrieve the data of the game and `vgamepad` to send the inputs. The env will reset using the dolphin python scriptable fork by Felk, using socket message to reset the env (aka loading a save state).

- Currently adding option to supervise the training of the agent before sending it to train on its own. I hope to gain some training time using this method. To train the agent I use a [custom recorder script](https://github.com/HugoM25/TenkaichiAI/blob/main/recorder.py) and train it using [this script](https://github.com/HugoM25/TenkaichiAI/blob/main/supervised_train.py).

Goal of this project : 

- Create a RL agent capable of winning against the CPU of the game.
- Create a program to allow players to fight against the AI in P1 V P2 mode.

