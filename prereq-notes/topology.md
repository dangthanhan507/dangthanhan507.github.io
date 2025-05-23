---
layout: default
title:  "GDL 2: Topology"
date:   2025-04-18
categories: GDL
parent: Prerequisites
# math: katex
mathjax: true
tags: 
  - latex
  - math
---

# GDL 2: Topology (super short)

## Metric Spaces

Metric spaces are sets $$X$$ equipped with a distance $$d(x,y)$$ between points $$x,y \in X$$. We can specify what is close/nearby in a quantifiable way. 

## Topological Spaces

Topological spaces offer us a qualitative and more abstract way to think about what is "local" or "close".

A topological space is a set $$X$$ together with a collection $$T$$ of subsets of $$X$$ called the open sets of $$X$$ and satisfying the following properties:
1. The empty set and $$X$$ belong to $$T$$.
2. Any finite intersection and arbitrary union of open sets in $$T$$ is open.

Open sets can be thought of as a neighborhood of the points they contain.

## Euclidian Topology

Is topology given by open sets induced by Euclidian Metric. More generally, for any metric space $$(X,d)$$, the open balls generate a topology on $$X$$ called topology generated by $$d$$.

### Continuity

A function $$f: X \to Y$$ between topological spaces is continuous if for every open subset $$U \subset Y$$ its preimage $$f^{-1}(U)$$ is open in $$X$$.

It is like $$\epsilon-\delta$$ continuity but without the need for a metric.

### Homeomorphism

A homeomorphism $$\phi: X \to Y$$ between topological spaces is a bijective map such that both $$\phi$$ and $$\phi^{-1}$$ are continuous. 

Cube is homeomorphic to sphere. Donut is homeomorphic to mug.

Let $$C = \{ (x,y,z) \mid \max (\mid x \mid, \mid y \mid, \mid z \mid) = 1 \}$$ be the cube. Define $$\phi: C \to S^2$$ with $$\phi(x,y,z) = \frac{(x,y,z)}{\sqrt{x^2+y^2+z^2}}$$.

The inverse is $$\phi^{-1}(x,y,z) = \frac{(x,y,z)} {\max(\mid x \mid, \mid y \mid, \mid z \mid)}$$.

Smoothness is not a topological property! 

### Hausdorff Spaces

Hausdorff Spaces is a physical space that respects the intuition that we can "separate" any two points. Hausdorff spaces are spaces where any two points can be "housed off".

The more formal definition is: A topological space $$X$$ is said to be a Hausdorff space if given any points $$p_1, p_2 \in X$$, there exists neighborhoods $$U_1$$ of $$p_1$$ and $$U_2$$ of $$p_2$$ such that $$U_1 \cap U_2 = \emptyset$$.


### Basis of Topological Space

In linear algebra, we always want to see how our linear map will affect the basis of our vector space. This is the same idea in topology. 

A collection $$\mathcal{B}$$ of open sets of $$X$$ is called a basis for the topology of $$X$$ if every open subset is the union of some collection of elements in $$B$$.

### Second-countable Spaces

A topological space is second-countable if it has a countable base. This means that the topology can be generated by a countable collection of open sets.

First-countable spaces are those that have a countable local base at each point. This means that for every point in the space, there exists a countable collection of open sets such that any open set containing the point contains at least one of the sets in the collection.


### Manifolds

An n-dimensional topological manifold is a second-countable Hausdorff space such that every point of $$M$$ has a neighborhood that is homeomorphic to an open subset of $$\mathbb{R}^n$$.