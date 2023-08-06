.. _tutor_numeric_tut2_matplotlib:

Tutorial 2: Matplotlib
======================

This sections shows several examples how to use module Matplotlib.
See module `homepage <http://www.matplotlib.org/>`_ for more tutorials, reference manual.

Basic graph
^^^^^^^^^^^

  .. code-block:: python
  
     import numpy as np
     import matplotlib.pyplot as plt
     
     # data generation
     x = np.linspace(-np.pi, np.pi, 100)
     y = np.sin(x)
     
     # display
     plt.figure()
     plt.plot(x, y)
     plt.show()
     
     # store figure
     plt.savefig('fig.png')
     
  .. image:: fig/matplotlib_01_basic_graph.png

Labels
^^^^^^
  
  .. code-block:: python
  
     # axis labels
     plt.xlabel('--> x')
     plt.ylabel('--> y')  
     
     # axis borders
     plt.xlim(-3.15, 3.15)
     plt.ylim(-1, 1)   
     
     # title inc. LaTeX syntax
     plt.title(r'y = $\sin$(x)') 
     
     # graph
     plt.grid('on')
     plt.plot(x, y, color='r')
     plt.show()
     
  .. image:: fig/matplotlib_02_labels.png   
  
Multiple graphs
^^^^^^^^^^^^^^^

  .. code-block:: python
  
     # graphs in single plot
     z = np.cos(x)
     plt.plot(x, y, label=r'$\sin$(x)')
     plt.plot(x, z, label=r'$\cos$(x)')
     plt.legend()
     plt.show()
     
  .. image:: fig/matplotlib_03_mult_plot.png        
     
  .. code-block:: python
  
     # subplots
     plt.subplot(211)
     plt.plot(x, y)
     plt.title(r'$\sin$(x)')
     
     plt.subplot(212)
     plt.plot(x, z)
     plt.title(r'$\cos$(x)')   
     
     plt.show()
     
  .. image:: fig/matplotlib_04_subplot.png
  
Special graphs
^^^^^^^^^^^^^^

  .. code-block:: python
  
     x = np.linspace(-np.pi, np.pi, 20)
     y = np.sin(x)  
  
     # stem graph
     plt.subplot(211)
     plt.stem(x, y)
     plt.title('stem graph')
     
     # bar graph
     plt.subplot(212)
     plt.bar(x, y)
     plt.title('bar graph')    
     
  .. image:: fig/matplotlib_05_stem_bar.png
  
  .. code-block:: python
  
     # scatter, non-correlated data
     x = np.random.uniform(-10, 10, 100) # uniform distribution (-10,10)
     y = np.random.uniform(-10, 10, 100)
     plt.subplot(211)
     plt.scatter(x, y)
     plt.title('non-correlated data')
     
     # scatter, correlated data         
     x = np.linspace(-10, 10, 100)
     y = x + np.random.normal(2, 2, 100) # normal distribution, mean=2, standard deviation=2  
     plt.subplot(212)
     plt.scatter(x, y)
     plt.title('correlated data')   
     
  .. image:: fig/matplotlib_06_scatter.png
  
  .. code-block:: python
  
     # histogram
     plt.subplot(211)
     plt.hist(y, 50) # 50 buckets
     plt.title('histogram')
     
     # boxplot            
     plt.subplot(212)
     plt.boxplot(y)
     plt.title('boxplot')
     
  .. image:: fig/matplotlib_07_hist_boxplot.png     
  
  .. code-block:: python
  
     # pie chart
     x = np.array([10,30,40,15,5,10]) # percentage
     labels = ['item 1', 'item 2', 'item 3', 'item 4', 'item 5', 'item 6']
     plt.pie(x, autopct='%1.1f%%', labels=labels, explode=[0.1]*6, shadow=True)
     
  .. image:: fig/matplotlib_08_pie.png
  
  .. code-block:: python
  
     # polar coordinates
     phi = np.arange(0, 2*np.pi, 2*np.pi/120) # 120 samples
     rho = np.linspace(0, 1, len(phi))        # spiral
     plt.polar(phi, rho)
     plt.title('polar')        
     
  .. image:: fig/matplotlib_09_polar.png     
  
  .. code-block:: python
  
     # contour
     x = np.arange(-1.5, 1.5, 0.1)
     y = np.arange(-1.5, 1.5, 0.1)
     X, Y = np.meshgrid(x, y)
     Z = X**2 + Y**2
     plt.contour(Z, N=np.arange(-1, 1.5, 0.3))
     plt.title('contour') 
     
  .. image:: fig/matplotlib_10_contour.png  
  
  .. code-block:: python
  
     from mpl_toolkits.mplot3d import Axes3D
  
     # surface
     fig = plt.figure()
     ax = fig.gca(projection='3d')
     ax.plot_surface(X, Y, Z)
     plt.title('surface')
     
  .. image:: fig/matplotlib_11_surface.png       
     
  .. code-block:: python     
     
     # wireframe   
     fig = plt.figure()
     ax = fig.gca(projection='3d')     
     ax.plot_wireframe(x, y, z)
     plt.title('wireframe')
     
  .. image:: fig/matplotlib_12_wireframe.png       