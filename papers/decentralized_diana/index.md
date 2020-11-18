title: A Linearly Convergent Algorithm for Decentralized Optimization: Sending Less Bits for Free!
date: 3 Nov 2020
abstract: Decentralized optimization methods enable on-device training of machine learning models without a central coordinator. In many scenarios communication between devices is energy demanding and time consuming and forms the bottleneck of the entire system. We propose a new randomized first-order method which tackles the communication bottleneck by applying randomized compression operators to the communicated messages. By combining our scheme with a new variance reduction technique that progressively throughout the iterations reduces the adverse effect of the injected quantization noise, we obtain the first scheme that converges linearly on strongly convex decentralized problems while using compressed communication only. We prove that our method can solve the problems without any increase in the number of communications compared to the baseline which does not perform any communication compression while still allowing for a significant compression factor which depends on the conditioning of the problem and the topology of the network. Our key theoretical findings are supported by numerical experiments.
authors:    Dmitry Kovalev
            Anastasia Koloskova
            Martin Jaggi
            Peter Richtárik
            Sebastian U. Stich
links: {"PDF": "https://arxiv.org/pdf/2011.01697", "arXiv" : "https://arxiv.org/abs/2011.01697"}