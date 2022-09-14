from Parser import Parser
from z3 import *
from ReSolver import ReSolver

# Tests are in no way conclusive nor any proof of correctness. 
# They just shows common functionality.

# Provided: H E \ L P
#reRow = ["HE|LL|O+", "[PLEASE]+"]
#reCol = ["[^SPEAK]+", "EP|IP|EF"]

# Unions: B C \ T E
#reRow = ["(A|B)(A|B|C)", "(T|X)E"]
#reCol = ["((B|C)|D)T", "(CE)|(DE)"]

# Dots: B A \ E C
#reRow = [".A", ".C"]
#reCol = ["BE", ".C"]

# Range 1: C B \ C C
#reRow = ["[ABC][AB]", "[ABCDE][BC]"]
#reCol = ["[CDE][CFG]", "[BC][CF]"]

# Range 2: C B \ C C
#reRow = ["[A-C][A-B]", "[A-E][B-C]"]
#reCol = ["[C-E][CFG]", "[B-C][CF]"]

# Range 3: F C \ L O
#reRow = ["[^A-E][^AB]", "[^A-K]O"]
#reCol = ["[B-F][KL]", "[BC]O"]

# Star: A A \ B B 
#reRow = ["A*B*", "B*"]
#reCol = ["AB*", "AB"]

# Plus: A A \ B C
#reRow = ["A+", "B+C"]
#reCol = ["AB", "AC"]

# Question: A A \ C E
#reRow = ["A?A?B?", "(AB)?(CE)?"]
#reCol = ["B?A?C?", "A?(CE)?E?"]

# Combined large: A B C D \ E F G H \ I J K L \ M N O P
reRow = [".(B|D)(C|D|E)D", "E[^ABC][^H-Z]H", ".*[A-K].", "MN(O|PQ)P"]
reCol = ["A(EI|FJ|CK)(M|J|K|KE)", "[^D-Z](A|B|FJ)(PQ|A|N)", "(C|F)[G-Z][K-Z]O", "D(H|P|Q)L(PE|P)"]

# Setup solvers and parsers
N = len(reRow)
rs = ReSolver(N)
p = Parser()
s = Solver()

conds = []
fields = [ [Int('x_%s_%s' %(i, j)) for i in range(N)] for j in range(N) ]


# Process row rules
for row in range(N):
    ast = p.parse(reRow[row])
    cond = rs.reCond(ast, fields, row, 0, N, dir=1)
    conds.append(cond)

# Process col rules
for col in range(N):
    ast = p.parse(reCol[col])
    cond = rs.reCond(ast, fields, col, 0, N, dir=0)    
    conds.append(cond)
# Solve conditions
for c in conds:
    s.add(c)
s.check()
model = s.model()

# Visualize
output = [[0 for _ in range(N)] for _ in range(N)]
for m in model:
    x, y = list(map(int, str(m).replace("x_", "").split("_")))
    output[x][y] = model[m]

for i in range(N):
    for j in range(N):
        print(chr(int(str(output[i][j]))), end=' ')
    print()








