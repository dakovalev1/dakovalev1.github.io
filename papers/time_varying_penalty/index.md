title: Towards Accelerated Rates for Distributed Optimization over Time-varying Networks
date: 23 Sep 2020
abstract: We study the problem of decentralized optimization over time-varying networks with strongly convex smooth cost functions. In our approach, nodes run a multi-step gossip procedure after making each gradient update, thus ensuring approximate consensus at each iteration, while the outer loop is based on accelerated Nesterov scheme. The algorithm achieves precision $\varepsilon > 0$ in $O(\sqrt{\kappa_g}\chi\log^2(1/\varepsilon))$ communication steps and $O(\sqrt{\kappa_g}\log(1/\varepsilon))$ gradient computations at each node, where $\kappa_g$ is the global function number and $\chi$ characterizes connectivity of the communication network. In the case of a static network, $\chi = 1/\gamma$ where $\gamma$ denotes the normalized spectral gap of communication matrix $\mathbf{W}$. The complexity bound includes $\kappa_g$, which can be significantly better than the worst-case condition number among the nodes.
authors:    Alexander Rogozin
        Vladislav Lukoshkin
        Alexander Gasnikov
        Dmitry Kovalev
        Egor Shulgin
links: {"PDF": "https://arxiv.org/pdf/2009.11069", "arXiv" : "https://arxiv.org/abs/2009.11069"}