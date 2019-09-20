#!/usr/bin/env python
# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt

from ..optimizer import Optimizer

norm = np.linalg.norm

class NetworkOptimizer(Optimizer):
    '''The base network optimizer class, which handles saving/plotting history.'''

    def init(self): # Note this is not the construction function __init__
        super().init()
        self.s = np.zeros((self.dim, self.n_agent))
        self.y = self.x_0.copy()
        for i in range(self.n_agent):
            self.s[:, i] = self.grad(self.y[:, i], i)


    # def save_history(self):
        # self.history.append({
            # 'x': self.x.mean(axis=1).copy(), 
            # 'y': self.y.copy(), 
            # 's': self.s.copy()
            # })


    def update(self):
        self.n_comm[self.t] += self.n_edges

        y_last = self.y.copy()
        self.y = self.x.dot(self.W)
        self.s = self.s.dot(self.W_s)
        for i in range(self.n_agent):
            self.s[:, i] += self.grad(self.y[:, i], i) - self.p.grad(y_last[:, i], i)

        self.local_update()


    def plot_history(self):

        p = self.p
        hist = self.history

        x_min = p.x_min
        f_min = p.f(x_min)

        plt.figure()
        legends = []

        # | f_0(x_0^{(t)}) - f(x^\star) / f(x^\star)
        tmp = [ ( p.f(h['x'][:, 0], 0) - f_min) / f_min for h in hist]
        plt.semilogy(tmp)
        legends.append(r"$\frac{ f_0(\mathbf{x}_0^{(t)}) - f(\mathbf{x}^\star) } {f(\mathbf{x}^\star) }$")

        # | f_0(x_0^{(t)}) - f_0(x^\star) / f_0(x^\star)
        tmp = [ ( p.f(h['x'][:, 0], 0) - p.f(x_min, 0)) / p.f(x_min, 0) for h in hist]
        plt.semilogy(tmp)
        legends.append(r"$\frac{ f_0(\mathbf{x}_0^{(t)}) - f_0(\mathbf{x}^\star) } {f_0(\mathbf{x}^\star) }$")

        # | f_0(\bar x^{(t)}) - f(x^\star) / f(x^\star)
        tmp = [ (p.f(h['x'].mean(axis=1), 0) - f_min) / f_min for h in hist]
        plt.semilogy(tmp)
        legends.append(r"$\frac{ f_0(\bar{\mathbf{x}}^{(t)}) - f(\mathbf{x}^\star) } {f(\mathbf{x}^\star) }$")

        # | f_0(\bar x^{(t)}) - f_0(x^\star) / f_0(x^\star)
        tmp = [ (p.f(h['x'].mean(axis=1), 0) - p.f(x_min, 0)) / p.f(x_min, 0) for h in hist]
        plt.semilogy(tmp)
        legends.append(r"$\frac{f_0(\bar{\mathbf{x}}^{(t)}) - f_0(\mathbf{x}^\star) } {f_0(\mathbf{x}^\star) }$")

        # | f(x_0^{(t)}) - f(x^\star) / f(x^\star)
        tmp = [ (p.f(h['x'][:, 0]) - f_min) / f_min for h in hist]
        plt.semilogy(tmp)
        legends.append(r"$\frac{ f(\mathbf{x}_0^{(t)}) - f(\mathbf{x}^\star) } {f(\mathbf{x}^\star) }$")

        # | f(\bar x^{(t)}) - f(x^\star) / f(x^\star)
        tmp = [ (p.f(h['x'].mean(axis=1)) - f_min) / f_min for h in hist]
        plt.semilogy(tmp)
        legends.append(r"$\frac{ f(\bar{\mathbf{x}}^{(t)}) - f(\mathbf{x}^\star) } {f(\mathbf{x}^\star) }$")

        # | \frac 1n \sum f_i(x_i^{(t)}) - f(x^\star) / f(x^\star)
        tmp = [ ( np.mean([p.f(h['x'][:, i], i) for i in range(p.n_agent)]) - f_min) / f_min for h in hist]
        plt.semilogy(tmp)
        legends.append(r"$\frac{ \frac{1}{n} \sum f_i (\mathbf{x}_i^{(t)}) - f(\mathbf{x}^\star) } {f(\mathbf{x}^\star) }$")

        # | \frac 1n \sum f(x_i^{(t)}) - f(x^\star) / f(x^\star)
        tmp = [ ( np.mean([p.f(h['x'][:, i]) for i in range(p.n_agent)]) - f_min) / f_min for h in hist]
        plt.semilogy(tmp)
        legends.append(r"$\frac{\frac{1}{n} \sum f(\mathbf{x}_i^{(t)}) - f(\mathbf{x}^\star) } {f(\mathbf{x}^\star) }$")

        plt.ylabel('Distance')
        plt.xlabel('#iters')
        plt.legend(legends)




        plt.figure()
        legends = []


        # \Vert \nabla f(\bar x^{(t)}) \Vert
        tmp = [norm(p.grad(h['x'].mean(axis=1))) for h in hist]
        plt.semilogy(tmp)
        legends.append(r"$\Vert \nabla f(\bar{\mathbf{x}}^{(t)}) \Vert$")

        # \Vert \nabla f_0(x_0^{(t)}) \Vert
        tmp = [norm(p.grad(h['x'][:, 0]), 0) for h in hist]
        plt.semilogy(tmp)
        legends.append(r"$\Vert \nabla f_0({\mathbf{x}_0}^{(t)}) \Vert$")

        # \Vert \frac 1n \sum \nabla f_i(x_i({(t)}) \Vert
        tmp = [norm(np.mean( [p.grad(h['x'][:, i], i) for i in range(p.n_agent)])) for h in hist]
        plt.semilogy(tmp)
        legends.append(r"$\Vert \frac{1}{n} \sum_i \nabla f_i({\mathbf{x}_i}^{(t)}) \Vert$")

        # \frac 1n \sum \Vert \nabla f_i(x_i({(t)}) \Vert
        tmp = [np.mean( [ norm( p.grad(h['x'][:, i], i)) for i in range(p.n_agent)]) for h in hist]
        plt.semilogy(tmp)
        legends.append(r"$\frac{1}{n} \sum_i \Vert \nabla f_i({\mathbf{x}_i}^{(t)}) \Vert$")

        plt.ylabel('Distance')
        plt.xlabel('#iters')
        plt.legend(legends)


        plt.figure()
        legends = []

        # \Vert \bar x^{(t)} - x^\star \Vert
        tmp = [norm(h['x'].mean(axis=1) - x_min) for h in hist]
        k = np.exp(np.log(tmp[-1]/tmp[0]) / len(hist))
        print("Actual convergence rate of " + self.name + " is k = " + str(k))
        plt.semilogy(tmp)
        legends.append(r"$\Vert \bar{\mathbf{x}}^{(t)} - \mathbf{x}^\star \Vert$")

        # \Vert x^{(t)} - \mathbf 1 \otimes x^\star \Vert 
        plt.semilogy([norm(h['x'].T - x_min, 'fro') for h in hist])
        legends.append(r"$\Vert \mathbf{x}^{(t)} - \mathbf{1} \otimes \mathbf{x}^\star \Vert$")

        # \Vert x^{(t)} - \mathbf 1 \otimes \bar x^{(t)} \Vert
        plt.semilogy([norm(h['x'].T - h['x'].mean(axis=1), 'fro') for h in hist])
        legends.append(r"$\Vert \mathbf{x}^{(t)} - \mathbf{1} \otimes \bar{\mathbf{x}}^{(t)} \Vert$")

        # \Vert s^{(t)} \Vert
        plt.semilogy([norm(h['s'], 'fro') for h in hist])
        legends.append(r"$\Vert \mathbf{s}^{(t)} \Vert$")

        # \Vert s^{(t)} - \mathbf 1 \otimes \bar g^{(t)} \Vert
        tmp = []
        for h in hist:
            g = np.array([p.grad(h['y'][:, i], i) for i in range(p.n_agent)])
            g = g.T.mean(axis=1)
            tmp.append(norm(h['s'].T - g, 'fro'))

        plt.semilogy(tmp)
        legends.append(r"$\Vert \mathbf{s}^{(t)} - \mathbf{1} \otimes \bar{\mathbf{g}}^{(t)} \Vert$")


        # \Vert \bar g^{(t)} - \nabla f(\bar y^{(t)}) \Vert
        tmp = []
        for h in hist:
            g = np.array([p.grad(h['y'][:, i], i) for i in range(p.n_agent)])
            g = g.T.mean(axis=1)
            tmp.append(norm(p.grad(h['y'].mean(axis=1)) - g, 2))

        plt.semilogy(tmp)
        legends.append(r"$\Vert \bar{\mathbf{g}}^{(t)} - \nabla f(\bar{\mathbf{y}}^{(t)}) \Vert$")


        # \Vert s^{(t)} - \mathbf 1 \otimes \nabla f(\bar y^{(t)}) \Vert
        tmp = []
        for h in hist:
            g = p.grad(h['y'].mean(axis=1))
            tmp.append(norm(h['s'].T - g, 'fro'))

        plt.semilogy(tmp)
        legends.append(r"$\Vert \mathbf{s}^{(t)} - \mathbf{1} \otimes \nabla f(\bar{\mathbf{y}}^{(t)}) \Vert$")


        # \Vert \nabla f(\bar y^{(t)}) \Vert
        tmp = []
        for h in hist:
            g = p.grad(h['y'].mean(axis=1))
            tmp.append(norm(g))

        plt.semilogy(tmp)
        legends.append(r"$\Vert \nabla f(\bar{\mathbf{y}}^{(t)}) \Vert$")


        # \Vert s^{(t)} - \nabla(y^{(t)}) \Vert
        tmp = []
        for h in hist:
            #print(h['y'])
            # print(p.grad(h['y'][:, 0], 0))
            g = np.array([p.grad(h['y'][:, i], i) for i in range(p.n_agent)])
            tmp.append(norm(h['s'] - g.T, 'fro'))

        plt.semilogy(tmp)
        legends.append(r"$\Vert \mathbf{s}^{(t)} - \nabla(\mathbf{y}^{(t)}) \Vert$")


        # \Vert s^{(t)} - (\nabla(y^{(t)} - \nabla f_i(x^\star)) \Vert
        tmp = []
        for h in hist:
            g = np.array([p.grad(h['y'][:, i], i) - p.grad(p.x_min, i) for i in range(p.n_agent)])
            tmp.append(norm(h['s'] - g.T, 'fro'))

        plt.semilogy(tmp)
        legends.append(r"$\Vert \mathbf{s}^{(t)} - (\nabla(\mathbf{y}^{(t)}) - \nabla f_i(\mathbf{x}^\star)) \Vert$")

        # Optimal first order method bound starting from x_0 = 0
        # kappa = L / sigma
        # r = (kappa - 1) / (kappa + 1)
        # tmp = r ** np.arange(len(hist)) * norm(x_min)
        # plt.semilogy(tmp)
        # legends.append("Optimal 1st order bound")

        plt.xlabel('#iters')
        plt.ylabel('Distance')
        plt.title('Details of ' + self.name + ', L=' + str(self.L) + r', $\sigma$=' + str(self.sigma) )
        plt.legend(legends)
