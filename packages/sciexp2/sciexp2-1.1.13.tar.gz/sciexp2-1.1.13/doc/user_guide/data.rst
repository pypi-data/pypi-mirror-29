.. _data:

Experiment evaluation --- `~sciexp2.data`
=========================================

The purpose of the `~sciexp2.data` module is to ease the extraction and manipulation of experiment results. The main abstraction is the `sciexp2.data.Data` object, an N-dimensional array that is derived from NumPy's `numpy.ndarray`.

The structure and its routines are designed in a way that the per-experiment information is retained (i.e., each array element has an associated :term:`instance` identifying the experiment where it came from). This is specially useful when evaluating the results of a big number of experiments, since the user can perform calculations at the semantic level, like analyzing certain subsets of experiments that match a given :term:`filters <filter>`, or computing the average execution time of all experiments, grouped by benchmark. It is thus also useful to use `matplotlib <http://matplotlib.org>`_ to plot these results, since it is also based on Python.

The examples in this section assume you're managing the results of the example experiments presented in :ref:`launchgen`.


Script preparation
------------------

In order to avoid some typing in the script, the `sciexp2.data.env` module can be used. It provides all the top-level functions related to the `~sciexp2.data.Data` object (together with a few other goodies)::

  #!/usr/bin/env python
  # -*- python -*-

  from sciexp2.data.env import *

  # file contents ...


Extract results from finished experiments
-----------------------------------------

Extraction routines are provided for different file formats in the `sciexp2.data.io` module. Assume the experiments produce result files in CSV format (comma-separated value), like the following example::

  time,cycles
  1000,10

You can easily extract them with `~sciexp2.data.io.extract_txt`::

  >>> data = extract_txt('experiments/res/@benchmark@-@argset@-@cores@-@l1@-@l1_assoc@-@l2@-@l2_assoc@.done')
  >>> data
  data_array([(1000,10), ..., (2000, 20)],
             dtype=[('time', int), ('cycles', int)],
             dims=[('@benchmark@-@argset@-@cores@-@l1@-@l1_assoc@-@l2@-@l2_assoc@',
                    ['foo-0-1-2-1-2-1',
                     ...,
                     'baz-2-4-32-4-512-4'])])

The result contains as many elements as extracted source files, and as many "fields" as columns on every source file (extraction produces `structured arrays <http://docs.scipy.org/doc/numpy/user/basics.rec.html>`_).

The extraction routines take every :term:`variable` in the ``source`` :term:`expression` and place it as a variable in the dimension metadata of the resulting array. Thus every element in the result relates to the variables of the source file that produced it.

.. note::

   By default, NumPy will only show the array values when using ``print(data)``. To see all the information (including metadata), use ``print(repr(data))``.


Manually creating arrays
------------------------

You can create arrays manually with either `~sciexp2.data.Data` or `~sciexp2.data.data_array`. By default, they will have no dimension metadata, but the ``dims`` argument can be provided with its contents::

  data_array([[1000, 10], [2000, 20]],
             dtype=int,
             dims=[('@benchmark@:@argset@:@cores@:@l1@:@l1_assoc@:@l2@:@l2_assoc@',
                    ['foo:0:1:2:1:2:1', 'baz:2:4:32:4:512:4']),
                   ('@metric@', ['time', 'cycles'])])

This array is similar to the one we got with `~sciexp2.data.io.extract_txt` in the previous example, but instead of fields, it has an extra dimension. Note also that the expression for the first dimension in this example is slightly different, showing that they can contain arbitrary text.

Dimension metadata accepts many different formants, and some of its elements can be missing; see the documentation of `~sciexp2.data.Data` for further information.



Changing the shape of arrays
----------------------------

Since extraction routines return a 1-dimensional array, it is usually common to reorganize its dimensions using `~sciexp2.data.Data.reshape`. For example, we can reshape the extracted array to have the ``benchmark`` variable in a separate dimension::

  >>> rdata = data.reshape(["benchmark"],
                           ["argset", "cores", "l1", "l1_assoc", "l2", "l2_assoc"])
  >> rdata
  data_array([[(1000, 10), ..., (1100, 11)],
              ...,
              [(-1, -1), ..., (2000, 20)]],
             dtype=[('time', int), ('cycles', int)],
             dims=[('@benchmark@', ['foo', ..., 'baz']),
                   ('@argset@-@cores@-@l1@-@l1_assoc@-@l2@-@l2_assoc@',
                    ['0-1-2-1-2-1', ..., '2-4-32-4-512-4'])])

