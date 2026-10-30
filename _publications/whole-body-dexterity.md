---
title: "Whole-Body Dexterity"
authors: "Conor Mc Gartoll, **An Dang**, Pranay Thangeda, Arjun Gupta, Carolina Higuera, Nima Fazeli, Mustafa Mukadam, Manikantan Nambi"
contribution: "Equal contribution: Conor Mc Gartoll, An Dang, and Pranay Thangeda."
year: 2026
status: arXiv preprint
order: 6
featured: true
summary: "Using a humanoid's arms and torso as contact surfaces to grasp, reposition, and carry objects with a proprioception-only policy transferred zero-shot to real hardware."
video: /videos/whole-body-dexterity.mp4
poster: /images/whole-body-dexterity.jpg
video_label: "Unitree G1 repositioning a basketball across its arms and torso"
video_caption: "Whole-body object manipulation on the Unitree G1."
source_url: https://wholebodydex.com/
links:
  - label: Project page
    url: https://wholebodydex.com/
  - label: Paper
    url: https://arxiv.org/abs/2610.22184
---

Whole-Body Dexterity uses the robot's body and appendages as contact surfaces
for manipulation. The pipeline generates feasible whole-body grasps, trains
reinforcement-learning experts to move between them, and distills the experts
into a single proprioception-only policy.

The policy transfers zero-shot to a real Unitree G1. It repositions a basketball
and a cardboard box around the torso and supports a longer task that picks up
a box, stows it under one arm, carries it from a shelf to a table, and places it.

This work was conducted during an internship at Amazon.
