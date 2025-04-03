---
layout: default
title:  "GNN WL-test"
date:   2025-04-03
categories: GNN expressivity
parent: Graph Notes (GNNs and more)
# math: katex
mathjax: true
tags: 
  - latex
  - math
---

# Weisfeiler-Lehman Test
The Weisfeiler-Lehman Test (WL-test) is a test that you can conduct to see if two graphs are isomorphic.



## Isomorphism
First lets define what isomorphism is. Generally, an isomorphism is a mapping between two spaces such that the structure between the 2 spaces are preserved. This is kind of vague, but I have seen examples of these before.

Examples of Isomorphisms:
- Homeomorphism (isomorphism of topological spaces)
- Diffeomorphism (isomorphism of spaces with differentiable structure)
- Symplectomorphism (isomorphism of symplectic manifolds, preserves energy)

One super specific example that I know of:
$$\mathrm{SO(3)} / \mathrm{SO(2)} \cong \mathrm{S}^2$$
In other words, the quotient space between $$SO(3)$$ and $$SO(2)$$ is isomorphic to $$S^2$$.

Let $$\mathcal{G}_1 = (\mathcal{V}_1, \mathcal{E}_1) $$ be the first graph and $$\mathcal{G}_2 = (\mathcal{V}_2, \mathcal{E}_2) $$ be the second graph.

