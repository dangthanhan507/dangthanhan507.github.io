---
layout: default
title: Beyond Pick and Place Workshop
parent: ICRA 2025
nav_order: 1
mathjax: true
---

# Beyond Pick and Place Workshop

## Katerina Fragkiadaki - 3D Generative Manipulation and Object Dynamics

Autonomous vehicles technology to robot manipulation.
- Foundation Models
- 2D diffusion policy or $$\pi_0$$
- 3D diffuser Actor

TO do 3d diffusion, predict gripper position 

- 3d point tracks
- model-based control with generative models (guided diffusion)

## David Held - Spatially-aware Robot Learning

- generalize dexterous manipulation to unseen objects?
- contact point network creates critic map (Q-value) .... gets contact locaiton through softmax
- motion network for actions (hybrid discrete-continuous RL)
    - learning hybrid actor-critic maps
- Visual Manip w/ legs
- HacMan++
- ArticuBot
    - generate lots of demos in simulation
- Point Cloud Diffusion Transformer (delta location of points)
    - this is SE(3) equivariant
    - 3D diffusion model
- TAPIP3D
- Discrete Diffusion


This is very similar to what I thought of (actor-critic maps)

## Rachel Holladay - Modelling Mechanics for Dexterous Decision-Making

Works on TAMP (Task And Motion Planning)

I think this is the same stuff as before.

New work (beyond pick and place)
- guarded planning
- GUARDED stands for: guiding uncertainty accounting for risk and dynamics

This is just revamped safety-based robotics.

## Micheal Posa - Dexterity and generalization?

- knows that robots will be first deployed doing tasks w/ BC or RL.
- pitching his stuff as forward-thinking

Model-based hierarchies struggle a lot with robotics. Micheal Posa thinks contact rich dynamics are a big problem.

Goes into Vysics which reconstructs objects using vision and contact-rich physics. 
Reconstructs objects with partial view and contact.

Russ said before -> Goal: "LQR" but for multi-contact systems

Can't solve the contact-rich MPC (QCQP or MIP).

Using linearization and ADMM you can split this into 2 parts:
- QP dynamic constraints
- complementarity constraint projection (non-convex)
- it works ok but is inherently local

Now he wants to do sampling with CI-MPC
- bi-level hybrid reasoning

<b> Insight: </b> Find an idea that you have unique insight into doing. If no one else did it, it wouldn't be solved. Don't chase the newest thing. 

## Spotlight

List of papers that are interesitng:
- GET-ZERO: Graph Embodiment Transformer for Zero-shot Embodiment Generalization
- Metric Semantic Manipulation-enhanced Mapping
- AugInsert: Learning robust force-visual policy via data augmentation
- FoAR: Force-Aware Reactive Policy for Contact-Rich Robotic Manipulation
- Streaming Flow Policy: Simplifying diffusion/flow policies
- DyWA: Dynamics-adaptive World Action Model for Generalizable Non-prehensile Manipulation
- SAIL: Faster-than-Demonstration Execution of Imitation Learning Policies
- Reactive Diffusion Policy: Slow-Fast Visual-Tactile Policy Learning for Contact-Rich Manipulation

## Russ Tedrake - Multitask pretraining



## Charting the Path Toward Contact-rich Manipulation

