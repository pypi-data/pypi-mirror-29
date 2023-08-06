.. _news:

Changes in SciExp²
==================

Here's a brief description of changes introduced on each version.


1.1.13
------

.. rubric:: External compatibility breaks

.. rubric:: New features

.. rubric:: Improvements

.. rubric:: Bug fixes

* Allow `sciexp2.common.utils.find_files` (and related) to search for directories (paths ending with "/").
* Fix `sciexp2.data.io.find_files` when using a job descriptor file.

.. rubric:: Documentation

* Fix documentation of `sciexp2.data.io.find_files`.
* Improve documentation of `sciexp2.data.io.extract_txt` and `sciexp2.data.io.extract_regex` regarding variable references and regular expressions.

.. rubric:: Internals

* Properly account progress indication in iterables.
* Fix `sciexp2.common.instance.InstanceGroup.dump` to only have the exported variables. Indirectly affects `sciexp2.data.io.find_files` when used with a job descriptor file.
* Improve Python 3 compatibility.


1.1.12
------

.. rubric:: External compatibility breaks

.. rubric:: New features

.. rubric:: Improvements

* Speedup construction of `sciexp2.data.Dim` objects by two orders of magnitude.
* Forward SIGINT and SIGTERM to user-specified commands in job scripts.
* Forward SIGINT to executing jobs with the shell backend (closes :issue:`293`).
* Forward SIGINT to executing commands with `sciexp2.launchgen.Launchgen.execute` (closes :issue:`293`).

.. rubric:: Bug fixes

.. rubric:: Documentation

.. rubric:: Internals

* Properly document `sciexp2.common.utils.OrderedSet.view` and `sciexp2.common.instance.InstanceGroup.view`.
* Add methods `sciexp2.common.utils.OrderedSet.set_view_able` and `sciexp2.common.instance.InstanceGroup.set_view_able`.
* Improve Python 3 compatibility.


1.1.11
------

.. rubric:: External compatibility breaks

.. rubric:: New features

.. rubric:: Improvements

.. rubric:: Bug fixes

* Fix progress message logging.
* Fix length calculation of progress operations.
* Export relevant variables to user-provided job commands.

.. rubric:: Documentation

.. rubric:: Internals


1.1.10
------

.. rubric:: External compatibility breaks

* Remove ``default_launchgen`` and its methods from module `sciexp2.launchgen.env` (you should explicitly instantiate `sciexp2.launchgen.Launcher` instead).

.. rubric:: New features

.. rubric:: Improvements

* Use package ``tqdm`` to show fancier progress indicators.
* Detect when we're running in a IPython/Jupyter notebook and use proper progress widgets when available.
* Make sure the output of the user's commands in launchgen's default templates is properly seen during interactive execution.
* Add method `sciexp2.data.Data.sort` (closes :issue:`307`).

.. rubric:: Bug fixes

* Fix construction of `~sciexp2.launchgen.Launcher` objects from other objects of the same type.
* Fix handling of argument ``append`` in `sciexp2.launchgen.Launcher.params` when applied to an empty object.
* Support `sciexp2.data.Data` dimensions with missing elements and elements with missing variable values.

.. rubric:: Documentation

* Extend and clarify quickstart, installation and basic concepts.
* Extend and clarify the user guide for `~sciexp2.launchgen`.
* Extend and clarify the installation and execution guide.

.. rubric:: Internals

* Remove unused progress indicator `sciexp2.common.progress.LVL_MARK`.


1.1.9
-----

.. rubric:: External compatibility breaks

.. rubric:: New features

.. rubric:: Improvements

.. rubric:: Bug fixes

* Fix bug in compatibility code handling argument inspection of functions.
* Fix compatibility code to detect unused arguments in older numpy versions.

.. rubric:: Documentation

.. rubric:: Internals


1.1.8
-----

.. rubric:: External compatibility breaks

.. rubric:: New features

.. rubric:: Improvements

* Do not crash progress reports when running on an IPython notebook.

.. rubric:: Bug fixes

* Fix expression and instance construction in `sciexp2.data.Data.flatten`.
* Fix indexing when using a filter on the last indexed dimension.
* Fix advanced indexing with boolean arrays.

.. rubric:: Documentation


.. rubric:: Internals


1.1.7
-----

.. rubric:: External compatibility breaks

.. rubric:: New features

.. rubric:: Improvements

.. rubric:: Bug fixes

* Fix dimension indexing in `sciexp2.data.DataDims`.

