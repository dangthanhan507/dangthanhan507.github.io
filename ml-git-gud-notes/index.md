---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: default
title:  ML (Git Gud) Resources
math: katex
has_children: true
---

This is a collection of resources I've used to try and git gud in ML. Hopefully, I can come back to these or someone will find use in it. I'm not going to list papers I've read since I think it's much better to go through compiled information first. This isn't a sufficient condition to get started in ML Research, but I think it's necessary to have gathered skills from these resources to be able to do research. 


<!-- # Display a link -->
## 1. Get started (Basics)
1. Andrej Karpathy Zero to Hero - [YouTube](https://www.youtube.com/playlist?list=PLoROMvodv4rO2c7g2i0a3d8b6e1a5c3d4)
    - Get good at backprop while learning about ML basics.
    - Learn how pytorch works under the hood.
    - Exposure to simple concepts like (Gradient Descent, Weight Initialization, Train/Val, BatchNorm/LayerNorm, Attention ...etc.)
    - Learn more complex training concepts (gradient accumulation, mixed precision, bfloat, distributed pytorch, )
    - End goal: you can get started in ML and run a simple training script by end of this playlist.
2. UvA DL - [Notebook-Website](https://uvadlc-notebooks.readthedocs.io/en/latest/)
    - Deep Learning 1 (PyTorch)
        - Tutorial 2-4: (Andrej Karpathy covered, but you should do it anyway to learn to visualize gradients and attention)
        - Tutorial 5-6: Basics on ResNets, CNNs, and Transformers
        - Tutorial 9,12,15: Autoencoder, Autoregressive models, Vision Transformers
        - Tutorial 7,8,10,11,16,17: These are all extras to make you learn about all the other things in deep learning.
    - Training Models at Scale
        - takes stuff you learned from (1.) and levels it up.
        - concepts:
            - tensor parallelism
            - looping parallelism
            - pipeline parallelism
            - profiling models
            - 3d parallelism
            - async layers
3. CS294 - [Website](https://sites.google.com/view/berkeley-cs294-158-sp24/home)
    - This is a course taught by Pieter Abbeel @ UC Berkeley. 
    - I think some of the topics are pretty niche, but the homeworks are invaluable.
    - You can think of the homeworks as hardcore mini-projects per question where you have to implement a paper miniaterized into a homework question.
    - This makes you more solid in your PyTorch!
    - I love homeworks that are hard because they make me better.
4. CS274B (UCI) - [Canvas](https://canvas.eee.uci.edu/courses/64508/assignments/syllabus)
    - This is a course taught by Erik Sudderth @ UC Irvine.
    - It goes into probabilistic graphical models (just more bayesian probability)
    - I like this compared to Stanford's equivalent class.
    - The techniques are very old (but solid) and going through the Bishop textbook and homework (hard) is a good way to build really strong bayes probability foundations.
    - This course made me very comfortable with probability (can't get any worse).

## 2. Becoming a good engineer
1. Full-stack DL - [Website](https://fullstackdeeplearning.com/)
    - This is a course that tries to make you become a better ML Engineer.
    - These are my takeaways
        - This is where I really got into PyTorch Lightning.
        - Learning to use W&B (Weights and Biases) to track your experiments.
        - Learning to use DVC (Data Version Control) to version your data.
        - Deploy models on gradio (seems to be what a lot of people use nowadays).
        - Learning to monitor models in production.
        - Obviously unittesting my code.
        - Learning to use Docker to containerize my code.
2. Missing Semester of CS Education - [Website](https://missing.csail.mit.edu/)
    - This is a course that tries to teach you the missing pieces of CS education.
    - While university education gives you a lot of theory, this course remedies it with relevant practical skills.
    - I think you really need this if you want to be a good software engineer. 
    - Stuff like Vim, Security, Build Systems, Git, Shell, etc.

## 3. Learning more!
1. UvA DL - [Notebook-Website](https://uvadlc-notebooks.readthedocs.io/en/latest/)
    - Deep Learning 2: Learn some super niche stuff that will make you overall better.
        - GDL  (Geometric Deep Learning)
        - DPM  (Deep Probabilistic Models (VAEs))
        - AGM  (Advanced Generative Models, 1x1 Normalizing Flows)
        - HDL  (Hyperparameter-Tuning Deep Learning)
        - BNN  (Bayesian Neural Networks)
        - PIML (Physics Inspired Machine Learning)
        - DS   (Dynamical Systems)
        - SGA  (Sampling Discrete Structures)
        - CRL  (Casual Identifiability)
2. Diffusion - [Website](https://diffusion.csail.mit.edu/)
    - MIT course on diffusion models.
    - Goes into deep mathematical details of diffusion models and flow matching.
    - Dip your toes into Stochastic Differential Equations (SDEs).
    - Has labs that help you train a diffusion model from the ground up in a more intuitive framework (flow matching).

## 4. Learning more about ML Research
1. Yannic Kilcher - [YouTube](https://www.youtube.com/@YannicKilcher)
    - Better understanding of ML PhD life - [Video](https://www.youtube.com/watch?v=rHQPBqMULXo)
        - It's one thing to hear from your advisor. It's another to hear from a guy who talks like he's your friend who has been through the trenches before.
    - He has a lot of videos on ML research papers. He does a good job of explaining the concepts and the math behind them.
    - I read the same papers he does a video on and compare my analysis to his to see what I'm missing.
2. Aleksa Gordic - [Youtube](https://www.youtube.com/c/TheAIEpiphany)
    - This guy does the same sort of content as Yannic Kilcher for papers. I like having another datapoint to compare. Also multiple sources help you keep up to date with current hype ML stuff.
    - Exclusive stuff from his channel:
        - Deep dives into codebases from papers he also reviews! (DINO, DETR, Diffusion,...etc.)
            - I love this as it helps me compare how someone with lots of ML experience quickly reads through code.
            - It also helps me link code with papers.
        - Livestreams himself implementing super Large models
            - Really nice background noise for working haha.
            - I like to watch him (not just as noise) to understand kind of what it takes to implement these models (some of my friends are pretty good at this stuff, but I'm not, so I gotta catch up). 
3. Machine Learning & Simulation - [Youtube](https://www.youtube.com/@MachineLearningSimulation)
    - This guy does lots of ML Physics stuff.
    - He also is a huge fan of JAX and has a lot of videos on it.
    - He also just goes into classical techniques on dynamical systems (even has a video on writing your own FEM from scratch).
    - I use this to learn things for fun (which helps get me better).