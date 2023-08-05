***********************************
Overview / Installation
***********************************

pyGDM2 is available on `pypi <https://pypi.python.org/pypi/pygdm2/>`_ and `gitlab <https://gitlab.com/wiechapeter/pyGDM2>`_. 

Detailed documentation with many examples is avaiable at the `pyGDM2 documentation website <https://wiechapeter.gitlab.io/pyGDM2-doc/>`_. See also the `documentation paper on arXiv (1802.04071) <https://arxiv.org/abs/1802.04071>`_




Requirements
================================

Python
------------------
    - **python** (2.7, `python <https://www.python.org/>`_)
    - **numpy** (`numpy <http://www.numpy.org/>`_)
    - **python 2 headers** (under linux, install the package *python-dev* or *python-devel*)


Fortran
------------------
    - *fortran* compiler (tested with **gfortran**. `gcc <https://gcc.gnu.org/fortran/>`_)
    - **openmp** (`openmp <http://www.openmp.org/>`_)
    - **f2py** (comes with **numpy**. `link <http://www.numpy.org/>`_)


Optional Python packages
-------------------------------------
    - **scipy** (*Strongly recommended*. Used for standard solver LU decomposition and several tools. `scipy <https://www.scipy.org/>`_)
    - **matplotlib** (*Strongly recommended*. For all 2D visualization tools. `matplotlib <https://matplotlib.org/>`_)
    - **mpi4py** (for MPI parallelized calculation of spectra. `mpi4py <http://mpi4py.readthedocs.io/en/stable/>`_)
    - **mayavi** (for all 3D visualization. `mayavi <http://docs.enthought.com/mayavi/mayavi/mlab.html>`_)
    - **PIL** (image processing. `PIL <https://pypi.python.org/pypi/PIL>`_)
    - **PaGMO / PyGMO** (version 2.4+. *Required* for the **EO** submodule. `pagmo <https://esa.github.io/pagmo2/>`_)

(all available via `pip <https://pypi.python.org/pypi/pip>`_)



Installation under Unix
=============================================

Via pip
-------------------------------

Install from pypi repository via

.. code-block:: bash
    
    $ pip install pygdm2



Via setup script
-------------------------------

The easiest possibility to compile (and install) pyGDM is via the 
setup-script, which uses the extended *distutils* from *numpy*. 

To install pyGDM, run in the source directory:

.. code-block:: bash
    
    $ python setup.py install

To install to a user-defined location, use the *prefix* option:

.. code-block:: bash
    
    $ python setup.py install --prefix=/some/specific/location


To only compile without installation, use

.. code-block:: bash
    
    $ python setup.py build




Manual compilation
-------------------------------------------------------------

1. clone git:

   .. code-block:: bash
    
        $ git clone https://gitlab.com/wiechapeter/pyGDM2.git

2. compile fortran parts:

   .. code-block:: bash
    
        $ cd fortranBase
        $ make

3. *optional, for system-wide usage* add to **path** and **pythonpath**, 
   e.g. add following lines to file "/home/USER/.profile", where 
   "path_of_pyGDM_folder" is the pyGDM installation directory:
  
   .. code-block:: bash
    
        PATH="path_of_pyGDM_folder:$PATH"
        export PATH
        
        PYTHONPATH="path_of_pyGDM_folder:$PYTHONPATH"
        export PYTHONPATH



Authors
=========================

Python code
------------------------
   - P\. R. Wiecha


Fortran code
-------------------------
   - C\. Girard
   - A\. Arbouet
   - R\. Marty
   - P\. R. Wiecha



   


