import numpy as np

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
    def rotMat(self, mat, rots):
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
'''
test = RotMatsN(4)

m = np.matrix([ [1], [0], [0], [0] ])

print(test.rotMat(m, (0, 0, 0, 0, 0, 0)))
'''