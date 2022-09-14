from z3 import *
import itertools
from itertools import permutations
class ReSolver:
    def __init__(self, N):
        self.N = N
        self.fields = [Int('x_%s' %(i)) for i in range(N)]

    # Create z3 conditions of ast.
    def reCond(self, ast, fields, row, i, l, dir):
        if l not in self.reLength(ast) or i + l > self.N:
            return False
        elif ast[0] == "empty":
            return True
        elif ast[0] == "char" and l == 1:
            return fields[row if dir == 0 else i][i if dir == 0 else row] == ord(ast[1])
        elif ast[0] == "digit" and l == 1:
            return fields[row if dir == 0 else i][i if dir == 0 else row] == ord(ast[1])
        elif ast[0] == "any" and l == 1:
            conds = []
            for c in range(ord('A'), ord('Z') + 1):
                conds.append(fields[row if dir == 0 else i][i if dir == 0 else row] == c)
            return self.createConds(conds)
        elif ast[0] == "set" and l == 1:
            return self.reCond(ast[1], fields, row, i, l, dir)
        elif ast[0] == "set_concat":
            return Or(self.reCond(ast[1], fields, row, i, l, dir), self.reCond(ast[2], fields, row, i, l, dir))
        elif ast[0] == "set_char":
            return self.reCond(ast[1], fields, row, i, l, dir)
        elif ast[0] == "set_range":
            n = self.eval(ast[1])
            m = self.eval(ast[2])
            conds = []
            for c in range(n, m + 1):
                conds.append(fields[row if dir == 0 else i][i if dir == 0 else row] == c)
            return self.createConds(conds)
        elif ast[0] == "set_not":
            s = self.evalSet(ast[1])
            rs = self.reverseSet(s)
            conds = []
            for c in rs:
                conds.append(fields[row if dir == 0 else i][i if dir == 0 else row] == c)
            return self.createConds(conds)
        elif ast[0] == "union":
            return Or(self.reCond(ast[1], fields, row, i, l, dir), self.reCond(ast[2], fields, row, i, l, dir))
        elif ast[0] == "concat":
            lens = self.reLength(ast[1])
            e = False
            for len in self.reLength(ast[1]):
                e = Or(e, And(self.reCond(ast[1], fields, row, i, len, dir), self.reCond(ast[2], fields, row, i + len, l - len, dir)))
            return e

        elif ast[0] == "group":
            return self.reCond(ast[1], fields, row, i, l, dir)
        elif ast[0] == "star":
            if l == 0:
                return True
            else:
                e = False
                for len in self.reLength(ast[1]):
                    e = Or(e, And(self.reCond(ast[1], fields, row, i, len, dir), self.reCond(ast, fields, row, i + len, l - len, dir)))
            return e    

    # calculates possible lengths of ast's
    def reLength(self, ast):
        if ast[0] == "empty":
            return set([0])
        elif ast[0] == "char" or ast[0] == "any": 
            return set([1])
        elif ast[0] == "set" or ast[0] == "set_concat" or ast[0] == "set_range" or ast[0] == "set_not":
            return set([1])
        elif ast[0] == "concat":
            return self.setAdd(self.reLength(ast[1]), self.reLength(ast[2]))
        elif ast[0] == "union":
            return self.reLength(ast[1]) | self.reLength(ast[2])
        elif ast[0] == "group":
            return self.reLength(ast[1])
        elif ast[0] == "star":
            s = set([0])
            len = self.reLength(ast[1])
            while True:
                tmp = self.setAdd(s, len)
                if s | tmp == s:
                    break
                s = s | tmp 
            return s
    

    def setAdd(self, set1, set2):
        res = set()
        for x in set1:
            for y in set2:
                s = x + y
                if s <= self.N:
                    res.add(s)
        return res

    # Or's multiple z3 conds together.
    def createConds(self, conds):
        if len(conds) == 1: 
            return conds[0]
        cond = conds.pop()
        return Or(cond, self.createConds(conds))

    # Evaluating a regular expression
    def eval(self, ast):
        if ast[0] == "char":
            return ord(ast[1])
        if ast[0] == "digit":
            return ord(ast[1])
    # Evaluating a regex set.
    def evalSet(self, ast):
        if ast[0] == "set_concat":
            return self.evalSet(ast[1]) |self.evalSet(ast[2])
        elif ast[0] == "set_range":
            n = self.eval(ast[1])
            m = self.eval(ast[2])
            s = set()
            for c in range(n, m + 1):
                s = s | set([c])
            return s
        elif ast[0] == "char" or ast[0] == "digit":
            return set([ord(ast[1])])
    
    # Used for the not operation.
    def reverseSet(self, s):
        all = set([c for c in range(ord('A'), ord('Z') + 1)])
        return all - s