This reshaping operation can be later useful when, for example, computing the per-benchmark average execution time of all experiments::

  >>> rdata["time"].mean(axis="benchmark")
  data_array([1025.0, ..., 1500.0],
             dtype=float,
             dims=[('@benchmark@', ['foo', ..., 'baz'])])

Note that in some cases, reshaping can produce new array elements that were missing on the original array; these elements will be "filled" with some type-specific value to indicate that they were originally missing. For example, if the original array missed an entry for ``baz-0-1-2-1-2-1``, the result will use ``-1`` to indicate that. You can change the default filling values with the ``filling_values`` argument.

During a reshape, you can also move a field into a dimension variable, or the other way around, with the ``fields_to_vars`` and ``vars_to_fields`` arguments::

  >>> data.reshape(fields_to_vars=["time"], vars_to_fields=["benchmark"])
  data_array([(10, 'foo'), ..., (20, 'baz')],
             dtype=[('cycles', int), ('benchmark', '|S300')],
             dims=[('@argset@-@cores@-@l1@-@l1_assoc@-@l2@-@l2_assoc@-@time@',
                    ['0-1-2-1-2-1-1000',
                     ...,
                     '2-4-32-4-512-4-2000'])])


Lazily manipulating arrays
--------------------------

It is common to start result analysis scripts by extracting and reshaping the data into an array that is later extensively used on the rest of the script. When having a big amount of source files, the extraction and reshaping can take a long time. The `~sciexp2.data.io.lazy` function can be used to store that "final" data array in disk, thus avoiding the steps unless necessay when re-executing the script::

  data = lazy(extract_txt, 'experiments/res/@benchmark@-@argset@-@cores@-@l1@-@l1_assoc@-@l2@-@l2_assoc@.done')
  rdata = data.reshape(["benchmark"],
                       ["argset", "cores", "l1", "l1_assoc", "l2", "l2_assoc"])
  rdata = rdata.realize("/tmp/data")

If the same source files are found in `~sciexp2.data.io.extract_txt` (and with the same contents), and if `~sciexp2.data.io.reshape` is called with the same arguments, the final ``rdata`` object will be loaded from the disk file ``"/tmp/data"``. Otherwise, the data will be recomputed and stored in the disk for future reference. See the documentation of `~sciexp2.data.io.lazy` and its related functions for saving intermediate results or lazily invoking user functions.


Indexing and slicing
--------------------

Indexing and slicing follows the same rules of `NumPy <http://docs.scipy.org/doc/numpy/reference/arrays.indexing.html>`_ arrays, including the use of `Ellipsis` and `numpy.newaxis`. In the case of `numpy.newaxis`, the new dimension that it creates will have empty metadata::

  >>> rdata
  data_array([[(1000, 10), ..., (1100, 11)],
              ...,
              [(-1,-1), ..., (2000, 20)]],
             dtype=[('time', int), ('cycles', int)],
             dims=[('@benchmark@', ['foo', ..., 'baz']),
                   ('@argset@-@cores@-@l1@-@l1_assoc@-@l2@-@l2_assoc@',
                    ['0-1-2-1-2-1', ..., '2-4-32-4-512-4'])])
  >>> rdata[..., np.newaxis]
  data_array([[[(1000, 10)], ..., [(1100, 11)]],
              ...,
              [[(-1, -1)], ..., [(2000, 20)]]],
             dtype=[('time', int), ('cycles', int)],
             dims=[('@benchmark@', ['foo', ..., 'baz']),
                   ('@argset@-@cores@-@l1@-@l1_assoc@-@l2@-@l2_assoc@',
                    ['0-1-2-1-2-1', ..., '2-4-32-4-512-4']),
                   None])


Wherever a NumPy function accepts the ``axis`` argument (usually `universal functions <http://docs.scipy.org/doc/numpy/reference/ufuncs.html>`_, like `~numpy.mean`), you can use any valid argument to the `Data.dims <sciexp2.data.Data.dims>` attribute to identify each dimension (see :ref:`data-dims` below):

