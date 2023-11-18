title: IntSGD: Floatless Compression of Stochastic Gradients
date: 16 Feb 2021
abstract: We propose a family of lossy integer compressions for Stochastic Gradient Descent (SGD) that do not communicate a single float. This is achieved by multiplying floating-point vectors with a number known to every device and then rounding to an integer number. Our theory shows that the iteration complexity of SGD does not change up to constant factors when the vectors are scaled properly. Moreover, this holds for both convex and non-convex functions, with and without overparameterization. In contrast to other compression-based algorithms, ours preserves the convergence rate of SGD even on non-smooth problems. Finally, we show that when the data is significantly heterogeneous, it may become increasingly hard to keep the integers bounded and propose an alternative algorithm, IntDIANA, to solve this type of problems.
authors:    Konstantin Mishchenko
            Bokun Wang
            Dmitry Kovalev
            Peter Richtárik
links: {"PDF" : "https://arxiv.org/pdf/2102.08374", "ICLR 2022" : "https://openreview.net/forum?id=pFyXqxChZc", "arXiv" : "https://arxiv.org/abs/2102.08374"}