import scipy.special as sp
import math
import numpy as np
import numpy.linalg as alg

class Task(object):

    def __init__(self, l, D, c, s, alpha, T, I, K):
        self.l = l
        self.D = D
        self.c = c
        self.s = s
        self.alpha = alpha
        self.T = T

        self.I = I
        self.x = np.linspace(0, self.l, self.I)
        self.hx = (self.l - 0) / (self.I - 1)
        self.K = K
        self.t = np.linspace(0, self.T, self.K)
        self.ht = (self.T - 0) / (self.K - 1)

        self.psi = lambda x: np.cos(np.pi * x / self.l)
        self.answer_analytic = []
        self.answer = []

    def analytic_decision(self):
        self.answer_analytic = [[np.cos(np.pi * x / self.l) *
                                 np.exp(-(self.D / self.c + (self.alpha / self.c) * ((np.pi / self.l) ** 2)) * t)
                                 for x in self.x] for t in self.t]
        return self.answer_analytic

    def isStable(self):
        return (self.alpha * self.ht / (self.c * self.hx ** 2)) < 1/2

    def calculate(self):
        for k in range(0, self.K):
            local_answer = np.zeros(self.I, np.float64)
            if k == 0:
                for i in range(0, self.I):
                    local_answer[i] = (self.psi(self.hx * i))
            else:
                for i in range(1, self.I-1):
                    local_answer[i] = self.answer[k-1][i] + \
                                      (self.alpha * self.ht * (self.answer[k-1][i+1] - 2 * self.answer[k-1][i] + self.answer[k-1][i-1])) / \
                                      (self.c * self.hx ** 2) - (self.D * self.ht * self.answer[k-1][i] / self.c)
                local_answer[0] = local_answer[1]
                local_answer[self.I - 1] = local_answer[self.I - 2] # I-1 узел здесь это по факту I, а I-2 это I-1
            self.answer.append(local_answer)
        return self.answer

    def calculateAbsError(self):
        if self.answer is not None and self.answer_analytic is not None:
            return np.max(np.abs(np.array(self.answer_analytic) - np.array(self.answer)))