* *Integers* identify the dimension by its index, like the original NumPy.
* *Variable names* (strings) identify the dimension by the name of a variable that it contains.
* *Expressions* (strings) identify the dimension by its expression.

.. note::

   NumPy specifies that if the ``axis`` argument is a sequence, it will identify multiple dimensions to act upon.


Basic indexing
~~~~~~~~~~~~~~

Like in NumPy arrays, `basic indexing  <http://docs.scipy.org/doc/numpy/reference/arrays.indexing.html#basic-slicing-and-indexing>`_ returns a `view <http://docs.scipy.org/doc/numpy/glossary.html#term-view>`_ of the original array. Besides the regular indexing and slicing using integers, `~sciexp2.data.Data` arrays also support other types of indexes:

* *Ticks* (strings) identify an element (instance) by the expansion of its dimension expression. Ticks are shown as the metadata when you print the `repr` of a `~sciexp2.data.Data` array.
* :term:`Filters <filter>` (strings or `~sciexp2.filter.Filter` instances) identify an element (instance) by matching its values to the given conditions. Alternatively, you can use the special variable `v_` provided by the `sciexp2.launchgen.env` module.
* *Instances* (dicts) serve as an optimized shortcut to indexing using a filter.

The following examples are thus equivalent::

  >>> rdata['time'][0, -1:]
  data_array([1000],
             dims=[('@argset@-@cores@-@l1@-@l1_assoc@-@l2@-@l2_assoc@',
                    ['2-4-32-4-512-4'])])
  >>> np.all(rdata['time'][0, -1:] == rdata['time']['foo',
  ...                                               '2-4-32-4-512-4':])
  True
  >>> np.all(rdata['time'][0, -1:] == rdata['time']["benchmark == 'foo'",
  ...                                               'argset == 2 && cores == 4 && l1 == 32 && l1_assoc == 4 && l2 == 512 && l2_assoc == 4':])
  True
  >>> np.all(rdata['time'][0, -1:] == rdata['time'][v_.benchmark == "foo",
  ...                                               (v_.argset == 2) & (v_.cores == 4) & (v_.l1 == 32) & (v_.l1_assoc == 4) & (v_.l2 == 512) & (v_.l2_assoc == 4):])
  True
  >>> np.all(rdata['time'][0, -1:] == rdata['time'][{'benchmark': 'foo'},
  ...                                               {'argset': 2, 'cores': 4, 'l1': 32, 'l1_assoc': 4, 'l2': 512, 'l2_assoc': 4}:])
  True

.. note::

   When a string is provided for indexing, a `~sciexp2.data.Data` array will first try using it as a filter, and if that fails, it will use it as a tick.


Advanced indexing
~~~~~~~~~~~~~~~~~

Like in NumPy arrays, `advanced indexing  <http://docs.scipy.org/doc/numpy/reference/arrays.indexing.html#advanced-indexing>`_ returns a copy of the original array; examples include using a index arrays and boolean arrays. Besides the indexing mechanisms supported by the basic indexing explained above, `~sciexp2.data.Data` arrays also support using a filter as the *step* field when slicing. In such cases, only the entries matching the given filter will be selected. The following examples are thus equivalent::

  >>> rdata['time'][[0, -1], 0]
  data_array([1000, -1],
             dims=[('@benchmark@', ['foo', 'baz'])])
  >>> np.all(rdata['time'][[0, -1], 0] == rdata['time'][[True, False, ...., False, True], 0])
  True
  >>> np.all(rdata['time'][[0, -1], 0] == rdata['time'][['foo', 'baz'], 0])
  True
  >>> np.all(rdata['time'][[0, -1], 0] == rdata['time'][::"benchmark in ['foo', 'baz']", 0])
  True
  >>> np.all(rdata['time'][[0, -1], 0] == rdata['time'][::"benchmark == 'foo' || benchmark == 'baz'", 0])
  True
  >>> np.all(rdata['time'][[0, -1], 0] == rdata['time'][::(v_.benchmark == "foo") | (v_.benchmark == "baz")])
  True


Dimension-oblivious indexing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When manipulating complex `~sciexp2.data.Data` arrays with multiple dimensions, it is often preferable to avoid positionally indexing every dimension. One reason is to avoid remembering on which dimension every variable is, or when programmatically building and index. It is also useful to make your code future-proof to changes in the array dimensions (i.e., to avoid adapting your code to the new array configuration).

