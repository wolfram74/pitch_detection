import sympy
from data_loader import quad_fitter

def algebra_1():
    x2, y1, y2, y3 = sympy.symbols('x2 y1 y2 y3', real=True)
    yvec = sympy.Matrix([[y1],[y2],[y3]])
    equations = sympy.Matrix([
        [(x2-1)**2, x2-1, 1],
        [x2**2, x2, 1],
        [(x2+1)**2, x2+1, 1]
        ])
    inverts = equations.inv()
    sympy.pprint(equations)
    sympy.pprint(inverts)
    for term in inverts:
        sympy.pprint(term.simplify())
    params = inverts*yvec
    for term in params:
        sympy.pprint(term.simplify())
    return

def fit_test():
    n = 4
    data = [3,7,5]
    p = quad_fitter(n, data)
    print(p)
    checks = [(
        p[0]*(n+shift)**2+
        p[1]*(n+shift)+
        p[2]
        )for shift in [-1, 0, 1]]
    print(checks, data)

# fit_test()
