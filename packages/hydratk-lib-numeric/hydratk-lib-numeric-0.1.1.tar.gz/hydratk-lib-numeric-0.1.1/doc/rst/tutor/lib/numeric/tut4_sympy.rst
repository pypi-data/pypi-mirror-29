.. _tutor_numeric_tut4_sympy:

Tutorial 4: SymPy
=================

This sections shows several examples how to use module SymPy.
See module `homepage <http://www.sympy.org/>`_ for more tutorials, reference manual.

Simplification
^^^^^^^^^^^^^^

  .. code-block:: python
   
     from sympy import *         
     
     # numerical expression
     simplify('5**3')
     125
     
     simplify('(5**2)/2 + 6')
     37/2
     
     # symbolic expressions
     init_printing(use_unicode=True)
     x = symbols('x')
     
     simplify((x**2 + 2*x + 1)/(x + 1))
     x + 1     
     
     simplify((x**2 + 2*x + 1)/(sqrt(x + 1)))
      2          
     x  + 2⋅x + 1
     ────────────
       _______  
              ╲╱ x + 1     
              
     simplify(sin(x)**2 + cos(x)**2)
     1
      
     # polynomials, rational functions 
     expand((x+1)**2)
      2          
     x  + 2⋅x + 1 
     
     factor(x**2 + 5*x + 6)
     (x + 2)⋅(x + 3)
     
     apart((x**2 + x + 1)/(x**3 + 3*x**2 + 3*x + 1))
       1        1          1    
     ───── - ──────── + ────────
     x + 1          2          3
             (x + 1)    (x + 1)      
             
Equations
^^^^^^^^^
 
  .. code-block:: python
   
     # single equation
     solveset(x**2 - 1 , x)
     {-1, 1}
      
     solveset(sin(x) - 1, x)
                 ⎧        π           ⎫
                 ⎨2⋅n⋅π + ─ | n ∊ ℤ⎬
                 ⎩        2           ⎭
                  
     solveset(1/x, x)
                 ∅
                        
     # linear equations
     linsolve([x + y + z - 1, x + y + 2*z - 3, x - z + 4], (x, y, z))
     {(-2, 1, 2)}
      
     linsolve(Matrix(([1, 1, 1, 1], [1, 1, 2, 3])), (x, y, z))
     {(-y - 1, y, 2)}
      
     # differential equation
     f = symbols('f', cls=Function)
      
     dsolve(f(x).diff(x,x) + f(x), f(x))
     f(x) = C₁⋅sin(x) + C₂⋅cos(x)
      
     dsolve(f(x).diff(x,x) - 2*f(x)*diff(x) + f(x) - sin(x), f(x))
              -x    x   sin(x)
     f(x) = C₁⋅ℯ   + C₂⋅ℯ  - ──────
                          2   
                          
Matrices
^^^^^^^^

  .. code-block:: python
  
     # definition
     Matrix([1,2,3])
               ⎡1⎤
               ⎢   ⎥
               ⎢2⎥
               ⎢   ⎥
               ⎣3⎦
               
     Matrix(([1,2,3], [4,5,6], [7,8,9]))
               ⎡1  2  3⎤
               ⎢                     ⎥
               ⎢4  5  6⎥
               ⎢                     ⎥
               ⎣7  8  9⎦
     
     # basic operations
     Matrix(([1,2,3], [4,5,6], [7,8,9])) * Matrix([1,1,1])
               ⎡6 ⎤
               ⎢      ⎥
               ⎢15⎥
               ⎢      ⎥
               ⎣24⎦
               
     Matrix(([1,2,3], [4,5,6])) + Matrix(([1,1,1], [0,0,1]))
               ⎡2  3  4⎤
               ⎢                     ⎥
               ⎣4  5  7⎦
               
     Matrix([1,2,3]).T
     [1  2  3]               
     
     # advanced operations
     Matrix(([1,2], [1,0])).det()
     -2
     
     Matrix([[1, 0, 1, 3], [2, 3, 4, 7], [-1, -3, -3, -4]]).rref()
               ⎛⎡1  0   1    3 ⎤, [0, 1]⎞
               ⎜⎢                                          ⎥                        ⎟
               ⎜⎢0  1  2/3  1/3⎥                        ⎟
               ⎜⎢                                          ⎥                        ⎟
               ⎝⎣0  0   0    0 ⎦                        ⎠
               
     Matrix([[1, 0, 1, 3], [2, 3, 4, 7], [-1, -3, -3, -4]]).columnspace()
              ⎡⎡1 ⎤, ⎡0 ⎤⎤
              ⎢⎢      ⎥      ⎢      ⎥⎥
              ⎢⎢2 ⎥      ⎢3 ⎥⎥
              ⎢⎢      ⎥      ⎢      ⎥⎥
              ⎣⎣-1⎦      ⎣-3⎦⎦               
     
     Matrix([[3, -2,  4, -2], [5,  3, -3, -2], [5, -2,  2, -2], [5, -2, -3,  3]]).eigenvects()
              ⎡⎛-2, 1, ⎡⎡0⎤⎤⎞, ⎛3, 1, ⎡⎡1⎤⎤⎞, ⎛5, 2, ⎡⎡1⎤, ⎡0 ⎤⎤⎞⎤
              ⎢⎜                     ⎢⎢   ⎥⎥⎟      ⎜                  ⎢⎢   ⎥⎥⎟      ⎜                  ⎢⎢   ⎥      ⎢      ⎥⎥⎟⎥
              ⎢⎜                     ⎢⎢1⎥⎥⎟      ⎜                  ⎢⎢1⎥⎥⎟      ⎜                  ⎢⎢1⎥      ⎢-1⎥⎥⎟⎥
              ⎢⎜                     ⎢⎢   ⎥⎥⎟      ⎜                  ⎢⎢   ⎥⎥⎟      ⎜                  ⎢⎢   ⎥      ⎢      ⎥⎥⎟⎥
              ⎢⎜                     ⎢⎢1⎥⎥⎟      ⎜                  ⎢⎢1⎥⎥⎟      ⎜                  ⎢⎢1⎥      ⎢0 ⎥⎥⎟⎥
              ⎢⎜                     ⎢⎢   ⎥⎥⎟      ⎜                  ⎢⎢   ⎥⎥⎟      ⎜                  ⎢⎢   ⎥      ⎢      ⎥⎥⎟⎥
              ⎣⎝                     ⎣⎣1⎦⎦⎠      ⎝                  ⎣⎣1⎦⎦⎠      ⎝                  ⎣⎣0⎦      ⎣1 ⎦⎦⎠⎦
              
Calculus
^^^^^^^^

  .. code-block:: python
  
     # derivatives
     diff(cos(x), x)
     -sin(x) 
     
     diff(-1/(x**2), x)
     2 
     ──
      3
     x              
     
     diff(-y*tan(y)/(x**2) + y, x, y)
                   ⎛     ⎛   2         ⎞                        ⎞
     2⋅⎝y⋅⎝tan (y) + 1⎠ + tan(y)⎠
     ────────────────────────────
                 3             
                x
                
     # integrals
     integrate(x**2, x)
      3
     x 
     ──
     3 
     
     integrate(exp(-x**2), x)
     √π⋅erf(x)
     ─────────
         2
         
     integrate(exp(-x**2), (x, -oo, oo))
     √π
     
     # limits
     limit((exp(x) - 1)/x, x, 0)
     1
     
     limit(1/x, x, 0, '-')
     -∞
     