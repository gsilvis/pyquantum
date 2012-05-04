
import sympy
from sympy import I

class QuantumBus(object):
    """represents a group of quantum bits, that may be entangled"""
    def __init__(self, n = 1):
        self._number_wires = n     # n wires, default number is 1

    def get_size(self):
        return self._number_wires

    def get_vector(self):
        return self._vector

    def set_vector(self, vec):
        self._vector = vec


def pure_wire(n, vals):

    if not len(vals) == n:
        return
    
    index = 0
    for i in range(0, n):
        if vals[n-i-1] == True:
            index = index + (2 ** i)
        elif vals[n-i-1] == False:
            pass
        else:
            return   # Return, because the input 'vals' was bad.
        
    vect = [0,] * (2 ** n)
    vect[index] = 1
        
    return arbitrary_wire(n, sympy.Matrix(vect))

def arbitrary_wire(n, vec):
    wire = QuantumBus(n)
    wire.set_vector(vec)
    return wire

def z_pos_wire():
    return arbitrary_wire(1, sympy.Matrix([1, 0]))

def z_neg_wire():
    return arbitrary_wire(1, sympy.Matrix([0, 1]))

def x_pos_wire():
    return arbitrary_wire(1, sympy.Matrix([1, 1]) / sympy.sqrt(2))

def x_neg_wire():
    return arbitrary_wire(1, sympy.Matrix([1, -1]) / sympy.sqrt(2))

def y_pos_wire():
    return arbitrary_wire(1, sympy.Matrix([1, I]) / sympy.sqrt(2))

def y_neg_wire():
    return arbitrary_wire(1, sympy.Matrix([1, -I]) / sympy.sqrt(2))


def join_wires(a, b):
    if a is None:
        return b
    if b is None:
        return a
    wires = a.get_size() + b.get_size()
    vec = sympy.zeros((2 ** wires, 1))
    m = 2 ** b.get_size()
    for i in range(0, 2 ** a.get_size()):
        k = i * m
        vec[k:k+m, 0] = a.get_vector()[i] * b.get_vector()

    return arbitrary_wire(wires, vec)


