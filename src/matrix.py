from array import array

class Matrix:
    def __init__(self, p, q, ls=None):
        self.p = p
        self.q = q
        if((ls != None) and (len(ls) == (p*q))):
            self.data = array("d", ls)
        else:
            self.data = array("d", [0]*(p*q))

    def __repr__(self):
        return 'Point({self.p}, {self.q}, {self.data})'.format(self=self)

    def __str__(self):
        res = str()
        tmp = self.data.tolist()
        for i in range(0,self.p*self.q,self.q):
            res += str(tmp[i:i+self.q]) + "\n"
        return res

    def __getitem__(self, key):
        i, j = key
        return self.data[self.q*(i-1)+j-1]

    def __setitem__(self, key, value):
        i, j = key
        self.data[self.q*(i-1)+j-1] = value

    def __add__(self, other):
        if((self.q == other.q) or (self.p == other.p)):
            res = Matrix(self.p, self.q)
            for i in range(self.p):
                for j in range(self.q):
                    res[i,j] = self[i,j] + other[i,j]
            return res
        else:
            return None

    def __sub__(self, other):
        if((self.q == other.q) or (self.p == other.p)):
            res = Matrix(self.p, self.q)
            for i in range(self.p):
                for j in range(self.q):
                    res[i,j] = self[i,j] - other[i,j]
            return res
        else:
            return None

    def __mul__(self, other):
        if(self.q == other.p):
            res = Matrix(self.p, other.q)
            for i in range(self.p):
                for j in range(self.q):
                    acc=0
                    for k in range(self.q):
                        acc += self[i,k] * other[k,j]
                    res[i,j] = acc
            return res
        else:
            return None

mat1 = Matrix(2,2,[1,2,3,4])
mat2 = Matrix(2,2,[4,3,2,1])
print(mat1)
print(mat2)
print(mat1 * mat2)
