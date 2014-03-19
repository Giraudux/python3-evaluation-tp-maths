from array import array

"""
 * Class matrix
 * i, p = rows
 * j, q = columns
"""
class matrix:

    def __init__(self, p, q, data=None):
        self.p = p
        self.q = q
        if isinstance(data, list):
            self.from_list(data)
        else:
            self.data = array("d", [0]*(p*q))

    def __repr__(self):
        return "matrix({self.p}, {self.q}, {self.data})".format(self=self)

    def __str__(self):
        res = str()
        tmp = self.data.tolist()
        for i in range(0,self.p*self.q,self.q):
            res += str(tmp[i:i+self.q]) + "\n"
        return res

    def __getitem__(self, key):
        i, j = key
        return self.data[self.q*i+j]

    def __setitem__(self, key, value):
        i, j = key
        self.data[self.q*i+j] = value

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
            res = matrix(self.p, other.q)
            for i in range(self.p):
                for j in range(other.q):
                    acc=0
                    for k in range(self.q):
                        acc += self[i,k] * other[k,j]
                    res[i,j] = acc
            return res
        else:
            return None

    def __eq__(self, other):
        return (self.p == other.p) and (self.q == other.q) and (self.data == other.data)

    def __ne__(self, other):
        return not(self == other)

    def from_list(self, data):
        if(len(data) == (self.p*self.q)):
            self.data = array("d", data)

    def from_json(self, json):
        return None

    def get_row(self, i):
        res = list()
        for j in range(self.q):
            res.append(self[i,j])
        return res 

    def get_column(self, j):
        res = list()
        for i in range(self.p):
            res.append(self[i,j])
        return res 

"""
 * Class lu_decomposition
"""
class lu_decomposition:

    def __init__(self, a, in_place=True):
        self.a = a
        self.decompose()

    def decompose(self):
        for k in range(self.a.p-1):
            for i in range(k+1,self.a.p):
                self.a[i,k] = self.a[i,k]/self.a[k,k]
                for j in range(k+1,self.a.p):
                    self.a[i,j] = self.a[i,j]-self.a[i,k]*self.a[k,j]

    def get_a(self):
        return self.a
