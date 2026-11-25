---
title: "Understanding AdamW: Worst-Case Convergence Analysis Strikes Back"
author: "Dmitry Kovalev"
date: 2026-11-25
# description: "An introduction to spectral decomposition."
macros: macros.tex
bibliography: references.bib
---



# Introduction

Before the invention of Muon [@jordan2024muon], AdamW [@loshchilov2019decoupled] has been arguably the most popular optimizer for large-scale deep learning. Its fast and stable convergence made it a default choice in most practical scenarios. 

Unfortunately, there is no satisfying theoretical explanation for AdamW's success. In particular, the original Adam paper [@kingma2015adam] contains a mistake in the convergence analysis, and other works [@li2023convergence] are unable to explain the advantages of AdamW over simple SGD variants. Some researchers even [suggest that neural networks could have evolved to make AdamW the best optimizer](https://wp.me/p9RZpk-ey). In this work, we will try to address this issue.



# Todo

$$
\min_{x \in \R^d} f(x)
$$

# References