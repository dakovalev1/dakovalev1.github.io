title: Revisiting Stochastic Extragradient
abstract: We consider a new extension of the extragradient method that is motivated by approximating implicit updates. Since in a recent work~\cite{chavdarova2019reducing} it was shown that the existing stochastic extragradient algorithm (called mirror-prox) of~\cite{juditsky2011solving} diverges on a simple bilinear problem, we prove guarantees for solving variational inequality that are more general than in~\cite{juditsky2011solving}. Furthermore, we illustrate numerically that the proposed variant converges faster than many other methods on the example of~\cite{chavdarova2019reducing}. We also discuss how extragradient can be applied to training Generative Adversarial Networks (GANs). Our experiments on GANs demonstrate that the introduced approach may make the training faster in terms of data passes, while its higher iteration complexity makes the advantage smaller. To further accelerate method's convergence on problems such as bilinear minimax, we combine the extragradient step with negative momentum~\cite{gidel2018negative} and discuss the optimal momentum value.
date: 27 May 2019
authors: Konstantin Mishchenko
            Dmitry Kovalev
            Egor Shulgin
            Peter Richtárik
            Yura Malitsky
links: {"PDF" : "https://arxiv.org/pdf/1905.11373", "arXiv" : "https://arxiv.org/abs/1905.11373"}