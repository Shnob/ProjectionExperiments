import numpy as np
from copy import copy

choose = lambda n, k : int(np.math.factorial(n) / (np.math.factorial(k) * np.math.factorial(n - k)))

class RotMatsN:
    def __init__(self, dim):
        self.dim = dim
        self.mats = []
        self.setupMats(dim)
    def setupMats(self, dim):
        a = 0
        b = 0
        for i in range(choose(dim, 2)):
            b += 1
            if b == dim:
                a += 1
                b = a + 1
            if a == dim:
                break
            self.mats.append((a, b))
        self.mats.sort(key = lambda x : x[0] + x[1]*1.1, reverse=True)

    def rotMat(self, mat, _rots):
        rots = copy(_rots)
        rots.reverse()
        for i in range(len(self.mats)):
            r = np.zeros((self.dim, self.dim))
            c = np.cos(rots[i])
            s = np.sin(rots[i])
            a = self.mats[i][0]
            b = self.mats[i][1]

            for j in range(self.dim):
                r[j][j] = 1

            r[a][a] = c
            r[b][b] = c
            r[a][b] = -s
            r[b][a] = s

            r = np.matrix(r)
            mat = r * mat

        return mat
    def rotMatList(self, mats, _rots):
        rots = copy(_rots)
        rots.reverse()
        ret = []
        for k in range(len(mats)):
            mat = mats[k]
            for i in range(len(self.mats)):
                r = np.zeros((self.dim, self.dim))
                c = np.cos(rots[i]) 
                s = np.sin(rots[i])
                a = self.mats[i][0]
                b = self.mats[i][1]

                for j in range(self.dim):
                    r[j][j] = 1

                r[a][a] = c
                r[b][b] = c
                r[a][b] = -s
                r[b][a] = s

                r = np.matrix(r)
                mat = r * mat

            ret.append(mat)
        return ret