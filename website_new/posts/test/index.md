---
title: "Understanding AdamW: Worst-Case Convergence Analysis Strikes Back"
author: "Dmitry Kovalev"
date: 2026-11-25
# description: "An introduction to spectral decomposition."
macros: macros.tex
bibliography: references.bib
---



# Introduction

Before the invention of Muon [@jordan2024muon], AdamW [@loshchilov2019decoupled] has been arguably the most popular optimizer for large-scale deep learning. Its fast and stable convergence made it a default choice in most practical scenarios. Unfortunately, there is no satisfying theoretical explanation for AdamW's success. In particular, the original Adam paper [@kingma2015adam] contains a mistake in the convergence analysis, and other works, e.g., [@li2023convergence] are unable to explain the advantages of AdamW over simple SGD variants. Some researchers even [suggested that neural networks could have evolved to make AdamW the best optimizer](https://wp.me/p9RZpk-ey). In this post, we will try to address the issue and finally provide a possible theoretical justification for the empirical success of AdamW.



## AdamW Summary

AdamW can be summarized in the following pseudocode:

!!! algorithm "Algorithm 1: AdamW"

    - **For** $k = 1,2, \dots, K-1$
        1. obtain stochastic gradient $g_k$ 
        2. compute 1st moment: $m_k = \beta_1 m_{k-1} + (1-\beta_1) g_k$
        - compute 2nd moment: $v_k = \beta_2 v_{k-1} + (1-\beta_2) g_k^2$
        - apply bias correction: $\hat{m}_k = \frac{m_k}{1-\beta_1^k}$, $\hat{v}_k = \frac{v_k}{1-\beta_1^k}$
        - update rule: $x_{k+1} = (1-\eta\lambda)x_k - \eta \frac{\hat{m}_k}{\sqrt{\hat v_k}}$
    - **Return** $x_K$


It is an instance of SGD with adaptive preconditioning which incorporates the following main algorithmic components:

- Componentwise preconditioning
- First and second moments of the gradient
- Bias correction
- Decoupled weight decay
 
# TODO


$$
\min_{x \in \R^d} f(x)
$$

[@kingma2015adam]

# References