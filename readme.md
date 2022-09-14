# Regex crossword solver
This is a regex crossword solver, using PLY and Z3. All regex strings are parsed and constructed as abstract syntax trees which then can be processed, creating z3 conditions allowing the z3 solver to solve this.

## How to run
Install PLY and Z3 for python

```
pip install ply z3-solver
```

Run ```./main.py``` to run program with input to stdin in the format:
```
N
Row regex 1
Row regex 2
...
Row regex N
Col regex 1
Col regex 2
...
Col regex N
```
Preinputted tests run from  ```./test.py```.
## Support
The program supports the following
* Upper case characters (ABC...Z)
* Groups (...)
* Any ( . )
* Unions (A | B)
* Ranges [ABC], [A-Z], [^ABC] and [^A-Z]
* Quantifiers A*, A+ and A? 



## Limitations
* The solver performs no error checks on non valid inputs.
* The solver isn't tested against lowercase letters or numbers.
* The solver isn't tested thouroughly.
* The solver doesn't implement any further regex features not described above.