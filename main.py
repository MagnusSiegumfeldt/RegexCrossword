from Parser import Parser
from z3 import *
from ReSolver import ReSolver

# Handle input
N = int(input())
reRow = ["" for _ in range(N)]
reCol = ["" for _ in range(N)]
for i in range(N):
    reRow[i] = input()
for i in range(N):
    reCol[i] = input()



# Setup solvers and parsers
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