.. rubric:: Documentation

* Improve introduction.

.. rubric:: Internals


1.1.6
-----

.. rubric:: External compatibility breaks

.. rubric:: New features

.. rubric:: Improvements

.. rubric:: Bug fixes

* Fix parsing of the ``keepdims`` argument in `sciexp2.data.wrap_reduce` for newer numpy versions (which affects all reduction operations).
* Fix setuptools dependency on Python (again).

.. rubric:: Documentation

.. rubric:: Internals


1.1.5
-----

.. rubric:: External compatibility breaks

* Changed semantics of callables in `sciexp2.data.meta.Dim.sort` to be compatible with `sort` in Python 3.

.. rubric:: New features

.. rubric:: Improvements

.. rubric:: Bug fixes

* Properly fail ``launcher`` when an experiment errors-out and we're in ``DEBUG`` log level.
* Fix dependency timestamp computation in `sciexp2.data.io.lazy` and friends with Python 3.

.. rubric:: Documentation

.. rubric:: Internals

* Remove ``cmp`` argument on calls to `sort` to be compatible with Python 3.
* Improve compatibility with Python 3.
* Always show a stable element order when pretty-printing instances.


1.1.4
-----

.. rubric:: External compatibility breaks

.. rubric:: New features

.. rubric:: Improvements

.. rubric:: Bug fixes

* Fix setuptools dependency on Python.

.. rubric:: Documentation

.. rubric:: Internals


1.1.3
-----

.. rubric:: External compatibility breaks

.. rubric:: New features

* Add method `sciexp2.data.DataIndexer.as_tuple`.

.. rubric:: Improvements

* Improve output file initialization in the shell template.
* Ignore empty variable values in argument ``DEPENDS`` of `sciexp2.launchgen.Launchgen.launcher` (closes :issue:`298`).
* Do not warn when `sciexp2.data.io.lazy` receives only non-lazy arguments.

.. rubric:: Bug fixes

* Fix boolean negation operator in `~sciexp2.common.filter.Filter`.
* Fix `~sciexp2.data.Data.ravel`.

.. rubric:: Documentation

.. rubric:: Internals


1.1.2
-----

.. rubric:: External compatibility breaks

.. rubric:: New features

.. rubric:: Improvements

* Allow setting `~sciexp2.data.meta.Dim` ticks to ``None``.
* Remove most limitations of assignments to `sciexp2.data.meta.Dim.expression` and `sciexp2.data.meta.Dim` contents.
* Generalize the following functions to work with any type of arrays: `sciexp2.data.append`, `sciexp2.data.concatenate`, `sciexp2.data.copy`, `sciexp2.data.delete`, `sciexp2.data.drop_fields`, `sciexp2.data.imag`, `numpy.lib.recfunctions.merge_arrays`, `sciexp2.data.ravel`, `sciexp2.data.real`, `numpy.lib.recfunctions.rename_fields`.
* Improve output file initialization in the shell template.
* Ignore empty variable values in argument ``DEPENDS`` of `sciexp2.launchgen.Launchgen.launcher` (closes :issue:`298`).

.. rubric:: Bug fixes

* Properly escape `sciexp2.data.meta.Dim.expression` values to avoid confusing the user's string with parts of a regular expression.
* Fix boolean negation operator in `~sciexp2.common.filter.Filter`.
* Fix `~sciexp2.data.Data.ravel`.

.. rubric:: Documentation

.. rubric:: Internals

* Fix hard resets on `sciexp2.common.instance.InstanceGroup.cache_reset`.
* Fix `sciexp2.data.DataDims` copies.
* Implement consistent named axis selection (``axis`` argument in numpy function) when using multiple array arguments.
* Follow `numpy`'s exception format when using a non-existing field name.


1.1.1
-----

.. rubric:: External compatibility breaks

* Remove argument ``filters`` in `sciexp2.launchgen.Launchgen.expand` in favour of `sciexp2.launchgen.Launchgen.select` (closes :issue:`300`).
* Deprecate argument ``export`` in `sciexp2.launchgen.Launchgen.launcher` in favour of new value ``EXPORTS`` in argument ``values`` (closes :issue:`301`).

.. rubric:: New features

.. rubric:: Improvements

.. rubric:: Bug fixes

* Fix filter optimization (breaks construction from multiple filters).
* Allow comparing variables in `~sciexp2.common.filter.PFilter` with strings (fixes :issue:`302`, as a refinement of :issue:`278`).
* Do not complain when about empty views when using `sciexp2.launchgen.Launchgen` methods (fixes :issue:`296`).

