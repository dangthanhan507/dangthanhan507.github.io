---
layout: default
title: 2. Flow
parent: Unsupervised Learning
nav_order: 3
mathjax: true
tags: 
  - latex
  - math
# math: katex
---

# Likelihood Models: Flow Models

We stil want to learn a distribution $$p_\theta(x)$$ and sample from it.

Recall Autoregressive models issues:
- Sampling is serial (hence slow)
- Lacks latent representation / embedding space
- Limited to discrete data (at least in terms of experimental success)

Flow models will address these issues, but its performance not as good as other models.

