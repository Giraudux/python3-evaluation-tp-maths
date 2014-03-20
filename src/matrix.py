from array import array

"""
 * Class matrix
 * i, p = rows
 * j, q = columns
"""
class matrix:

    def __init__(self, p, q, data=None):
        self._p = p
        self._q = q
        if isinstance(data, list):
            self.from_list(data)
        else:
            self._data = array("d", [0]*(p*q))

    def __repr__(self):
        return "matrix({self._p}, {self._q}, {self._data})".format(self=self)

    def __str__(self):
        res = str()
        tmp = self._data.tolist()
        for i in range(0,self._p*self._q,self._q):
            res += str(tmp[i:i+self._q]) + "\n"
        return res

    def __getitem__(self, key):
        i, j = key
        return self._data[self._q*i+j]

    def __setitem__(self, key, value):
        i, j = key
        self._data[self._q*i+j] = value

    def __add__(self, other):
        if((self._q == other._q) or (self._p == other._p)):
            res = Matrix(self._p, self._q)
            for i in range(self._p):
                for j in range(self._q):
                    res[i,j] = self[i,j] + other[i,j]
            return res
        else:
            return None

    def __sub__(self, other):
        if((self._q == other._q) or (self._p == other._p)):
            res = Matrix(self._p, self._q)
            for i in range(self._p):
                for j in range(self._q):
                    res[i,j] = self[i,j] - other[i,j]
            return res
        else:
            return None

    def __mul__(self, other):
        if(self._q == other._p):
            res = matrix(self._p, other._q)
            for i in range(self._p):
                for j in range(other._q):
                    acc=0
                    for k in range(self._q):
                        acc += self[i,k] * other[k,j]
                    res[i,j] = acc
            return res
        else:
            return None

    def __eq__(self, other):
        return (self._p == other._p) and (self._q == other._q) and (self._data == other._data)

    def __ne__(self, other):
        return not(self == other)

    def from_list(self, data):
        if(len(data) == (self._p*self._q)):
            self._data = array("d", data)

    def from_json(self, json):
        return None

    def get_row(self, i):
        res = list()
        for j in range(self._q):
            res.append(self[i,j])
        return res 

    def get_column(self, j):
        res = list()
        for i in range(self._p):
            res.append(self[i,j])
        return res 

"""
 * Class lu_decomposition
"""
class lu_decomposition:

    def __init__(self, a, in_place=True):
        if not in_place:
            self._a = a
        else:
            self._a = None
        self._lu = a
        self.decompose()

    def decompose(self):
        for k in range(self._lu.get_p()-1):
            for i in range(k+1,self._lu.get_p()):
                self._lu[i,k] = self._lu[i,k]/self._lu[k,k]
                for j in range(k+1,self._lu.get_p()):
                    self._lu[i,j] = self._lu[i,j]-self._lu[i,k]*self._lu[k,j]

    def get_a(self):
        return self._a