.. rubric:: Documentation

* Clarify use cases of ``files`` sub-command in :program:`launcher`.
* Clarify how variables are substituted in `sciexp2.launchgen.Launchgen.params`.

.. rubric:: Internals

* Fix representation of strings in `~sciexp2.common.filter.Filter` objects (was breaking escape sequences, used in regular expressions).


1.1
---

.. rubric:: External compatibility breaks

* Remove `sciexp2.data.Data.dim_sort` and ``dim_sort`` argument in `sciexp2.data.Data.reshape` in favour of `sciexp2.data.meta.Dim.sort`.
* Remove unused "filter override" operator.
* Deprecate "add" operation in `~sciexp2.common.filter.Filter` in favour of "and".
* Forbid `~sciexp2.data.Data` indexing with intermediate results from `~sciexp2.data.DataIndexer`.

.. rubric:: New features

* Allow sorting `sciexp2.data.Data` arrays using `sciexp2.data.meta.Dim.sort` (closes :issue:`279`).
* Add filter syntax to check variable existence (``exists(VAR)``; closes :issue:`262`).
* Add ``--inverse`` argument in :program:`launcher` to easily invert the job state selection (closes :issue:`287`).
* Add `sciexp2.data.meta.Dim.values` and  `sciexp2.data.meta.Dim.unique_values` to easily retrieve per-variable values (closes :issue:`290`).
* Add `sciexp2.launchgen.Launchgen.translate` and `sciexp2.launchgen.Launchgen.expand` to translate and expand expressions from instances (closes :issue:`276`).
* Add `sciexp2.data.Data.idata` attribute to allow immediate dimension-oblivious indexing (shortcut to `sciexp2.data.Data.indexer`; closes :issue:`282`).

.. rubric:: Improvements

* Auto-optimize filter matching.
* Using `sciexp2.launchgen.LaunchgenView.select_inverse` works properly on nested views (only inverts the last selection).
* Allow `sciexp2.launchgen.Launchgen.pack` to dereference symbolic links (closes :issue:`280`).
* Allow `sciexp2.data.Data.indexer` to accept `~sciexp2.common.filter.PFilter` instances (closes :issue:`284`).
* Allow arbitrary values to be returned by functions used through `sciexp2.data.io.lazy` and similar (closes :issue:`285`).
* Simplify use of variables in the ``files`` sub-command of :program:`launcher` (closes :issue:`281`).
* Allow selecting multiple dimensions in `sciexp2.data.DataDims` and `sciexp2.data.DataIndexer`.

.. rubric:: Bug fixes

* Fix bug in string representation for `sciexp2.common.filter.Filter`.
* Fix indexing in `~sciexp2.data.meta.Dim` when using filters as a start and/or stop slice.
* Fix management of ``DONE`` and ``FAIL`` files in the shell template.
* Fix merging of `~sciexp2.common.filter.PFilter` with strings (closes :issue:`278`).
* Fix result of "or" operation in `~sciexp2.common.filter.Filter`.
* Fix array element-wise comparison (metadata is ignored for now).
* Make indexing logic more robust (closes :issue:`283`).

.. rubric:: Documentation

.. rubric:: Internals

* Add method `sciexp2.common.utils.OrderedSet.copy`.
* Add methods `sciexp2.common.utils.OrderedSet.sorted` and `sciexp2.common.utils.OrderedSet.sort`.
* Add method `sciexp2.common.instance.InstanceGroup.sorted`.
* Implement `sciexp2.common.instance.InstanceGroup.sort` as in-place sorting.
* Auto-optimize simple boolean filter expressions.
* Drop argument ``allowed`` in `~sciexp2.common.filter.Filter` (use `~sciexp2.common.filter.Filter.validate` instead).
* Drop method `sciexp2.common.filter.Filter.constant`.
* Provide exception check callback for missing variable references in `~sciexp2.common.instance.InstanceGroup.select` and `~sciexp2.common.instance.InstanceGroup.expand`.
* Drop argument ``allow_unknown`` from `sciexp2.common.filter.Filter.match`; handle from clients instead.
* Never return an `~numpy.ndarray` in `~sciexp2.data.meta.Data._get_indexes` (work around NumPy bug `#6564 <https://github.com/numpy/numpy/issues/6564>`_).
* Allow variables in `~sciexp2.common.utils.find_files` to span more than one directory (closes :issue:`288`).


