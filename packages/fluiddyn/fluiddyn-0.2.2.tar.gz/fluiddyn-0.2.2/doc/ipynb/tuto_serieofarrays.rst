
Serieofarrays
=============

This notebook focuses on demonstrating how the classes :class:`fluiddyn.util.serieofarrays.SeriesOfArrays` can be used. 

This class can be used to create subsets from series of files. Let's first import it:

.. code:: ipython3

    from fluiddyn.util.serieofarrays import SeriesOfArrays

This class works with a serie of files (or a file containing a serie of
arrays) so we first need to create files. For this demo, we just create
emtpy files.

.. code:: ipython3

    import os
    
    path_dir = 'tmp_singleframe'
    if not os.path.exists(path_dir):
        os.mkdir(path_dir)
    for i0 in range(6):
        with open(path_dir + f'/image{i0}.png', 'w') as f:
            pass
        
    print(os.listdir(path_dir))


.. parsed-literal::

    ['image3.png', 'image0.png', 'image4.png', 'image2.png', 'image5.png', 'image1.png']


We write a simple function to print the subsets of files that we are
going to create...

.. code:: ipython3

    def print_subsets(series):
        for serie in series:
            print('(', end='')
            for name in serie.iter_name_files():
                print(name, end=', ')
            print(')')

We show that we can create many different subsets quite easily:

.. code:: ipython3

    series = SeriesOfArrays('tmp_singleframe/im*', 'i:i+2')
    print_subsets(series)


.. parsed-literal::

    (image0.png, image1.png, )
    (image1.png, image2.png, )
    (image2.png, image3.png, )
    (image3.png, image4.png, )
    (image4.png, image5.png, )


.. code:: ipython3

    series = SeriesOfArrays('tmp_singleframe/im*', 'i:i+2', ind_step=2)
    print_subsets(series)


.. parsed-literal::

    (image0.png, image1.png, )
    (image2.png, image3.png, )
    (image4.png, image5.png, )


.. code:: ipython3

    series = SeriesOfArrays('tmp_singleframe/im*', 'i:i+3', ind_stop=3)
    print_subsets(series)


.. parsed-literal::

    (image0.png, image1.png, image2.png, )
    (image1.png, image2.png, image3.png, )
    (image2.png, image3.png, image4.png, )


.. code:: ipython3

    series = SeriesOfArrays('tmp_singleframe/im*', 'i:i+3:2')
    print_subsets(series)


.. parsed-literal::

    (image0.png, image2.png, )
    (image1.png, image3.png, )
    (image2.png, image4.png, )
    (image3.png, image5.png, )


Let's consider another serie of files this time with two indices:

.. code:: ipython3

    path_dir = 'tmp_doubleframe'
    if not os.path.exists(path_dir):
        os.mkdir(path_dir)
    for i0 in range(3):
        with open(path_dir + f'/im_{i0}a.png', 'w') as f:
            pass
        with open(path_dir + f'/im_{i0}b.png', 'w') as f:
            pass
        
    print(os.listdir(path_dir))


.. parsed-literal::

    ['im_2b.png', 'im_0b.png', 'im_1b.png', 'im_1a.png', 'im_2a.png', 'im_0a.png']


Creating subsets of files is still very simple:

.. code:: ipython3

    series = SeriesOfArrays('tmp_doubleframe/im*', 'i, 0:2')
    print_subsets(series)


.. parsed-literal::

    (im_0a.png, im_0b.png, )
    (im_1a.png, im_1b.png, )
    (im_2a.png, im_2b.png, )


.. code:: ipython3

    series = SeriesOfArrays('tmp_doubleframe/im*', '0:2, i')
    print_subsets(series)


.. parsed-literal::

    (im_0a.png, im_1a.png, )
    (im_0b.png, im_1b.png, )


Of course we can do many more things with these objects:

.. code:: ipython3

    print([name for name in dir(series) if not name.startswith('__')])


.. parsed-literal::

    ['get_name_all_arrays', 'get_name_all_files', 'get_next_serie', 'get_serie_from_index', 'ind_start', 'ind_step', 'ind_stop', 'indslices_from_indserie', 'iserie', 'nb_series', 'serie', 'set_index_series']


.. code:: ipython3

    print([name for name in dir(series.serie) if not name.startswith('__')])


.. parsed-literal::

    ['_compute_strindices_from_indices', '_from_movies', '_index_lens', '_index_separators', '_index_slices', '_index_slices_all_files', '_index_types', '_separator_base_index', 'base_name', 'check_all_arrays_exist', 'check_all_files_exist', 'compute_indices_from_name', 'compute_name_from_indices', 'extension_file', 'filename_given', 'get_array_from_index', 'get_array_from_indices', 'get_array_from_name', 'get_arrays', 'get_index_slices', 'get_index_slices_all_files', 'get_name_arrays', 'get_name_files', 'get_nb_arrays', 'get_nb_files', 'get_path_all_files', 'get_path_arrays', 'get_path_files', 'isfile', 'iter_arrays', 'iter_indices', 'iter_name_arrays', 'iter_name_files', 'iter_path_files', 'nb_indices', 'nb_indices_name_file', 'path_dir', 'set_index_slices']

