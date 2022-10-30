title: Stochastic Distributed Learning with Gradient Quantization and Variance Reduction
abstract: We consider distributed optimization where the objective function is spread among different devices, each sending incremental model updates to a central server. To alleviate the communication bottleneck, recent work proposed various schemes to compress (e.g.\ quantize or sparsify) the gradients, thereby introducing additional variance ω≥1 that might slow down convergence. For strongly convex functions with condition number κ distributed among n machines, we (i) give a scheme that converges in O((κ+κωn+ω) log(1/ε)) steps to a neighborhood of the optimal solution. For objective functions with a finite-sum structure, each worker having less than m components, we (ii) present novel variance reduced schemes that converge in O((κ+κωn+ω+m)log(1/ε)) steps to arbitrary accuracy ε>0. These are the first methods that achieve linear convergence for arbitrary quantized updates. We also (iii) give analysis for the weakly convex and non-convex cases and (iv) verify in experiments that our novel variance reduced schemes are more efficient than the baselines.
authors:Samuel Horváth
        Dmitry Kovalev
        Konstantin Mishchenko
        Peter Richtárik
        Sebastian U. Stich
date: 4 April 2019
links: {"PDF" : "https://arxiv.org/pdf/1904.05115.pdf", "Optimization Methods and Software": "https://www.tandfonline.com/doi/abs/10.1080/10556788.2022.2117355", "arXiv" : "https://arxiv.org/abs/1904.05115"}