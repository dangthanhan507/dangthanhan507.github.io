---
layout: default
title: Isaac Tutorial
parent: Isaac
nav_order: 1
---

# Isaac Gym Notes (for An)
 
This is the breakdown of the Isaac Gym codebase. Here are important links:
- [Documentation](https://docs.robotsfan.com/isaacgym/)
- [IsaacGym Forum](https://forums.developer.nvidia.com/c/robotics-edge-computing/isaac/isaac-gym/322)

---

## Vectorized Environments

IsaacGym environments are vectorized environments. This means they can run multiple environments in parallel. For us, this means that it follows the OpenAI Gym API for vectorized environments:


Here's example code from IsaacGymEnvs:

```python
import isaacgym
import isaacgymenvs
import torch

num_envs = 2000

envs = isaacgymenvs.make(
	seed=0, 
	task="Ant", 
	num_envs=num_envs, 
	sim_device="cuda:0",
	rl_device="cuda:0",
)
print("Observation space is", envs.observation_space)
print("Action space is", envs.action_space)
obs = envs.reset()
for _ in range(20):
	random_actions = 2.0 * torch.rand((num_envs,) + envs.action_space.shape, device = 'cuda:0') - 1.0
	envs.step(random_actions)
```

Here's another example from the Gym API site:

```python
envs = gym.vector.make("CartPole-v1", num_envs=3)
envs.reset()
actions = np.array([1, 0, 1])
observations, rewards, dones, infos = envs.step(actions)
```

Here's an example implementation of a Gym Environment:

```python
class DictEnv(gym.Env):
    observation_space = gym.spaces.Dict({
        "position": gym.spaces.Box(-1., 1., (3,), np.float32),
        "velocity": gym.spaces.Box(-1., 1., (2,), np.float32)
    })
    action_space = gym.spaces.Dict({
        "fire": gym.spaces.Discrete(2),
        "jump": gym.spaces.Discrete(2),
        "acceleration": gym.spaces.Box(-1., 1., (2,), np.float32)
    })

    def reset(self):
        return self.observation_space.sample()

    def step(self, action):
        observation = self.observation_space.sample()
        return (observation, 0., False, {})
```

no extra methods are needed. We mainly focus on `reset` and `step` and make sure we define `observation_space` and `action_space` correctly. 

---

## 1. Simulation Setup

### 1.1 Gym
CoreAPI is located in `isaacgym.gymapi'. All Gym API functions are accessed by `Gym` object acquired by the following code:

```python
from isaacgym import gymapi
gym = gymapi.acquire_gym()
```

### 1.2 Sim

```python
sim_params = gymapi.SimParams()
sim = gym.create_sim(
    compute_device_id,
    graphics_device_id,
    gymapi.SIM_PHYSX,
    sim_params
)
```

we use `create_sim` to create a simulation which contains graphics context and physics context. Allows us to load assets, create environments, and interact with simulation.

We have two choices for simulation:
- `gymapi.SIM_PHYSX` - PhysX simulation: robust rigid body and articulation (CPU/GPU) with new tensor api support.
- `gymapi.SIM_FLEX` - Flex simulation: soft body and rigid body simulation (GPU only) does not fully support new tensor api.

### 1.3 Simulation Parameters

This is how to configure the simulation parameters:

```python
# get default set of parameters
sim_params = gymapi.SimParams()

# set common params
sim_params.dt = 1 / 60
sim_params.substeps = 2
sim_params.up_axis = gymapi.UP_AXIS_Z
sim_params.gravity = gymapi.Vec3(0.0, 0.0, -9.8)

# set PhysX specific params
sim_params.physx.use_gpu = True
sim_params.physx.solver_type = 1
sim_params.physx.num_position_iterations = 6
sim_params.physx.num_velocity_iterations = 1
sim_params.physx.contact_offset = 0.01
sim_params.physx.rest_offset = 0.0

# set Flex specific params
sim_params.flex.solver_type = 5
sim_params.flex.num_outer_iterations = 4
sim_params.flex.num_inner_iterations = 20
sim_params.flex.num_position_iterations = 4
sim_params.flex.relaxation = 0.8
sim_params.flex.warm_start = 0.5

sim = gym.create_sim(
    compute_device_id,
    graphics_device_id,
    gymapi.SIM_PHYSX,
    sim_params
)
```

### 1.4 Ground Plane

```python
plane_params = gymapi.PlaneParams()
plane_params.normal = gymapi.Vec3(0.0, 0.0, 1.0) # z-up
plane_params.distance = 0.0
plane_params.static_friction = 1.0
plane_params.dynamic_friction = 1.0
plane_params.restitution = 0.0

gym.add_ground(sim, plane_params)
```

### 1.5 Load Assets

Gym supports URDF and MJCF file formats. Here's a quick way to load those files into a simulation:

```python
asset_root = "../../assets"
asset_file = "urdf/franka_description/robots/franka_panda.urdf"
asset = gym.load_asset(sim, asset_root, asset_file)
```

The `load_asset` function uses the file name extension to determine which processing code to use. We can also pass extra information to the asset importer:

```python
asset_options = gymapi.AssetOptions()
asset_options.fix_base_link = True
asset_options.armature = 0.01
asset = gym.load_asset(sim, asset_root, asset_file, asset_options)
```

This doesn't automatically add it to the simulation, but it is the first step.

### 1.6 Environment and Actors

Environment consists of collection of actors and sensors simulated together. The overall reason to pack them together is performance. 

Lets setup a simple environment:

```python
spacing = 2.0
lower = gymapi.Vec3(-spacing, 0.0, -spacing)
upper = gymapi.Vec3(spacing, spacing, spacing)
env = gym.create_env(sim, lower, upper, 8)
```
this creates 8 environments.

If we want to create an actor, we can do so below:
```python
pose = gymapi.Transform()
pose.p = gymapi.Vec3(0.0, 0.0, 0.0)
pose.r = gymapi.Quat(0.0, 0.0, 0.0, 1.0)
actor_handle = gym.create_actor(
    env,
    asset,
    pose,
    "MyActor",
    0,
    1
)
```

Here's a quick example of going from axis-angle to quaternion:

```python
pose.r = gymapi.Quat.from_axis_angle(gymapi.Vec3(1, 0, 0), -0.5 * math.pi)
```

Any argument after `MyActor` are optional. The two args are <b> collision_group </b> and <b> collision_filter </b>. The `collision_group` assigns the actor to a collision group. This prevents actors from the same environment from colliding with each other. The `collision_filter` is a bit mask that helps filter collision between bodies (kinda like preventing self-collision checks if we just have a robot). 

```python
num_envs = 64
envs_per_row = 8 #infer columns from num_envs
env_spacing = 2.0
env_lower = gymapi.Vec3(-env_spacing, 0.0, -env_spacing)
env_upper = gymapi.Vec3(env_spacing, env_spacing, env_spacing)

envs = []
actor_handles = []
for i in range(num_envs):
    env = gym.create_env(sim, env_lower, env_upper, envs_per_row)
    envs.append(env)
    
    height = random.uniform(1.0, 2.5)
    pose = gymapi.Transform()
    pose.p = gymapi.Vec3(0.0, height, 0.0)

    actor_handle = gym.create_actor(
        env,
        asset,
        pose,
        "MyActor",
        i,
        1
    )
    actor_handles.append(actor_handle)
```

Be aware that once you finish populating one environment and start creating another, the first environment can no longer have stuff added to it. This is because of how memory is allocated. We can find ways to "fake" having dynamic number of actors, but that is for later.

### 1.7 Running Sim

Super Simple:
```python
while True:
    # step the physics
    gym.simulate(sim) # each iteration is one timestep
    gym.fetch_results(sim, True)
```

### 1.8 Adding a Viewer

If we want to visualize our setup, we need to add a viewer. 

```python
cam_props = gymapi.CameraProperties()
viewer = gym.create_viewer(sim, cam_props)
```

If we want to update the viewer (re-draw on it), we need to execute the following every iteration:

```python
gym.step_graphics(sim)
gym.draw_viewer(viewer, sim, True)
```

The `step_graphics` function synchronizes visual representation with simulation context. The `draw_viewer` renders the visual representation of the simulation. They are separate because `step_graphics` can be called without `draw_viewer` or even the need for a viewer.

To synchronize visual update frequency with real time we add this to the loop:

```python
gym.sync_frame_time(sim)
```

This throttles down the simulation rate to match real-time. If it's slower than real time, this has no effect.

We can terminate simulation by checking if viewer was closed with `query_viewer_has_closed`.

```python
while not gym.query_viewer_has_closed(viewer):
    gym.simulate(sim)
    gym.fetch_results(sim, True)

    gym.step_graphics(sim)
    gym.draw_viewer(viewer, sim, True)
    gym.sync_frame_time(sim)
```

---

## Assets

---

## Physics Simulation

---

## Tensor API

---

## Force Sensors

---

## Simulation Tuning

---

## Math Utilities

---

## Graphics and Camera Sensors

---

## Terrains

---

## Python API

- Checkout IsaacGym_Preview_TacSL_Package/isaacgym/docs/api/python/gym_py.html