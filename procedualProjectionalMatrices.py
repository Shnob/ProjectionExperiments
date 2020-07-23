import numpy as np
from copy import copy

class ProjMatN:
    def __init__(self, dim, dist):
        self.dim = dim
        self.dist = dist
    def projMat(self, _x, offset = None):
        x = copy(_x)

        if offset is not None:
            x = x + offset
        d = 1/(self.dist - x.item(x.size - 1))

        a = self.dim - 1
        b = self.dim

        n = np.zeros((a, b))
        for i in range(a):
            n[i][i] = d
        return np.matrix(n) * x, d
    def projMatList(self, _x, offset = None):
        p = copy(_x)
        ret = []
        for i in range(len(p)):
            if offset is not None:
                p[i] = p[i] + offset
            d = 1/(self.dist - p[i].item(p[i].size - 1))

            a = self.dim - 1
            b = self.dim

            n = np.zeros((a, b))
            for j in range(a):
                n[j][j] = d

            pp = np.matrix(n) * p[i]
            ret.append(pp)
        return ret