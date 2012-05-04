
import bus
import gate
import sympy

def compose_gates(first, second):
    if first is None:
        return second
    if second is None:
        return first

    if first.get_size() != second.get_size():
        return
    mat1 = first.get_matrix()
    mat2 = second.get_matrix()
    result = mat2 * mat1
    return gate.arbitrary_gate(first.get_size(), result)

def compose_map_gates(l):
    return reduce(compose_gates, l)

def apply_gate(b, g):
    if b.get_size() != g.get_size():
        return
    vec = b.get_vector()
    mat = g.get_matrix()
    result = mat * vec
    return bus.arbitrary_wire(b.get_size(), result)

def reverse_gate(b, g):
    if b.get_size() != g.get_size():
        return
    vec = b.get_vector()
    mat = g.get_matrix()
    result = mat.inv() * vec
    return bus.arbitrary_wire(b.get_size(), result)

# add n inputs to the TOP.
def expand_inputs(g, n):
    size = g.get_size()
    mat = g.get_matrix()
    newmat = sympy.zeros((2 ** (n + size), 2 ** (n + size)))
    for i in range(0, 2 ** n):
        k = 2 ** size
        newmat[i*k:(i+1)*k, i*k:(i+1)*k] = mat
    return gate.arbitrary_gate(n + size, newmat)

def permute_inputs(n, l):

    l.reverse()
    mat = sympy.zeros((2 ** n, 2 ** n))
    for i in range(0, 2 ** n):
        ilist = map(int, bin(i)[2:])
        ilist = [0,] * (n  - len(ilist)) + ilist
#        ilist.reverse()
        res = 0
        for j in range(0, n):
            res = res + (2 ** j) * ilist[l[j]]
        mat[res, i] = 1
    return mat

def permute_inputs_old(n, l):
    def f(i, j):
        ilist = map(int, bin(i)[2:])
        jlist = map(int, bin(j)[2:])
        ilist = [0,] * (n - len(ilist)) + ilist
        jlist = [0,] * (n - len(jlist)) + jlist
        for index in range(0, len(l)):
            if ilist[index] != jlist[l[index]]:
                return 0
        return 1

    return sympy.Matrix(2 ** n, 2 ** n, f)

def map_inputs(g, new_size, inputs):
    old_size = g.get_size()
    if new_size > old_size:
        g = expand_inputs(g, new_size - old_size)
        for i in range(old_size, new_size):
            for j in range(0, new_size):
                if inputs.count(j) == 0:
                    inputs.insert(0, j)
    elif new_size < old_size:
        return

    mat1 = permute_inputs(new_size, inputs)
    mat2 = mat1.inv()
        
    return gate.arbitrary_gate(new_size, mat2 * (g.get_matrix()) * mat1)


#the second one acts on LATER wires
def parallel_gates(g2, g1):
    if g1 is None:
        return g2
    if g2 is None:
        return g1
    s1 = g1.get_size()
    s2 = g2.get_size()
    g1 = expand_inputs(g1, s2)
    g2 = map_inputs(g2, s1 + s2, range(0, s2))
    return compose_gates(g1, g2)

def parallel_map_gates(gs):
    return reduce(parallel_gates, gs)    

def parallel_repeat_gate(g, n):
    return parallel_map_gates([g,] * n)
