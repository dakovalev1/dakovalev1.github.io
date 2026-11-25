---
title: "Understanding AdamW via Worst-Case Convergence Analysis"
author: "Dmitry Kovalev"
date: 2026-11-25
# description: "An introduction to spectral decomposition."
macros: macros.tex
bibliography: references.bib
---



# Introduction

Before the invention of Muon [@jordan2024muon], AdamW [@loshchilov2019decoupled] has been arguably the most popular optimizer for large-scale deep learning. Its fast and stable convergence made it a default choice in most practical scenarios. Unfortunately, there is no satisfying theoretical explanation for AdamW's success. In particular, the original Adam paper [@kingma2015adam] contains a mistake in the convergence analysis, and other works, e.g., [@li2023convergence] are unable to explain the advantages of AdamW over simple SGD variants. Some researchers even [suggested that neural networks could have evolved to make AdamW the best optimizer](https://wp.me/p9RZpk-ey). In this post, we will try to address the issue and finally provide a possible path towards theoretical justification for the empirical success of AdamW.

<!-- ## AdamW: Summary of Existing Knowledge -->

Given some probability distribution $\cD$ and a stochastic objective function $f(\cdot\,;\xi) \colon \R^d \to \R$, consider the following standard stochastic optimization problem:

$$
\min_{x \in \R^d} f(x),\qquad f(x) =  \E_{\xi \sim \cD}[f(x;\xi)].
$$

AdamW is an optimization algorithm for solving such problems. It can be summarized with the following pseudocode:

!!! algorithm "Algorithm 1: AdamW"

    - **For** $k = 1,2, \dots, K-1$
        - obtain stochastic gradient:<br>
         $g_k = \nabla f(x;\xi_k)$, where $\xi_k \sim \cD$ is a fresh sample
        - compute 1st moment:<br> $m_k = \beta_1 m_{k-1} + (1-\beta_1) g_k$
        - compute 2nd moment:<br> $v_k = \beta_2 v_{k-1} + (1-\beta_2) (g_k \odot g_k)$
        - apply bias correction:<br> $\hat{m}_k = m_k/(1-\beta_1^k)$, $\hat{v}_k = v_k/(1-\beta_2^k)$
        - perform update with componentwise preconditioning and decoupled weight decay:<br> $x_{k+1} = (1-\eta\lambda)x_k - \eta \cdot \hat{m}_k\oslash\sqrt{\hat v_k}$
    - **Return** $x_K$

 
Let's briefly discuss what we know about the main steps of the algorithm. The *componentwise preconditioning*, which in the case of AdamW corresponds to the elementwise division by the square root of the second moment, is relatively well understood. Intuitively, it works well when the coordinates of the function $f(x)$ have very different scales; formally, this phenomenon was described by [@liu2025adagrad,@jiang2025provable]. However, AdamW is not the only algorithm with 



<!-- ### Component-wise preconditioning -->

# TODO 




[@kingma2015adam]

# References