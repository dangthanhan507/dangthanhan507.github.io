---
layout: default
title: Isaac Setup
parent: Isaac
nav_order: 1
---

# Setting up Isaac

We are starting off from IsaacGymEnvs which uses IsaacGym 4. This IsaacGym only supports Ubuntu 20.04 and Ubuntu 18.04.
In order to set this up on my machine, I will have to use Docker.

Check out this [link](https://docs.robotsfan.com/isaacgym/index.html) for getting into IsaacGym 

## Docker Setup on Desktop

Check out these tutorials:
- [Install](https://docs.docker.com/engine/install/ubuntu/)
- [PostInstall](https://docs.docker.com/engine/install/linux-postinstall/)

## Get NVIDIA Container Toolkit

Check this out for setting up an nvidia container for docker.
- [link](https://docs.omniverse.nvidia.com/isaacsim/latest/installation/install_container.html)

## Setup NGC Account

Need to get an NGC account to download the container from this github [repo](https://github.com/NVIDIA-Omniverse/IsaacSim-dockerfiles?tab=readme-ov-file)
- [link](https://ngc.nvidia.com/signin)

Generate API Key from NGC Account
- [link](https://docs.nvidia.com/ngc/gpu-cloud/ngc-user-guide/index.html#generating-api-key)

Current API Key
- password: ```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```
- Username: ```$oauthtoken```

Run this command to login

```
docker login nvcr.io
```
and enter the username and password when prompted.

## Setup Isaac Gym

Follow instructions from this [link](https://medium.com/@piliwilliam0306/install-isaac-gym-on-ubuntu-22-04-8ebf4b86e6f7).
Before running python scripts, put this in your bashrc file: 

```export LD_LIBRARY_PATH=/home/andang/anaconda3/envs/rlgpu/lib```

[Link](https://docs.robotsfan.com/isaacgym/index.html) to Isaac Gym Documentation (also displayed in docs folder when you download Isaac Gym)


## Anaconda Management

Using the tutorial from the isaacgym download, you get an ```rlgpu``` environment.

However, we will run into issues with running ```train.py``` in IsaacGymEnvs.

We upgrade our pytorch version (originally 1.8.1) as follows:

<!-- ```bash
python3 -m pip install torch==1.8.1 --no-cache-dir --force-reinstall --index-url https://download.pytorch.org/whl/cu113
``` -->

```bash
python3 -m pip install torch==1.13.1
```

## Jayjun's !Happiness

Branch overview:

- Main (vitascope)
    - 8 camera support
    - texture support
    - point cloud support
    - +2 cameras support for tactile sensor
    - multiple environemnts semi-support
    - waypoint following (follow $$\text{SE}(3)$$ pose)
- OG (rl + insertion)
    - 3 cameras rgbd
    - 2 tactile cameras
    - shear + rgb
    - rl_games library for (RL training)

Start off with these files in OG Branch:
- Run teacher/run_train_state.sh (to get something running)
- distill_expert_to_tactile_rgb_with_delta_ee_to_socket.py
- distill_expert_to_tactile_shear_with_delta_ee_to_socket.py

Dig into this file:
- tacsl_sensors folder

Vitascope Library
- vitascope/vitascope/sim
- getting tactile point clouds
- segmentation on normal cameras

TacSL can't get good FT from wrist

NOTE: If you want to render, make sure you set force_render to True in your train.py. Here is a sample command to run:

```bash
python3 train.py task=Cartpole headless=False force_render=True
```