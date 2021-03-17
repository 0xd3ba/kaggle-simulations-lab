# Kaggle Simulations Lab
Build and experiment with a wide variety of *Reinforcement-Learning* agents for various 
[Kaggle Simulation](https://www.kaggle.com/simulations) competitions, EASILY !

### Environments Supported


| Environment   |      Supported yet ?     |
|----------|:-------------|
| [Hungry Geese](https://www.kaggle.com/c/hungry-geese) |  ❌️️ |
| [Rock, Paper, Scissors](https://www.kaggle.com/c/rock-paper-scissors) |  ❌️ |
| [Connect-X](https://www.kaggle.com/c/connectx) |  ❌️ |
| [Halite by Two Sigma (Playground Edition)](https://www.kaggle.com/c/halite-iv-playground-edition) |  ❌️ |
| [Santa 2020 - The Candy Cane Contest](https://www.kaggle.com/c/santa-2020) |  ❌️ |
| [Google Research Football with Manchester City F.C.](https://www.kaggle.com/c/google-football) |  ❌️ |

## Installation Instructions

Make sure you have `Python3 (v3.5+)` installed on your system. If not installed, it will
not work.

#### 1. (Optional) Setting up a virtual environment - Highly recommended
- Make sure Python's virtual environment module is installed. If not, install it using `pip3` or `pip`
depending on your system:
```
$ pip3 install virtualenv
```
Alternatively, on Linux-based systems you can do
```
$ sudo apt install python3-venv
```
- Once installed, change to a directory where you'll like the virtual environment to be created.
Then create the virtual environment using `python3` or `python` and then activate it
```
$ python3 -m venv kaggle_sim_venv       # You can use any other name for this
$ source kaggle_sim_venv/bin/activate   # Activate the virtual environment
(kaggle_sim_venv) $ ...                 # Now activated
```

#### 2. Installing the dependencies
- Clone the repository and change to the repository's root directory
```
(kaggle_sim_venv) $ git clone https://github.com/0xd3ba/kaggle-simulations-lab
(kaggle_sim_venv) $ cd kaggle-simulations-lab
```

- Install the dependencies by using `pip3` or `pip` (virtual environment is highly
recommended for this, or else this step may mess things up)
```
(kaggle_sim_venv) $ pip3 install -r requirement.txt
```

#### 3. Starting the application
- Once all the steps above are completed, you can start the application by simply doing
```
(kaggle_sim_venv) $ python3 kaggleSimLab.py
```
<br/>