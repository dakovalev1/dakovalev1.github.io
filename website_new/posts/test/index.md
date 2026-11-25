---
title: "Understanding AdamW: Worst-Case Convergence Analysis Strikes Back"
author: "Dmitry Kovalev"
date: 2026-11-25
# description: "An introduction to spectral decomposition."
macros: macros.tex
bibliography: references.bib
---



# Introduction

Before the invention of Muon, AdamW has been arguably the most popular optimizer for large-scale deep learning. Its fast and stable convergence made it a default choice in most practical scenarios. Unfortunately, there is not satisfying theoretical explanation for AdamW's success. In particular, the original [Adam paper](https://arxiv.org/abs/1412.6980) contains a mistake in the convergence analysis. Other works typically unable to explain the [@loshchilov2019adamw]


$$
\min_{x \in \R^d} f(x)
$$

