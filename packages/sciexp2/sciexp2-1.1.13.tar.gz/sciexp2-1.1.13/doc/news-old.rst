.. _news-old:

Older SciExp² versions
======================


0.18.2
------

.. rubric:: External compatibility breaks

.. rubric:: New features

* Lazy result realization also works without a file path (see `~sciexp2.data.io.lazy`).
* Add `~sciexp2.data.io.lazy_wrap`, `~sciexp2.data.io.lazy_wrap_realize` and `~sciexp2.data.io.lazy_wrap_checkpoint` to streamline use of lazily evaluated functions.
* Allow per-variable conversion rules in `~sciexp2.data.io.extract_regex` (closes :issue:`270`).

.. rubric:: Improvements

* Use default value if converter fails in `~sciexp2.data.io.extract_regex`.
* Show an error message (instead of throwing an exception) if job submission fails.
* Add argument ``--keep-going`` to :program:`launcher` to keep submitting jobs even if others fail.
* Provide a crude string representation of lazy results (`~sciexp2.data.io.lazy`).

.. rubric:: Bug fixes

* Make `~sciexp2.data.wrap_reduce` more resilient (closes :issue:`269`).
* Apply converters in `~sciexp2.data.io.extract_txt` for string fields.
* Fix missing value handling in first line for `~sciexp2.data.io.extract_regex`.
* Apply user conversions on missing values for `~sciexp2.data.io.extract_regex` (closes :issue:`268`).
* Fix dtype detection when using ``vars_to_fields`` (data extraction and reshaping).
* Remove output file if there is an error during lazy result realization.

.. rubric:: Documentation

* Document converters and default values in `~sciexp2.data.io.extract_txt`.

.. rubric:: Internals


0.18.1
------

.. rubric:: External compatibility breaks

.. rubric:: New features

.. rubric:: Improvements

.. rubric:: Bug fixes

.. rubric:: Documentation

.. rubric:: Internals

* Switch to Git repository.


0.18
----

.. rubric:: External compatibility breaks

* New argument `fields_to_vars` in data extraction routines (`sciexp2.data.io`; deprecates argument `promote`).
* Rename argument `columns` into `fields` in `~sciexp2.data.io.extract_txt`.
* Rename argument `rows` into `fields` in `~sciexp2.data.io.extract_regex`.

.. rubric:: New features

* Add generic data extraction routine `~sciexp2.data.io.extract_func` (closes :issue:`233`).
* Add support for gzip-compressed source files in data extraction routines for `~sciexp2.data.io` (closes :issue:`232`).
* Add function `~sciexp2.data.data_frombuffer` (closes :issue:`194`).
* Add function `~sciexp2.data.data_memmap`.
* Add argument `fields_to_vars` in `~sciexp2.data.Data.reshape`.
* Add argument `vars_to_fields` in data extraction routines (`sciexp2.data.io`) and `~sciexp2.data.Data.reshape` (closes :issue:`241`).

.. rubric:: Improvements

* Add support for "multi-comparisons" in filters  (e.g., ``1 < a < 3``).
* Allow pattern binding operations with any type of arguments in filters.
* Add support for lists in filters (e.g., ``[1, 2, b]``).
* Add support for list membership checks in filters (e.g., ``a in [1, 3, 5]``).

.. rubric:: Bug fixes

* Fix handling of unary minus operator in filters.
* Fix handling of override operator in filters.

.. rubric:: Documentation

* Improve documentation of routines in `sciexp2.data.io`.
* Initial user guide for the `sciexp2.data` package.

.. rubric:: Internals

* Reimplement `~sciexp2.data.io.extract_txt` and `~sciexp2.data.io.extract_regex` on top of `~sciexp2.data.io.extract_func`.


0.17.1
------

.. rubric:: External compatibility breaks