Instead, you can use the `Data.indexer <sciexp2.data.Data.indexer>` attribute to build a `~sciexp2.data.DataIndexer` object. It will calculate the dimension positions for you and can be later used as an index into the actual `~sciexp2.data.Data` array. A `~sciexp2.data.DataIndexer` object can be indexed like a regular `~sciexp2.data.Data` array; the ``dims`` attribute can be used to select the dimensions to index (see :ref:`data-dims` below), and indexing in their result will produce indexing information tied to these dimensions::

  >>> idx = rdata.indexer
  >>> idx = idx.dims["benchmark"][["foo", "baz"]]
  >>> idx = idx.dims["cores"][0]
  >>> rdata["time"][idx]
  data_array([1000, -1],
             dims=[('@benchmark@', ['foo', 'baz'])])

.. warning::

   As of now, indexing more than once the same dimension will only retain the last indexing information.


If you are not going to reuse the indexer object (e.g., to index multiple arrays with the same configuration), you can use the `Data.idata <sciexp2.data.Data.idata>` attribute as an equivalent shortcut::

  >>> rdata["time"].idata["benchmark", "cores"][["foo", "baz"], 0]
  data_array([1000, -1],
             dims=[('@benchmark@', ['foo', 'baz'])])


.. _data-dims:

Dimension metadata manipulation
-------------------------------

`~sciexp2.data.Data` arrays provide the `~sciexp2.data.Data.dims` attribute, which can be indexed as a list to retrieve the per-dimension metadata, stored in `~sciexp2.data.meta.Dim` objects. Indexes can be any of:

* Dimension index (integer).
* Dimension variable (string).
* Dimension expression (string).

The following are thus equivalent::

  >>> rdata.dims[1]
  Dim('@argset@-@cores@-@l1@-@l1_assoc@-@l2@-@l2_assoc@',
      ['0-1-2-1-2-1', ..., '2-4-32-4-512-4'])
  >>> rdata.dims[1] is rdata.dims["cores"]
  True
  >>> rdata.dims[1] is rdata.dims["@argset@-@cores@-@l1@-@l1_assoc@-@l2@-@l2_assoc@"]
  True

Additionally, some of the `~sciexp2.data.meta.Dim` attributes offer views to different types of the dimension information:

* `Dim.indexes <sciexp2.data.meta.Dim.indexes>` shows the indexes of the selected elements.
* `Dim.ticks <sciexp2.data.meta.Dim.ticks>` shows the ticks (the per-instance expanded expression) of the selected elements.
* `Dim.instances <sciexp2.data.meta.Dim.instances>` shows the instances of the selected elements.

These provide the following output::

  >>> rdata.dims["benchmark"]
  Dim('@benchmark@',
      ['foo', 'bar', 'baz'])
  >>> list(rdata.dims["benchmark"].indexes)
  [0, 1, 2]
  >>> list(rdata.dims["benchmark"].ticks)
  ['foo', ..., 'bar']
  >>> list(rdata.dims["benchmark"].instances)
  [Instance({'benchmark': 'foo'}), Instance({'benchmark': 'bar'}), Instance({'benchmark': 'baz'})]

Among other operations, the `~sciexp2.data.meta.Dim` objects can, in turn, be indexed like `~sciexp2.data.Data` arrays, and the aforementioned attributes can too::

  >>> rdata.dims["benchmark"][::v_.benchmark == "bar"]
  Dim('@benchmark@',
      ['bar'])
  >>> rdata.dims["benchmark"].indexes[::v_.benchmark == "bar"]
  [1]
  >>> rdata.dims["benchmark"].ticks[::v_.benchmark == "bar"]
  ['bar']
  >>> rdata.dims["benchmark"].instances[::v_.benchmark == "bar"]
  [Instance({'benchmark': 'bar'})]

Finally, the dimension metadata of a `~sciexp2.data.Data` array can also be changed through assignments to the `Data.dims <sciexp2.data.Data.dims>` attribute, as well as through assignments to the `Dim.expression <sciexp2.data.meta.Dim.expression>` and contents of a `~sciexp2.data.meta.Dim` object. See their respective documentation for more information.