1.0.2
-----

.. rubric:: External compatibility breaks

.. rubric:: New features

.. rubric:: Improvements

* Show progress message when building new dimensions in `sciexp2.data.Data.reshape`.
* Improve performance of `sciexp2.data.Data.reshape`.

.. rubric:: Bug fixes

* Fix spurious ignored `AttributeError` exceptions when using `~sciexp2.common.progress`.

.. rubric:: Documentation

.. rubric:: Internals


1.0.1
-----

.. rubric:: External compatibility breaks

.. rubric:: New features

.. rubric:: Improvements

* Return ``None`` in `sciexp2.data.meta.Dim.index` when dimension is not associated.

.. rubric:: Bug fixes

* Fix `sciexp2.data.meta.Dim` association when indexing.

.. rubric:: Documentation

.. rubric:: Internals


1.0
---

.. rubric:: External compatibility breaks

* Move dimension-related classes to `sciexp2.data.meta` (with shortened names).
* `sciexp2.data.meta.Dim` constructor no longer performs copies, use `sciexp2.data.meta.Dim.copy` instead.
* Remove argument `copy_dims` from `~sciexp2.data.Data`.
* Remove methods `sciexp2.data.Data.dim` and `sciexp2.data.Data.dim_index` in favour of `sciexp2.data.Data.dims` and `sciexp2.data.meta.Dim.index`, respectively.
* Remove method `sciexp2.data.Data.iteritems`.
* Remove attribute `sciexp2.data.meta.Dim.contents`.
* Remove deprecated (since 0.18) argument `promote` in in data extraction routines (`sciexp2.data.io`).

.. rubric:: New features

* Add `sciexp2.data.meta.Dim.instances` attribute to access the instances of a dimension.
* Add `sciexp2.data.meta.Dim.translate` and `sciexp2.data.meta.Dim.extract`.
* Add `sciexp2.data.DataDims` to query and manipulate collections of dimension metadata objects.
* Allow `~sciexp2.data.meta.Dim` objects with missing ticks or empty expression (closes :issue:`243`).
* Allow `~sciexp2.data.Data` objects with empty dimension metadata (closes :issue:`242`).
* All views of a `~sciexp2.data.Data` object have consistent metadata.
* Allow element and ``expression`` assignments to `~sciexp2.data.meta.Dim` objects (closes :issue:`236`).
* Unhandled `~numpy.ndarray` methods now return a `~sciexp2.data.Data` object without metadata.
* Add `~sciexp2.data.Data.indexer` to facilitate alignment of indexes to dimensions.

.. rubric:: Improvements

* Export `~sciexp2.data.io.lazy_wrap`, `~sciexp2.data.io.lazy_wrap_realize` and `~sciexp2.data.io.lazy_wrap_checkpoint` through `sciexp2.data.env`.
* Return a `~sciexp2.data.Data` when using `~numpy.newaxis` or advanced indexing.
* Allow ``axis`` `numpy.ufunc` argument with multiple values (closes :issue:`274`).
* Let ``keepdims`` `numpy.ufunc` argument return a `~sciexp2.data.Data` object (closes :issue:`275`).
* Return a `~sciexp2.data.Data` object with empty metadata when broadcasting to a `~numpy.ndarray` argument.

.. rubric:: Bug fixes

* Fixed indexing results on `sciexp2.data.meta.Dim.instances`.

.. rubric:: Documentation

* Add a quick example of all modules in the introduction.
* Document array and metadata indexing and manipulation in the user guide.

.. rubric:: Internals

* Move free functions for `~sciexp2.data.Data` objects into `sciexp2.data._funcs`.
* Rename `sciexp2.data.meta.ExpressionError` as `~sciexp2.data.meta.DimExpressionError`.
* Refactor dimension expression logic into `sciexp2.data.meta.DimExpression`.
* Add `~sciexp2.common.progress.progressable_simple` to wrap container iterations with a progress indicator.
* Sanitize `sciexp2.data.meta.Dim` construction.
* Remove the ``EXPRESSION`` internal variable from dimension metadata, making it smaller at the expense of more complex expression lookups (closes :issue:`231`).
* Remove the ``INDEX`` internal variable from dimension metadata, making it smaller at the expense of more costly index lookups.
* Allow constructing views of `sciexp2.data.meta.Dim` objects.


Older versions
--------------

:ref:`news-old`.
