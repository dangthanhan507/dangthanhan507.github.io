---
title: "HydroShear: Hydroelastic Shear Simulation for Tactile Sim-to-Real Reinforcement Learning"
authors: "**An Dang**, Jayjun Lee, Mustafa Mukadam, X. Alice Wu, Bernadette Bucher, Manikantan Nambi, Nima Fazeli"
contribution: "Equal contribution: An Dang and Jayjun Lee."
year: 2026
status: RSS
venue: "Robotics: Science and Systems (RSS)"
order: 4
featured: true
summary: "A non-holonomic hydroelastic tactile simulator that models stick-slip transitions and path-dependent shear for zero-shot sim-to-real reinforcement learning."
video: /videos/hydroshear.mp4
poster: /images/hydroshear.jpg
video_label: "HydroShear title video demonstrating tactile simulation and robot manipulation"
video_caption: "The full title video from the HydroShear project."
source_url: https://hydroshear.github.io/
links:
  - label: Project page
    url: https://hydroshear.github.io/
  - label: Paper
    url: https://arxiv.org/abs/2603.00446
  - label: Code
    url: https://github.com/MMintLab/hydroshear
---

HydroShear models stick-slip transitions, path-dependent force and shear
buildup, and full SE(3) object-sensor interactions. It uses signed distance
functions to track contact displacement and simulate tactile shear while
remaining agnostic to the underlying physics engine.

The simulator enables zero-shot transfer of reinforcement-learning policies
for peg insertion, bin packing, book shelving, and drawer pulling.

Presented at Robotics: Science and Systems (RSS) 2026.
