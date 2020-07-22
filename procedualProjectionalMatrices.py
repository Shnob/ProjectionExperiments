import numpy as np
from copy import copy

class ProjMatN:
    def __init__(self, dim, dist):
        self.dim = dim
        self.dist = dist
    def projMat(self, _x, offset = None):
        x = copy(_x)
        p = []
        for j in range(len(x)):
            p.append([x[j]])
        p = np.matrix(p)

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
            for i in range(a):
                n[i][i] = d
            ret.append(np.matrix(n) * p[i])
        return ret

'''
test = ProjMatN(3, 3)

mat = np.matrix([ [1], [0], [0] ])

newMat = test.projMat(mat)

print(newMat)
'''