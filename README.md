
<p align="center">

<h1 align="center"> TenkaichiAI (WORK IN PROGRESS) </h1>

<p align="center"> An RL Agent made to play against in the game Dragon Ball Budokai Tenkaichi 3 
</p>

<p align="center">
<img src="demo_training.gif">
</p>


Goal of this project : 

- Create a RL agent capable of winning against the CPU of the game.
- Create a program to allow players to fight against the AI in P1 V P2 mode.


## How does it work ?

This project is based on the dolphin emulator, and more specifically on this [fork](https://github.com/Felk/dolphin) that lets you use python to communicate with the emulator. 

The [dolphin_server.py](/dolphinSide/dolphin_server.py) file will be executed by this emulator and, via a socket server, will enable communication with another python script, the AI. 

The dolphin server allows you to : 
 - retrieve current emulator observations based on values in memory
 - restart the game (by loading a savestate at the start of battle) 
 - send/read controller presses.


## Setup

To set up the training configuration you need to : 


1. Get the dolphin python scripting fork [here](https://github.com/Felk/dolphin/tags) and a .iso of tenkaichi 3.

2. Clone this repository locally and make sure to change the line with the command in the [env file](AISide/tenkaichi_env.py) to make sure it works on your computer : 

```cmd 
<path_to_dolphin> --script <path_to_dolphin_server_script> --e <path_to_dbzbt3_iso>
```

## Memory locations

To easily extract data from the game, the program reads directly from the memory locations allocated by the emulator. 

Here are some of these addresses (the complete list can be found [here](/adresses_dbzbt3.csv)) :

| Name of variable | Type of variable | P1 Address | P2 Address |
| ---------------- | ---------------- | ---------- | ---------- |
| HEALTH | 2 Bytes? | 0x92334CA2 | 0x92336D42 |
| Position X | Float | 0x90F9A570 | 0x90F9B5D0 |
| Position Y | Float | 0x90F9A004 | 0x90F9B694 |
| Position Z | Float | 0x90F99F48 | 0x90F9B608 |