* Rename `sciexp2.data.Data.sort` as `~sciexp2.data.Data.dim_sort`, since `numpy.sort` already exists (closes :issue:`244`).
* Rename argument `order` in `~sciexp2.data.Data.reshape` as `dim_sort` to keep naming consistent.

.. rubric:: New features

.. rubric:: Improvements

* Lazy evaluation with `sciexp2.data.io.lazy` detects changes to the source code of functions passed as arguments, triggering a re-computation.

.. rubric:: Bug fixes

* Fix command line argument parsing of :program:`launcher` when using a job descriptor file as a binary.
* Fix reductions (`~sciexp2.data.wrap_reduce`) when the result has no dimensions (e.g., a single number).
* Fix indexing of `~sciexp2.data.Data` objects when using the old numeric-compatible basic slicing [#numeric-slicing]_.

.. rubric:: Documentation

.. rubric:: Internals

.. [#numeric-slicing] http://docs.scipy.org/doc/numpy/reference/arrays.indexing.html#basic-slicing


0.17
----

.. rubric:: External compatibility breaks

* Slicing a `~sciexp2.data.Dimension` always returns a new one (or `None`).

.. rubric:: New features

* Added dimension slicing helpers `~sciexp2.data.Dimension.indexes` and  `~sciexp2.data.Dimension.ticks`.
* Functions that have an `axis` argument can now identify a dimension by giving the name of one of its variables (closes :issue:`200`).

.. rubric:: Improvements

* Raise exception `~sciexp2.data.io.ConverterError` when the user-provided conversion functions in   `~sciexp2.data.io.extract_regex` fail.
* Slicing in `~sciexp2.data.Data` accepts anything that can be converted into a filter (e.g., `dict`; closes :issue:`235`).
* Slicing in `~sciexp2.data.Data` also accepts anything that can be converted into a filter (e.g., `dict`) as long as it selects one element (closes :issue:`230`).
* Fixed dimension metadata when performing binary operations with `~sciexp2.data.Data` objects (closes :issue:`54`).

.. rubric:: Bug fixes

* Raise `~sciexp2.data.io.EmptyFileError` when probing a file without matches during `~sciexp2.data.io.extract_regex`.
* Do not fail when using `~sciexp2.data.io.extract_txt` on files with one single column and row (closes :issue:`238`).
* Properly handle `~numpy.genfromtxt`-specific arguments in  `~sciexp2.data.io.extract_txt` (closes :issue:`239`).

.. rubric:: Documentation

.. rubric:: Internals

* Can pretty-print `~sciexp2.data.Dimension` instances.
* Provide copy constructor of `~sciexp2.data.Dimension` instances.
* Provide public `~sciexp2.data.wrap_reduce` and `~sciexp2.data.wrap_accumulate` methods to wrap existing numpy functions.


0.16
----

.. rubric:: External compatibility breaks

* Command :program:`launcher` now has a saner command and option syntax.
* New syntax for template descriptor files.
* Remove commands `monitor` and `reset` from :program:`launcher`.
* Removed variable `sciexp2.common.progress.SHOW` in favour of routine `~sciexp2.common.progress.level`.
* Changed the syntax of `~sciexp2.launchgen.Launchgen.execute` (it's compatible with the common single-string argument).

.. rubric:: New features

* Add commands `summary`, `variables` and `files` to :program:`launcher`.
* Template descriptors can refer to some of the variables defined by their parent.
* Template descriptors, `~sciexp2.launchgen.Launchgen.launcher` and :program:`launcher` can define additional job submission arguments.
* Program :program:`launcher` can define additional job killing arguments.
* Add simple begin/end progress indicator (`sciexp2.common.progress.LVL_MARK`).
* Add `~sciexp2.launchgen.file_contents` to simplify inserting the contents of a file as the value of a variable.
* Add support for parallel command execution in `~sciexp2.launchgen.Launchgen.execute` (closes :issue:`170`).

.. rubric:: Improvements

* Can now run launcher scripts even if the execution system is not installed (assumes no job is currently running).
* Improved error resilience in template scripts.
* All file-generation routines in  `~sciexp2.launchgen` will retain the permission bits of their source file.
* Be clever about interactive terminals when showing progress indicators.
* User can set the desired progress reporting level when using :program:`launcher`.
* Program :program:`launcher` now explicitly shows outdated jobs.

.. rubric:: Bug fixes

* Fix error when using `~sciexp2.common.instance.InstanceGroup.select` with a dict-based filter that contains a non-existing value.
* Fix path computation of ``STDOUT`` and ``STDERR`` files in the gridengine template.
* Properly handle operations through a `~sciexp2.launchgen.LaunchgenView`.
* Allow creating a `~sciexp2.launchgen.Launchgen` from a `~sciexp2.launchgen.LaunchgenView` (closes :issue:`228`).
* Fix creation of a `~sciexp2.launchgen.Launchgen` from a `~sciexp2.launchgen.Launchgen` or `~sciexp2.launchgen.LaunchgenView`.

.. rubric:: Documentation

* Point out availability of examples' input files on the source distribution.

.. rubric:: Internals

* Job submission no longer removes results; instead, job scripts do it themselves.
* Do not treat template variables ``DONE`` and ``FAIL`` as glob patterns.
* New module `~sciexp2.common.parallel` providing simple parallelization primitives.


0.15.4
------

.. rubric:: External compatibility breaks

.. rubric:: New features

.. rubric:: Improvements

.. rubric:: Bug fixes

* Fix data loss bug in `~sciexp2.common.utils.OrderedSet`.

.. rubric:: Documentation

.. rubric:: Internals


0.15.3
------

.. rubric:: External compatibility breaks

.. rubric:: New features

.. rubric:: Improvements

.. rubric:: Bug fixes

* Fix error during executable file generation in `~sciexp2.launchgen`.
* Fix test number detection in `~sciexp2.launchgen.Launchgen.find_SPEC`.

.. rubric:: Documentation

.. rubric:: Internals


0.15.2
------

.. rubric:: External compatibility breaks

.. rubric:: New features

.. rubric:: Improvements

.. rubric:: Bug fixes

* Add missing package declaration.

.. rubric:: Documentation

.. rubric:: Internals


0.15.1
------

.. rubric:: External compatibility breaks

.. rubric:: New features

* Add `sciexp2.data.Data.imag`, `sciexp2.data.imag`, `sciexp2.data.Data.real` and  `sciexp2.data.real`.

.. rubric:: Improvements

* Allow building new `~sciexp2.data.Data` instances by copying metadata from others.
* Any unimplemented method in `~sciexp2.data.Data` falls back to a `numpy.ndarray` and (by default) issues a warning (see `~sciexp2.data.WARN_UPCAST`).
* Add `sciexp2.data.Data.copy` and `sciexp2.data.copy`.
* Add `sciexp2.data.Data.ravel`.

.. rubric:: Bug fixes

.. rubric:: Documentation

.. rubric:: Internals

* Provide `sciexp2.data.Dimension.copy`.


0.15
----

.. rubric:: External compatibility breaks

* Remove `sciexp2.data.io.maybe` and `sciexp2.data.io.maybe_other` in favour of `~sciexp2.data.io.lazy`.
* Removed *sort* in `~sciexp2.data.Data.reshape` in favour of *order* using the same semantics as `~sciexp2.data.Data.sort`.

.. rubric:: New features

* Simpler lazy data extraction and management infrastructure with `~sciexp2.data.io.lazy`.
* Allow sorting data dimensions with `~sciexp2.data.Data.sort` (closes :issue:`198`).
* Added `~sciexp2.data.concatenate` (closes :issue:`193`).
* Added `~sciexp2.data.append` (closes :issue:`50`).
* Added `~sciexp2.data.Data.append_fields` (closes :issue:`215`).
* Added `~sciexp2.data.append_fields`, `~sciexp2.data.drop_fields`, `~sciexp2.data.rename_fields` and `~sciexp2.data.merge_arrays` (closes :issue:`215`).
* Added `~sciexp2.data.Data.transpose` (closes :issue:`204`).
* Added `~sciexp2.data.Data.flatten` and `~sciexp2.data.ravel`.
* Added `~sciexp2.data.delete`.
* Added support for multi-line regular expressions in `~sciexp2.data.io.extract_regex` (closes :issue:`206`).

.. rubric:: Improvements

* Detect argument changes in results produced by `~sciexp2.data.io.lazy` to force re-execution.
* Allow lists of filters as arguments to `~sciexp2.data.io.find_files`, and to all the extraction routines by extension (closes :issue:`209`).
* Allow data extraction routines to take a single input file (closes :issue:`210`).
* Properly handle immediate `promote` string in `~sciexp2.data.io.extract_txt` and `~sciexp2.data.io.extract_regex`.
* Support both `promote` and `count` in `~sciexp2.data.io.extract_txt` and `~sciexp2.data.io.extract_regex` (closes :issue:`203`).
* Allow passing some arguments in `~sciexp2.data.io.extract_txt` down to `~numpy.genfromtxt` (closes :issue:`211`).

.. rubric:: Bug fixes

* Make scripts generated by `~sciexp2.launchgen.Launchgen.launcher` executable.
* Ensure `~sciexp2.data.data_array` uses the appropriate dtype.
* Fix handling of `Ellipsis` in `~sciexp2.data` (closes :issue:`213`).
* Fix handling of `~sciexp2.data` indexing with multiple filters (closes :issue:`208`).
* Fix data extraction when all fields have the same type (closes :issue:`205` and :issue:`225`).
* Fix descriptor parsing in `~sciexp2.data.io.extract_txt` (closes :issue:`212` and :issue:`223`).

.. rubric:: Documentation

.. rubric:: Internals


0.14.2
------

.. rubric:: External compatibility breaks

.. rubric:: New features

.. rubric:: Improvements

.. rubric:: Bug fixes

* Fixed internal error in `~sciexp2.launchgen.Launchgen.execute`.

.. rubric:: Documentation

.. rubric:: Internals


0.14.1
------

.. rubric:: External compatibility breaks

.. rubric:: New features

.. rubric:: Improvements

.. rubric:: Bug fixes

* Fixed internal error in `~sciexp2.launchgen.Launchgen.find_files`.

.. rubric:: Documentation

.. rubric:: Internals


0.14
----

.. rubric:: External compatibility breaks

* Removed prefixed underscore from user-visible variables *LAUNCHER*, *DONE* and *FAIL* generated by `~sciexp2.launchgen.Launchgen` (closes :issue:`216`).
* Removed *done_expr* and *fail_expr* arguments to `~sciexp2.launchgen.Launchgen.launcher` in favour of variables *DONE* and *FAIL*, which have a default value (closes :issue:`217`).
* By default, `~sciexp2.launchgen.Launchgen.launcher` generates the job descriptor in file ``jobs.jd`` (controlled through variable *JD*).
* If specified, argument *export* in `~sciexp2.launchgen.Launchgen.launcher` overrides the variables that are exported by default.

.. rubric:: New features

* Method `~sciexp2.launchgen.Launchgen.execute` can now specify *stdin*, *stdout* and *stderr* (closes :issue:`168`).
* Program :program:`launcher` accepts the values (or the relative path to them, when interpreted as files) of certain variables (e.g., *DONE*) as a short-hand to filters (closes :issue:`182`).
* Method `~sciexp2.launchgen.Launchgen.launcher` accepts a list of variables that `~sciexp2.launchgen.launcher` will use to establish whether a job needs reexecution (closes :issue:`175`).
* Method `~sciexp2.launchgen.Launchgen.params` can also append new contents instead of recombining them with the existing ones (closes :issue:`202`).
* Function `~sciexp2.data.io.find_files` accepts job descriptor files as arguments.

.. rubric:: Improvements

* The user can now easily set when the *gridengine* template should send a mail notification (closes :issue:`126`).
* Properly handle *stdout* and *stderr* redirection in the *gridengine* and *shell* templates (closes :issue:`180`).
* Default templates can have separate values for files holding stdout/stderr (variables *STDOUT* and *STDERR*) and the *DONE* and *FAIL* files.
* Generating or copying files with `~sciexp2.launchgen.Launchgen` will only update these when new contents are available (closes :issue:`174`).

.. rubric:: Bug fixes

* Mark jobs as failed whenever the *_FAIL* file exists (closes :issue:`163`).
* Fix handling of job descriptor files in directories other than the output base.
* Fixed *gridengine* template to establish the base directory (closes :issue:`176`).

.. rubric:: Documentation

.. rubric:: Internals

* Method `~sciexp2.launchgen.Launchgen.launcher` only exports the appropriate variables.
* Method `~sciexp2.launchgen.Launchgen.launcher` makes job launcher scripts executable.
* Added `~sciexp2.common.utils.get_path` to handle path expansions (used in `~sciexp2.launchgen.Launchgen`).
* New implementation of the pretty-printing module `~sciexp2.common.pp` (adds IPython as a dependency).
* Store some metadata in job descriptor files to ensure their formatting.


0.13
----

.. rubric:: External compatibility breaks

* Variable `sciexp2.launchgen.Launchgen.DEFAULT_OUT` has been renamed to `~sciexp2.launchgen.Launchgen.OUTPUT_DIR`.

.. rubric:: New features

* Implemented the *modulus* operation in filters.
* Added *programmatic filters* to streamline the filter writing (see `~sciexp2.common.filter.PFilter`; relates to :issue:`185`).
* Instances of `~sciexp2.launchgen.Launchgen` can be constructed with initial contents (including copies of other instances).
* Method `~sciexp2.launchgen.Launchgen.generate` now accepts filters.
* Added method `~sciexp2.launchgen.Launchgen.select` to return an object that operates on a subset of the contents (closes :issue:`184` and :issue:`186`).

.. rubric:: Improvements

.. rubric:: Bug fixes

* All methods in `~sciexp2.launchgen.Launchgen` performing parameter recombination accept any iterable structure (closes :issue:`164`).

.. rubric:: Documentation

* Rewrote the user guide for launchgen, which is now more concise and tangible, as well as describes the latest features.

.. rubric:: Internals

* Have `~sciexp2.common.filter.Filter` accept a list of arguments.
* Have `~sciexp2.common.filter.Filter.match` silently fail when it contains a variable not present in the source if argument ``allow_unknown`` is set to ``True``.


0.12
----

.. rubric:: External compatibility breaks

* `~sciexp2.data.Dimension` no longer handles named groups if the `expression` argument is a regular expression, as version 0.11.2 removed the feature from the `~sciexp2.data.io` module.
* Removed function `sciexp2.data.build_dimension` and method `sciexp2.data.Dimension.build_instance` in favour of a saner `~sciexp2.data.Dimension` constructor and methods `~sciexp2.data.Dimension.add` and `~sciexp2.data.Dimension.extend`.

.. rubric:: New features

* Progress indicators now try to avoid updating the screen too often. Speed can be controlled through `sciexp2.common.progress.SPEED`.
* Whether to show progress indicators on the screen can be globally controlled through `sciexp2.common.progress.SHOW`.
* Add support for `sciexp2.data.Data.reshape` to sort axes according to their variables.

.. rubric:: Improvements

* Improvement of orders of magnitude on the speed of creation of new `~sciexp2.data.Data` objects (thanks to optimized `~sciexp2.data.Dimension` construction).
* Improvement of orders of magnitude on the speed of `~sciexp2.data.Data.reshape` (thanks to optimized `~sciexp2.data.Dimension` construction and improved algorithm).
* Better progress indication in `~sciexp2.data.Data.reshape` and  `~sciexp2.data.Data` slicing.

.. rubric:: Bug fixes

* Fix sorting of results for file-finding routines.

.. rubric:: Documentation

* Reference documentation no longer shows class hierarchies.

.. rubric:: Internals

* Refactored progress indicators into the `~sciexp2.common.progress` module.
* Use context manager protocol with `~sciexp2.common.progress.Counter` and `~sciexp2.common.progress.Spinner`.
* Progress indicator type (counter or spinner) can be automatically selected through `sciexp2.common.progress.get` and `sciexp2.common.progress.get_pickle`.
* Split `~sciexp2.common.instance.InstanceGroup` caching into  `~sciexp2.common.instance.InstanceGroup.cache_get` and  `~sciexp2.common.instance.InstanceGroup.cache_set`.
* Added proactive and zero-caching instance additions in `~sciexp2.common.instance.InstanceGroup`.
* Small performance improvements on various operations of the `~sciexp2.common.instance` module.
* Move `sciexp2.common.instance.Expander.Result` into `~sciexp2.common.instance.ExpanderResult`.
* Added `~sciexp2.common.progress.progressable` as a means to add progress indication in routines that where oblivious to it (e.g., adding it to an instance group to get progress indication when used with an expander).
* Huge speedup in `~sciexp2.common.instance.InstanceGroup.sort` by using Python's :func:`sorted` routine.
* Add support for progress indicators in `~sciexp2.common.instance.InstanceGroup.sort`.


0.11.2
------

.. rubric:: External compatibility breaks

* Extraction routines in `~sciexp2.data.io` do not retain the complete source expression as the dimension expression (now it just contains the variables).

.. rubric:: New features

.. rubric:: Improvements

* Extraction routines in `~sciexp2.data.io` ignore empty files by default.

* Added `~sciexp2.common.varref.expr_to_regexp` to handle expression-to-regexp conversions in a single place.

* Added `~sciexp2.common.varref.expr_get_vars` and `~sciexp2.common.varref.regexp_get_names` to handle variable/group name extraction in a single place (closes :issue:`195`).

* Failed translations show the offending substitution (closes :issue:`188`).

.. rubric:: Bug fixes

.. rubric:: Documentation


0.11.1
------

.. rubric:: External compatibility breaks

.. rubric:: New features

* Added "pattern binding" operators to `~sciexp2.common.filter.Filter`, so that filters can express matches with regular expressions.

.. rubric:: Improvements

* Ensure that `~sciexp2.data.io.maybe` and `~sciexp2.data.io.maybe_other` applied to extraction routines preserve the path used to find files as the dimension expression.

* Properly handle `~numpy.ndarray.argmax` and `~numpy.ndarray.argmin` reductions.

* Properly handle `~numpy.ndarray.cumsum` and `~numpy.ndarray.cumprod` accumulations.

.. rubric:: Bug fixes

* Handle indexing of `~sciexp2.data.Data` objects with boolean arrays.

* Properly handle the `axis` argument in reductions when not explicitly named.

* Properly translate named regular expression groups into variable references in dimension expressions. Integrates with complex path expressions given to extraction routines as an implicit argument to `~sciexp2.data.io.find_files`.

.. rubric:: Documentation


0.11
----

.. rubric:: External compatibility breaks

* Removed top-level scripts ``launchgen`` and ``plotter`` (closes :issue:`119`).

  Script ``launcher`` now is able to show the list and contents of templates (instead of the now removed ``launchgen``).

  The old functionality of injecting a default instance and its methods is now available (and documented) in the `sciexp2.launchgen.env` module.

* Removed module ``sciexp2.common.cmdline``.

  Was used by the top-level scripts, of which only one is present now.

* Removed modules ``sciexp2.common.config`` and ``sciexp2.common.doc`` (closes :issue:`118`).

  Was used by the ``--describe`` argument of top-level scripts, which no longer exists.

* Removed ``sciexp2.common.utils.check_module``.

  All checks are already performed by the requirements stated in the ``setup.py`` script.

.. rubric:: New features

* Added initial unit-testing framework. Can be run with ``python ./setup test``. See ``python ./setup test --help`` for additional arguments.

* Added module `sciexp2.data.env` to quickly import all relevant functions and classes.

.. rubric:: Improvements

* Depend on Python 2.7 or later (closes :issue:`43`).

  This implies that ``sciexp2.common.utils.OrderedDict`` has been removed in favour of Python's `~collections.OrderedDict`, and :program:`launcher` now uses `argparse` instead of `optparse`.

.. rubric:: Bug fixes

.. rubric:: Documentation

* Showing the contents of a template now lists the variables that must be forcefully defined by the user.

* Properly document how to install and run using "virtualenv" and "pip" (closes :issue:`178`).


0.10
----

.. rubric:: External compatibility breaks

* Moved data extraction methods in ``sciexp2.data.io.RawData`` into routines in `sciexp2.data.io` (`~sciexp2.data.io.extract_txt` and `~sciexp2.data.io.extract_regex`).

* Re-implemented data extraction routines (`~sciexp2.data.io.extract_txt` and `~sciexp2.data.io.extract_regex`) to provide a saner, simpler and more unified interface (closes :issue:`103`).

* Removed the bit-rotten "valuename" implementation from the `~sciexp2.data.Data` object, which also helps decreasing the number of concepts (closes :issue:`192`).

* Removed ``sciexp2.data.load`` and ``sciexp2.data.io.extract_maybe`` in favour of `~sciexp2.data.io.maybe` and `~sciexp2.data.io.maybe_other`.

* Removed bit-rotten module ``sciexp2.data.save``.

* Remove ``sciexp2.data.io.Source`` in favour of `~sciexp2.data.io.find_files`.

  All data extraction utilities in `sciexp2.data.io` can now accept either an `~sciexp2.common.instance.InstanceGroup` (resulting from a call to `~sciexp2.data.io.find_files`), a tuple with the arguments for `~sciexp2.data.io.find_files` or simply the file expression (thus without filters) as the first argument for `~sciexp2.data.io.find_files`.

* Remove ``sciexp2.data.io.RawData`` and ``sciexp2.data.Data.from_rawdata`` in favour of extraction routines that directly return a `~sciexp2.data.Data` object (closes :issue:`122`).

.. rubric:: New features

* Instances of `~sciexp2.data.Data` can be built directly by the user (see `~sciexp2.data.Data` and `~sciexp2.data.data_array`; closes :issue:`51` and :issue:`65`).

* Added `~sciexp2.data.io.maybe` and `~sciexp2.data.io.maybe_other` to simplify the process of caching the initial extraction and transformation of data (closes :issue:`177`).

.. rubric:: Improvements

* Data extraction routines can also work with file-like objects (aside from open existing files).

* Routine `~sciexp2.data.io.extract_regex` can now perform multiple extracts per file.

* Routine `~sciexp2.data.Data.reshape` now lets the user specify per-field filling values for newly-generated entries (closes :issue:`55`).

.. rubric:: Bug fixes

.. rubric:: Documentation


0.9.7
-----

.. rubric:: External compatibility breaks

.. rubric:: New features

* Added the possibility to filter which files to process with `~sciexp2.launchgen.Launchgen.pack`.

.. rubric:: Improvements

.. rubric:: Bug fixes

* Fix a strange bug where `~sciexp2.launchgen.Launchgen.find_files` returned no results even though there were files to be found.

.. rubric:: Documentation


0.9.6
-----

.. rubric:: External compatibility breaks

.. rubric:: New features

.. rubric:: Improvements

* Return a `~sciexp2.data.Data` object when slicing with numpy-derived arrays.

.. rubric:: Bug fixes

* Allow superclasses when specifying indexing methods with `sciexp2.data.with_dim_index` (closes :issue:`92`).
* Allow superclasses when specifying indexing methods with `sciexp2.data.with_new_dim_index`.
* Return a `~sciexp2.data.Data` object with the appropriate metadata when using reduction-like numpy routines; if the result has no meaning as a `~sciexp2.data.Data` object, a :class:`numpy.ndarray` is returned instead.
* Fix import path to ipython's :mod:`IPython.core.ultratb` module.
* Fix a couple of typos in variable names when building `~sciexp2.data.Dimension` objects.

.. rubric:: Documentation

* The :ref:`todo` is temporarily disabled due to a bug in `Sphinx <http://sphinx.pocoo.org>`_.

.. rubric:: Improvements

.. rubric:: Bug fixes


0.9.5
-----

.. rubric:: External compatibility breaks

.. rubric:: New features

.. rubric:: Improvements

* Move common initialization code to abstract `~sciexp2.system.Job` class.
* Only try to kill jobs in `~sciexp2.launcher.Launcher` if they're in the running state.

.. rubric:: Bug fixes

* Do not use `sciexp2.system.Job.state` to query job state in generic machinery, but use the "_STATE" variable instead.
* Rename abstract `sciexp2.system.Job.status` into `sciexp2.system.Job.state` (closes :issue:`125`).
* Fix cleanup of progress indication stack when (un)pickling contents with progress indication.

.. rubric:: Documentation


0.9.4
-----

.. rubric:: External compatibility breaks

.. rubric:: New features

.. rubric:: Improvements

* Improve memory usage during `~sciexp2.data.Data.from_rawdata` when using extremely large inputs (closes :issue:`66`).
* Improve speed of `~sciexp2.common.instance.InstaceGroup.select` (closes :issue:`63`). This results in improved speeds during `~sciexp2.data.Data.reshape`.
* Use a plain :class:`dict` during reverse lookup in `~sciexp2.common.instance.InstaceGroup` (closes :issue:`120`). This was unnecessary and a :class:`dict` might yield faster lookups.
* Show a clearer error message when a filter contains unknown variable names during `~sciexp2.common.filter.Filter.match` (closes :issue:`123`).

.. rubric:: Bug fixes

* Allow calls to `sciexp2.launchgen.Launchgen.generate` without any extra values.
* Generate source distribution with description and template data files for launchgen.

.. rubric:: Documentation

* Rewrite the user guide for :ref:`launchgen` and :ref:`launcher` for much more clarity and extensive examples.


0.9.3
-----

.. rubric:: External compatibility breaks

* Deleted variables ``QUEUE_CMD`` and ``STDINDIR`` in launcher's `gridengine` template.
* Job descriptor files for :program:`launcher` use the ``.jd`` suffix instead of ``.dsc``.

.. rubric:: New features

* Added variable ``QSUB_OPTS`` in launcher's `gridengine` template.
* Templates can provide their own default values (see ``launchgen -T templatename``).

.. rubric:: Improvements

* When finding files, the same variable can appear more than once (e.g., ``@v1@-foo-@v2@-bar-@v1@``).
* More robust and faster file finding, including finding files using expressions without variable references.

.. rubric:: Bug fixes

.. rubric:: Documentation

* Add some user-oriented summaries on the launcher template headers.


0.9.2
-----

.. rubric:: External compatibility breaks

* Removed `selector` argument in `sciexp2.launchgen.Launchgen.params`.

.. rubric:: New features

* Let the user tinker with the `~sciexp2.templates.SEARCH_PATH` of launchgen templates.
* Let the user tinker with the `~sciexp2.system.SEARCH_PATH` of execution systems.

.. rubric:: Improvements

.. rubric:: Bug fixes

.. rubric:: Documentation

* User guide for :program:`launchgen`.
* User guide for :program:`launcher`.
* Auto-generated API documentation.
