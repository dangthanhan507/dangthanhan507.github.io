---
title: "HULK: Learning Whole-Body Forceful Loco-Manipulation for Humanoids"
authors: "**An Dang**, Arturo Flores Alvarez, Yu-Ming Chen, Conor Mc Gartoll, Helen Sun, Aaron Ames, Nima Fazeli, Manikantan Nambi"
contribution: "Equal contribution: An Dang and Arturo Flores Alvarez."
year: 2026
status: arXiv preprint
order: 5
featured: true
summary: "Combining model predictive control guidance and reinforcement learning for forceful humanoid loco-manipulation, including carrying objects and pulling a 300 kg cart."
video: /videos/hulk-power-clean.mp4
poster: /images/hulk-power-clean.jpg
video_label: "HULK humanoid robot performing a power clean with a barbell"
video_caption: "HULK performing a power clean on real hardware."
source_url: https://hulk-wbc.com/
links:
  - label: Project page
    url: https://hulk-wbc.com/
  - label: Paper
    url: https://arxiv.org/abs/2610.08970
---

HULK combines model predictive control (MPC) reward guidance with reinforcement
learning to develop whole-body controllers for forceful humanoid
loco-manipulation. Wrist-force and grasping specialists are distilled into a
single controller, with capture-point constraints helping it learn balance
recovery.

On hardware, the controller performs tasks including payload carrying,
fridge carrying, canister carrying, and pulling a cart loaded to 300 kg.
The 300 kg figure refers to the cart's load.

This work was conducted during an internship at Amazon.

### Pulling a 300 kg cart

{% include research-video.html src="/videos/hulk-cart.mp4" poster="/images/hulk-cart.jpg" label="HULK pulling a cart loaded to 300 kilograms" caption="A standalone hardware demonstration; 300 kg is the cart load." source="https://hulk-wbc.com/" %}
