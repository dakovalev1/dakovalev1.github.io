---
title: "Understanding AdamW via Worst-Case Convergence Analysis"
author: "Dmitry Kovalev"
date: 2026-11-25
# description: "An introduction to spectral decomposition."
macros: macros.tex
bibliography: references.bib
---




Before the invention of Muon [@jordan2024muon], AdamW [@loshchilov2019decoupled] has been arguably the most popular optimizer for large-scale deep learning. Its fast and stable convergence made it a default choice in most practical scenarios. Unfortunately, despite the fact that this algorithm was invented almost a decade ago, its theoretical understanding remains limited. In this post, we will try to find a theoretical justification of AdamW's empirical success by means of theoretical worst-case convergence analysis. More concretely, we will show that AdamW may be the best possible algorithm for a certain class of stochastic convex optimization problems.


# Preliminaries

## Stochastic Optimization
Given a stochastic objective function $f_\xi(\cdot)\colon \R^d \to \R$, where $\xi$ is a random variable sampled from a probability distribution $\cD$, consider a standard stochastic optimization problem:


$$
\label{eq:main}
\min_{x \in \R^d} f(x),\quad\text{where}\quad f(x) =  \E_{\xi \sim \cD}[f_\xi(x)].
$$

One of the simplest algorithms for solving such problems is SGD with a constant stepsize $\eta > 0$, which iterates

$$
x_{k+1} = x_k - \eta \cdot \nabla f_{\xi_k}(x_k),
$$

where $\xi_k \sim \cD$ is sampled independently at each iteration. Under mild regularity assumptions, the stochastic gradient is unbiased, i.e., 

$$
\E [\nabla f_{\xi_k}(x_k) \mid x_k] = \nabla f(x_k),
$$

so that SGD recovers the full-batch GD update in expectation.


## AdamW

AdamW is an extension of SGD for solving problem $\eqref{eq:main}$. Its pseudocode is given below.

!!! algorithm "Algorithm 1: AdamW"
    - **input:** $x_1 \in \R^d$, $(m_0,v_0) = 0 \in \R\times\R^d$
    - **for** $k = 1,2, \dots, K-1$
        - obtain stochastic gradient:<br>
         $g_k = \nabla f_{\xi_k}(x_k)$, where $\xi_k \sim \cD$ is a fresh sample
        - compute 1st moment:<br> $m_k = \beta_1 m_{k-1} + (1-\beta_1) g_k$
        - compute 2nd moment:<br> $v_k = \beta_2 v_{k-1} + (1-\beta_2) (g_k \odot g_k)$
        - apply bias correction:<br> $\hat{m}_k = m_k/(1-\beta_1^k)$, $\hat{v}_k = v_k/(1-\beta_2^k)$
        - perform update with componentwise preconditioning and decoupled weight decay:<br> $x_{k+1} = (1-\eta\lambda)x_k - \eta \cdot \hat{m}_k\oslash(\sqrt{\hat v_k} + \epsilon)$
    - **output:** $x_K$






# References