.. _tutor_numeric_tut1_numpy:

Tutorial 1: NumPy
=================

This sections shows several examples how to use external module NumPy.
See module `homepage <http://www.numpy.org/>`_ for more tutorials, reference manual.

Array creation
^^^^^^^^^^^^^^

  .. code-block:: python
  
     import numpy as np
     
     # 1D array of size 1x8
     a = np.array([1,2,3,4,5,6,7,8])
     
     [1 2 3 4 5 7 8]
     
     # 2D array of size 2x4
     a = np.array([[1,2,3,4], [5,6,7,8]])
     
     [[1 2 3 4]
      [5 6 7 8]]   
      
     # 3D array of size 3x2x2
     a = np.array([[[1,2], [3,4]], [[5,6], [7,8]], [[9,10], [11,12]]])        
     
     [[[ 1  2]
       [ 3  4]]

      [[ 5  6]
       [ 7  8]]

      [[ 9 10]
       [11 12]]]
       
     # array attributes - dimension, size, count of items
     a.ndim     
     3
     
     a.shape
     (3, 2, 2) 
     
     a.size
     12 
       
     # m-D array created from 1D
     a = np.array([1,2,3,4,5,6,7,8])
     a.reshape(2,4)

     [[1 2 3 4]
      [5 6 7 8]]     
     
     a.reshape(2,2,2)     
          
     [[[1 2]
       [3 4]]

      [[5 6]
       [7 8]]]   
       
     # chain vectors
     # horizontal chain 1x8
     a = np.array([1,2,3,4])
     b = np.array([5,6,7,8])
     np.hstack((a,b))
     
     [1 2 3 4 5 6 7 8]
     
     # vertical chain 2x4
     np.vstack((a,b))
     
     [[1 2 3 4]
      [5 6 7 8]]     
            
     # chain matrices
     # horizontal chain 2x4
     a = np.array([[1,2], [3,4]])
     b = np.array([[5,6], [7,8]])
     np.hstack((a,b)
     
     [[1 2 5 6]
      [3 4 7 8]]
     
     # vertical chain 4x2
     np.vstack((a,b)
     
    [[1 2]
     [3 4]
     [5 6]
     [7 8]]            

Indexing
^^^^^^^^
  .. code-block:: python
  
     # original matrix
     a = np.array([[1,2,3,4,5], [6,7,8,9,10], [11,12,13,14,15]])
     
     [[ 1  2  3  4  5]
      [ 6  7  8  9 10]
      [11 12 13 14 15]]
      
     # concrete item, position 2,3
     a[1,2]
     
     8    
     
     # first row
     a[0,:]
     
     [1 2 3 4 5]
     
     # second column
     a[:,1]
     
     [ 2  7 12] 
     
     # whole matrix
     a[:]
     
     [[ 1  2  3  4  5]
      [ 6  7  8  9 10]
      [11 12 13 14 15]]
      
     # submatrix of rows 2-3, columns 2-4         
     a[1:3, 1:4]
     
     [[ 7  8  9]
      [12 13 14]]
              
Arithmetic operations
^^^^^^^^^^^^^^^^^^^^^

  .. code-block:: python
  
     a = np.array([1,2,3,4])
     b = np.array([5,6,7,8])  
  
     # addition
     a+b
     
     [ 6  8 10 12]
     
     # subtraction
     a-b
     
     [-4 -4 -4 -4]
     
     # multiplication
     a*b
     
     [ 5 12 21 32]
     
     # division, integer by default   
     a/b
     
     [ 0 0 0 0]
     
     # float array
     a = np.array([1,2,3,4], dtype=float)
     b = np.array([5,6,7,8], dtype=float)
     a/b
     
     [ 0.2         0.33333333  0.42857143  0.5       ]   
     
     # power
     a**2
     
     [ 1  4  9 16]
     
     # rounding
     a = np.array([1.1,2.5,3.4,4.7])
     
     np.round(a) # classic round
     [ 1.  2.  3.  5.]
     
     np.floor(a) # round down
     [ 1.  2.  3.  4.]
     
     np.ceil(a)  # round up
     [ 2.  3.  4.  5.] 
     
Data generation
^^^^^^^^^^^^^^^

  .. code-block:: python
  
     # vector of ones
     a = np.ones(10)
     
     [ 1.  1.  1.  1.  1.  1.  1.  1.  1.  1.]
     
     # vector of zeros
     a = np.zeros(10)
     
     [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]   
     
     # range
     a = np.arange(10)
     
     [0 1 2 3 4 5 6 7 8 9]
     
     # linear scale <-10,10> with 21 samples
     a = np.linspace(-10,10,21)
     
    [-10.  -9.  -8.  -7.  -6.  -5.  -4.  -3.  -2.  -1.   0.   1.   2.   3.   4.
       5.   6.   7.   8.   9.  10.]    
       
     # logarithmic scale, power of 10
     a = np.logspace(1,4,4)
     
     [    10.    100.   1000.  10000.]   
     
     # geometric scale, power of 2
     a = np.geomscale(1,16,5)
     
     [  1.   2.   4.   8.  16.]
     
Mathematical functions
^^^^^^^^^^^^^^^^^^^^^^

  .. code-block:: python
  
     # square root
     a = np.arange(1,10)
     np.sqrt(a) 
     
     [ 1.          1.41421356  1.73205081  2.          2.23606798  2.44948974
       2.64575131  2.82842712  3.          3.16227766]
       
     # exponential, logarithmic
     np.exp(a)
     
     [  2.71828183e+00   7.38905610e+00   2.00855369e+01   5.45981500e+01
        1.48413159e+02   4.03428793e+02   1.09663316e+03   2.98095799e+03
        8.10308393e+03   2.20264658e+04]
        
     np.log(a))
     [ 0.          0.69314718  1.09861229  1.38629436  1.60943791  1.79175947
       1.94591015  2.07944154  2.19722458  2.30258509]
       
     # goniometric
     np.sin(a)
     
     [ 0.84147098  0.90929743  0.14112001 -0.7568025  -0.95892427 -0.2794155
       0.6569866   0.98935825  0.41211849 -0.54402111]
       
     np.tan(a)
     [ 1.55740772 -2.18503986 -0.14254654  1.15782128 -3.38051501 -0.29100619
       0.87144798 -6.79971146 -0.45231566  0.64836083]
       
     # aggregation
     np.max(a) # maximal value
     10
     
     np.min(a) # minimal value    
     1
     
     np.sum(a) # sum of items
     55
     
     a = np.array([[1,2,3], [4,5,6], [7,8,9]])
     a.sum(axis=0) # sum of columns
     [12 15 18]
     
     a.sum(axis=1) # sum of rows
     [ 6 15 24]
     
     # complex numbers
     a = 2 + 2j # use j for imaginary unit instead of i
     
     (2+2j)
     
     np.real(a) # real part
     2.0
     
     np.imag(a) # imaginary part
     2.0
     
     np.abs(a) # absolute value
     2.82842712475
     
     np.angle(a) # phase
     0.785398163397
     
     np.conj(a) # complex conjugate
     (2-2j)