
import sympy
from sympy import I

import compose


class QuantumGate(object):
    """represents a quantum gate that acts on some number of quantum wires """
    def __init__(self, n = 1):
        self._number_wires = n
        self.set_matrix(sympy.eye(n))  # identity gate by default

    def get_size(self):
        return self._number_wires

    #  Please give a matrix of the right
    def set_matrix(self, mat):
        self._matrix = mat

    def get_matrix(self):
        return self._matrix


def arbitrary_gate(n, mat):
    g = QuantumGate(n)
    g.set_matrix(mat)
    return g

def _hadamard_gate_helper(n):
    def f(x, y):
        return -2 * (bin(x & y).count('1') % 2) + 1
    return sympy.Matrix(2 ** n, 2 ** n, f)


    if n == 0:
        return sympy.Matrix([[1]])
    elif n < 0:
        return None
    else:
        m = _hadamard_gate_helper(n-1)
        return m.row_join(m).col_join(m.row_join(-m))

def hadamard_gate(n = 1):
    return arbitrary_gate(n, _hadamard_gate_helper(n) / (sympy.sqrt(2) ** n))

def pauli_x_gate():
    mat = sympy.Matrix([[0, 1], [1, 0]])
    return arbitrary_gate(1, mat)

def pauli_y_gate():
    mat = sympy.Matrix([[0, -I], [I, 0]])
    return arbitrary_gate(1, mat)

def pauli_z_gate():
    mat = sympy.Matrix([[1, 0], [0, -1]])
    return arbitrary_gate(1, mat)

def controlled_gate(gate):
    size = gate.get_size()
    mat = sympy.eye(2 ** (size + 1))
    mat[(2 ** size):, (2 ** size):] = gate.get_matrix()
    return arbitrary_gate(size + 1, mat)
    
def swap_gate():
    mat = sympy.Matrix([[1, 0, 0, 0],
                        [0, 0, 1, 0],
                        [0, 1, 0, 0],
                        [0, 0, 0, 1]])
    return arbitrary_gate(2, mat)

def toffoli_gate():
    return controlled_gate(controlled_gate(pauli_x_gate()))

def fredkin_gate():
    return controlled_gate(swap_gate())

def classical_fn_gate(n, m, f):
    """Takes a number of input bits and output bits to a function, and a
    function.  Creates a quantum gate on n+m wires that performs the gate on
    the first n wires, and xors its output onto the last m.

    Specifically, the function f should take an integer in the appropriate
    [unsigned] range, and output an integer in the appropriate [unsigned]
    range"""
    
    def l(k):
        x = k / (2 ** n)
        y = k % (2 ** n)
        y = y ^ f(x)
        return y + x * (2 ** n)


    mat = sympy.zeros((2 ** (m + n), 2 ** (m + n)))
    for i in range(0, 2 ** (m + n)):
        mat[i, l(i)] = 1

    return arbitrary_gate(n + m, mat)

