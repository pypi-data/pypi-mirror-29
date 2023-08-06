
Paramcontainer
==============

This notebook shows how the class :class:`fluiddyn.util.paramcontainer.ParamContainer` can be used. 

.. code:: ipython3

    from fluiddyn.util.paramcontainer import ParamContainer

Let's consider code taken from fluidimage. The object containing the
parameter is initialized in the package. It is first created empty:

.. code:: ipython3

    params = ParamContainer(tag='params')

We then fill it with default parameters:

.. code:: ipython3

    # taken from fluidimage.work.piv.singlepass
    params._set_child('piv0', attribs={
            'shape_crop_im0': 48,
            'shape_crop_im1': None,
            'displacement_max': None})
    
    params.piv0._set_doc("""Parameters describing one PIV step.""")
    
    params.piv0._set_child('grid', attribs={
        'overlap': 0.5,
        'from': 'overlap'})
    
    params.piv0.grid._set_doc("""
    Parameters describing the grid.
    
    overlap : float (0.5)
        Number smaller than 1 defining the overlap between interrogation windows.
    
    from : str {'overlap'}
        Keyword for the method from which is computed the grid.
    """)


There are other functions to add attribute to a child:

.. code:: ipython3

    params.piv0._set_attrib
    params.piv0._set_attribs




.. parsed-literal::

    <bound method ParamContainer._set_attribs of <fluiddyn.util.paramcontainer.ParamContainer object at 0x7f6c43fb8518>
    
    <piv0 displacement_max="None" shape_crop_im0="48" shape_crop_im1="None">
      <grid from="overlap" overlap="0.5"/>  
    
    </piv0>
    >



The ParamContainer object can be used in the code to generate the
documentation, as for example in this
`page <http://fluidimage.readthedocs.io/en/latest/generated/fluidimage.topologies.piv.html>`__.

Then the user has to modify the default parameters in a python script.
She/he can first create the object in ipython and play with it. The
representation of the object shows the parameters and their values:

.. code:: ipython3

    params.piv0




.. parsed-literal::

    <fluiddyn.util.paramcontainer.ParamContainer object at 0x7f6c43fb8518>
    
    <piv0 displacement_max="None" shape_crop_im0="48" shape_crop_im1="None">
      <grid from="overlap" overlap="0.5"/>  
    
    </piv0>



It is also easy to print the documentation (or part of the
documentation):

.. code:: ipython3

    params.piv0._print_doc()


.. parsed-literal::

    Documentation for params.piv0
    -----------------------------
    
    Parameters describing one PIV step.
    


.. code:: ipython3

    params.piv0._print_docs()


.. parsed-literal::

    Documentation for params.piv0
    -----------------------------
    
    Parameters describing one PIV step.
    
    Documentation for params.piv0.grid
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Parameters describing the grid.
    
    overlap : float (0.5)
        Number smaller than 1 defining the overlap between interrogation windows.
    
    from : str {'overlap'}
        Keyword for the method from which is computed the grid.
    


.. code:: ipython3

    params.piv0.grid._print_docs()


.. parsed-literal::

    Documentation for params.piv0.grid
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Parameters describing the grid.
    
    overlap : float (0.5)
        Number smaller than 1 defining the overlap between interrogation windows.
    
    from : str {'overlap'}
        Keyword for the method from which is computed the grid.
    


Modifying a value is as simple as

.. code:: ipython3

    params.piv0.grid.overlap = 0.2

.. code:: ipython3

    params.piv0.grid




.. parsed-literal::

    <fluiddyn.util.paramcontainer.ParamContainer object at 0x7f6c43fb8588>
    
    <grid from="overlap" overlap="0.2"/>  



A spelling mistake is clearly annonced by a AttributeError:

.. code:: ipython3

    try:
        params.piv0.grid.overlqp = 0.2
    except AttributeError as e:
        print(e)


.. parsed-literal::

    overlqp is not already set in grid.
    The attributes are: ['from', 'overlap']
    To set a new attribute, use _set_attrib or _set_attribs.

