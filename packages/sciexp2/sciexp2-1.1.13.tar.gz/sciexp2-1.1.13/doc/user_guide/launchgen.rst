.. _launchgen:

Experiment creation --- `~sciexp2.launchgen`
============================================

The goal of the `~sciexp2.launchgen` module is to define a set of experiments and create a self-contained directory with all the files necessary for running these experiments. The reason to make it self-contained is that this directory can then be moved into the system(s) where the experiments must be run (e.g., a cluster, or some other machine different from the development one).

For the sake of making the description more tangible, this guide will show how to generate experiments to evaluate all benchmarks on a simple benchmark suite (``mybenchsuite``), where each benchmark is run with different input sets inside a computer simulator program (``mysim``) that uses different configuration parameters (specified in a configuration file). Thus, each experiment will be defined by the tuple comprised of the benchmark name, the benchmark's input set, and the different configuration parameter permutations defined by the user. The initial file organization is the following::

  .
  |- generate.py       # the experiment-generation script described here
  |- mysimulator       # source code for the simulator
  |  |- Makefile
  |  `- mysim.c
  |- mysim.cfg.in      # template configuration file for the simulator
  `- mybenchsuite      # benchmark suite
     |- 1.foo          # source code for a specific benchmark
     |  |- source.c
     |  `- Makefile
     |- 2.broken
     |  |- source.c
     |  `- Makefile
     |- 3.baz
     |  |- source.c
     |  `- Makefile
     |- README         # files that can be ignored
     `- NEWS

This is the roadmap to create an ``experiments`` directory that will contain all the necessary pieces to run our experiments:

#. Execute external programs to compile the simulator and the benchmarks.

#. Copy files for the simulator and each of the selected benchmarks into the ``experiments`` directory.

#. Define different sets of arguments to run the benchmarks with different inputs.

#. Define different configuration parameter combinations for the simulator.

#. Generate a simulator configuration file for each set of simulation parameters, and generate a script for each combination of simulator parameters, benchmark and benchmark input sets. These files are generated from templates by :term:`translating <translation>` any :term:`variable` they reference in their contents with the values specified by us.

This example also showcases some of the more advanced features of `~sciexp2.launchgen`, but you can first take a look at :ref:`quick_example` for a much shorter and simpler example.


Script preparation
------------------

All the functions typically used in a `~sciexp2.launchgen` script are available in the `sciexp2.launchgen.env` module, so we can import its contents to make them available at the top level::

  #!/usr/bin/env python
  # -*- python -*-

  from sciexp2.launchgen.env import *

  # file contents ...


Directory preparation
---------------------

First, we create a `~sciexp2.launchgen.Launchgen` object with its output directory set, where all generated files will be placed::

  l = Launchgen(out="./experiments")

This object is initially empty, and only has the output directory set::

  >>> l
  Launchgen(out='./experiments')

.. note::

   It is usually recommended to *not* remove the output directory when re-executing a `~sciexp2.launchgen` script, since methods `~sciexp2.launchgen.Launchgen.pack`,  `~sciexp2.launchgen.Launchgen.generate` and  `~sciexp2.launchgen.Launchgen.launcher` (see below) already take care of overwriting destination files only if their contents are outdated. Furthermore, the :ref:`launcher <launcher>` program is able to re-run only those experiments whose scripts or configuration files have been updated (e.g., generated with new contents since last run).


Compile and copy the simulator
------------------------------

As there is only one simulator, we can use `~sciexp2.launchgen.Launchgen.execute` right away to execute ``make`` from the current directory, and then use `~sciexp2.launchgen.Launchgen.pack` to copy the resulting binary into the output ``experiments`` directory::

  l.execute("make", "-C", "./mysimulator")
  # copied into 'experiments/bin/mysim'
  l.pack("./mysimulator/mysim", "bin/mysim")


Find, compile and copy benchmarks
---------------------------------

Hard-coding the list of benchmarks is not desirable, so it is much better to dynamically detect them with `~sciexp2.launchgen.Launchgen.find_files` (unsurprisingly, it finds both files and directories)::

  l.find_files("./mybenchsuite/[0-9]*\.@benchmark@/",
               v_.benchmark != 'broken')

The first argument is an :term:`expression` to find all benchmark directories, which accepts both Python's regular expressions and SciExp²'s expressions with variable references at the same time. The following is an argument list with :term:`filters <filter>` (in this case with a single element) to narrow which of these directories we're interested in. In this case, we want to omit the benchmark directory *2.broken*, since we know it's broken, but we're eager to run all the rest before fixing it. Note that the filter uses the special variable `v_` (provided by `sciexp2.launchgen.env`), but we could have instead used a plain string to specify the same filter: ``"benchmark != 'broken'"``. Note also the trailing slash in the expression, which prevents matching the ``README`` and ``NEWS`` files under the ``mybenchsuite`` directory.

The result is that our `~sciexp2.launchgen.Launchgen` object now contains one element (an :term:`instance`) for each directory that matches the :term:`expression` in `~sciexp2.launchgen.Launchgen.find_files`, and each element contains the :term:`variable <variable>` specified in that expression, plus an additional ``FILE`` variable that contains the full path of what we've found. In the terms used by SciExp², each instance is :term:`extracted <extraction>` from the given :term:`expression` by using the found paths::

  >>> l
  Launchgen([Instance({'benchmark': 'foo', 'FILE': './mybenchsuite/1.foo/'}),
             Instance({'benchmark': 'baz', 'FILE': './mybenchsuite/3.baz/'})],
            out='./experiments')

Then, we call ``make`` into each of the selected benchmark directories, and copy the resulting binaries into the output directory::

  # results in executing the following commands:
  #   make -C ./mybenchsuite/1.foo/
  #   make -C ./mybenchsuite/3.baz/
  l.execute("make", "-C", "@FILE@")

  # results in the following copies:
  #   ./mybenchsuite/1.foo/foo -> ./experiments/benchmarks/foo
  #   ./mybenchsuite/3.baz/baz -> ./experiments/benchmarks/baz
  l.pack("@FILE@/@benchmark@", "benchmarks/@benchmark@")

Both command execution and file copying use :term:`expressions <expression>`, which are :term:`expanded <expansion>` for each of the :term:`instances <instance>` in the `~sciexp2.launchgen.Launchen` object. This results in executing ``make`` on each of the benchmark directories (since the command only references the ``@FILE@`` variable), and copying each of the per-benchmark binaries we just compiled.


.. note::

   Higher level methods based on `~sciexp2.launchgen.Launchgen.find_files` are available for finding and parsing specific contents (e.g., `SPEC <http://www.spec.org>`_ benchmarks or `SimPoint <http://cseweb.ucsd.edu/~calder/simpoint/>`_ results). See `~sciexp2.launchgen.Launchgen` for details.


Define experiment parameters
----------------------------

Defining the experiment parameters is one of the heavy-weight operations, which is encapsulated in `~sciexp2.launchgen.Launchgen.params`. First of all, we want each benchmark to execute with different arguments, which are benchmark specific.

Let's start with the simpler ``foo`` benchmark, which has two possible input values (``small`` or ``big``). For that, we use `~sciexp2.launchgen.Launchgen.select` to get the sub-set of instances for that benchmark, and define their ``inputset`` and ``args`` parameter by applying `~sciexp2.launchgen.Launchgen.params` on that sub-set::

  with l.select(v_.benchmark == 'foo') as s:
      s.params(inputset="@args@",
               args=["small", "big"])

If we look at the `~sciexp2.launchgen.Launchgen` object, it now has the variables defined by `~sciexp2.launchgen.Launchgen.params` only on the sub-set of instances we got from `~sciexp2.launchgen.Launchgen.select`::

  >>> l
  Launchgen([Instance({'benchmark': 'foo', 'inputset': 'small', 'args': 'small', 'FILE': './mybenchsuite/1.foo/'}),
             Instance({'benchmark': 'foo', 'inputset': 'big', 'args': 'big', 'FILE': './mybenchsuite/1.foo/'}),
             Instance({'benchmark': 'baz', 'FILE': './mybenchsuite/3.baz/'})],
            out='./experiments')

The ``baz`` benchmark example is a bit more involved, since it has three input arguments (``arg1``, ``arg2`` and ``arg3``). The first two take any value in the 2-element range starting at zero, and the third takes the base-two logarithm of the sum of the first two arguments::

  import math
  with l.select(v_.benchmark == 'baz') as s:
      s.params((v_.arg1 != 0) | (v_.arg2 != 0),
               inputset="@arg1@@arg2@",
               args="@arg1@ @arg2@ @arg3@",
               arg1=range(2),
               arg2=range(2),
               arg3=defer(math.log, defer("arg1") + defer("arg2"), 2))

In this case, we define the argument list that we will later use to run the benchmark as a string with the benchmark arguments (``args``). Since we must define the value of the third argument as a function of the first two, we have to `~sciexp2.launchgen.defer` its calculation until we know ``arg1`` and ``arg2``. The outer call will `~sciexp2.launchgen.defer` the execution of the `math.log` function until all the values passed as arguments to it are known; in turn, these deferred arguments must be identified with calls to `~sciexp2.launchgen.defer`, passing the deferred variable name as an argument. If we apply any operator or function call on deferred results, the result will in turn be a value deferred until all the variables it depends on are known (i.e., ``defer("arg1") + defer("arg2")``). Note that in this case, `~sciexp2.launchgen.Launchgen.params` also has a filter to avoid having the first two arguments both at zero, since the logarithm is infinite.

Now, the `~sciexp2.launchgen.Launchgen` object would look like this::

  >>> l
  Launchgen([Instance({'benchmark': 'foo', 'inputset': 'small', 'args': 'small', 'FILE': './mybenchsuite/1.foo/'}),
             Instance({'benchmark': 'foo', 'inputset': 'big', 'args': 'big', 'FILE': './mybenchsuite/1.foo/'}),
             Instance({'benchmark': 'baz', 'inputset': '01', 'args': '0 1 0.0', 'arg1': '0', 'arg2': '1', 'arg2': '0.0', 'FILE': './mybenchsuite/3.baz/'}),
             Instance({'benchmark': 'baz', 'inputset': '10', 'args': '1 0 0.0', 'arg1': '1', 'arg2': '0', 'arg2': '0.0', 'FILE': './mybenchsuite/3.baz/'}),
             Instance({'benchmark': 'baz', 'inputset': '11', 'args': '1 1 1.0', 'arg1': '1', 'arg2': '1', 'arg3': '1.0', 'FILE': './mybenchsuite/3.baz/'})],
            out='./experiments')


In both cases, we also generate the ``inputset`` variable, which will help us to uniquely identify each of the benchmark's input sets. Note that in most benchmark suites, the different input sets have a unique name or number assigned to each benchmark, and we could use that instead of building our own unique identifier value.


Finally, we also need to define the parameters we will use with our computer simulator (variables ``cores``, ``l1``, ``l2``, ``l1_assoc`` and ``l2_assoc``), together with filtering-out some configurations that the simulator does not support. Again, this will take each of the benchmark configurations and "extend" each of them with each of the simulator parameter combinations.::

  l.params(v_.l1 <= v_.l2,
           v_.l1_assoc <= v_.l2_assoc,
           cores=range(1, 5),
           l1=[2**x for x in range(1,  6)], # size in KB
           l2=[2**x for x in range(1, 10)],
           l1_assoc=[1, 2, 4],
           l2_assoc=[1, 2, 4, 8])


.. note::

   Using Python's ``with`` statement with `~sciexp2.launchgen.Launchgen.select` is not mandatory, but can improve code readability in these cases. The canonical way to use it instead would be to treat its result as a regular object::

     s = l.select(...)
     s.params(...)


.. warning::

   The `filter <sciexp2.common.filter.PFilter>` used in the example above is implemented by overloading certain operations. As the logical *and* and logical *or* cannot be overloaded, it uses the bit-wise *and* and bit-wise *or* instead, which have a different operator precedence; thus parentheses must be used to evaluate the expression in the proper order.

More generally, `~sciexp2.launchgen.Launchgen.params` accepts any of the following value type (right-hand-side) for any of the specified variables (left-hand-side):

- *Immediate values*: Can be strings or anything that does not fit the following two categories. In the case of strings, they are treated as :term:`expressions <expression>`, which are :term:`translated <translation>` with the variable values of each :term:`instance`.

- *Value sequences*: Anything that can be iterated and is not a string (e.g., `range`, lists, etc.). If the values in a sequence are strings, they are treated as described above.

- *The* `~sciexp2.launchgen.defer` *function*: An alternative to using strings with variable references when the literal value is necessary for later operating with it.

As a result, the contents of the `~sciexp2.launchgen.Launchgen` object will contain the *cartesian product* of the original contents and the permutations of the newly defined parameters. If this is not desired, you can use different `~sciexp2.launchgen.Launchgen` objects, or can pass the ``append=True`` argument to append new entries instead of recombining them with the existing contents.


Generate simulator configuration files
--------------------------------------

The contents of a `~sciexp2.launchgen.Launchgen` can be used to generate files from an input template, by substituting variable references with the specific values on each instance. In this example, we have a template simulator configuration file in ``mysim.cfg.in`` with the following contents::

  cores = @cores@
  l1_size  = @l1@         # Bytes
  l1_assoc = @l1_assoc@
  l2_size  = @l2@         # Bytes
  l2_assoc = @l2_assoc@

With `~sciexp2.launchgen.Launchgen.generate`, we can create a new configuration file from our template (``"conf/@cores@-@l1@-@l1_assoc@-@l2@-@l2_assoc@.cfg"``) for each parameter combination we defined above::

  l.generate("mysim.cfg.in", "conf/@cores@-@l1@-@l1_assoc@-@l2@-@l2_assoc@.cfg",
             # convert from KB into B
             l1=defer("l1") * 1024,
             l2=defer("l2") * 1024)

What `~sciexp2.launchgen.Launchgen.generate` does is, for each possible expansion of the second argument (which is an expression), take the file in the first argument (which could also be an expression), and use the instance corresponding to that expansion to :term:`translate <translation>` the file contents (the input file is, in fact, treated as a string whose contents are then translated).

Note that the configuration file expects ``@l1@`` and ``@l2@`` to be defined in Bytes, while we defined our parameters in KBytes. For that, we can use `~sciexp2.launchgen.Launchgen.generate` to also perform parameter recombination like `~sciexp2.launchgen.Launchgen.params`, so that we can "translate" the values for ``l1`` and ``l2`` "in-place". We could acoomplish the same by first invoking `~sciexp2.launchgen.Launchgen.params` and then `~sciexp2.launchgen.Launchgen.generate` (without any parameter arguments); the difference is that the parameter recombinations in `~sciexp2.launchgen.Launchgen.generate` will not modify the contents of our `~sciexp2.launchgen.Launchgen` object. This can be helpful to keep the parameters "clean" of intermediate variables and values by only defining them during the generation of specific files.

.. warning ::

   For each possible simulation parameter combination, there exist multiple benchmark/argument combinations. That is, there are multiple instances in the contents that expand to the output file expression. When such things happen, the output file will only be generated once with the first instance expanding to that expression, and subsequent instances will simply show the message "*Skipping already generated file*".


Generate an execution script for each experiment
------------------------------------------------

The final step is to generate some scripts to actually run our experiments with all the selected benchmark, inputs and simulation parameter combinations. We could simply use `~sciexp2.launchgen.Launchgen.generate`, but `~sciexp2.launchgen.Launchgen.launcher` is an extension of it that already has some pre-defined templates, and produces some extra metadata to manage experiment execution with the :program:`launcher` program. We first have to decide which pre-defined template to use; all of them can be seen with :program:`launcher` :option:`--list-templates`. With that, we can now use :program:`launcher` :option:`--show-template` to inspect the template and see what variables we need to define for it to work.

In this example we will use the ``shell`` template. Looking at the output of ``launcher --show-template shell`` we can see that we only need to defined the ``CMD`` variable, which contains the actual command-line that will execute our experiment. Therefore, this will produce our experiment scripts::

  l.launcher("shell", "jobs/@ID@.sh",
             # save some typing by defining these once and for all
             ID="@benchmark@-@inputset@-@SIMID@",
             SIMID="@cores@-@l1@-@l1_assoc@-@l2@-@l2_assoc@",

             DONE="res/@ID@.done",
             FAIL="res/@ID@.fail",

             CMD="""
  # Python multi-line strings are handy to write commands in multiple lines
  ./bin/mysim -config conf/@SIMID@.cfg -output @DONE@ -bench ./benchmarks/@benchmark@ @args@
  """)

The first two arguments are almost the same as in `~sciexp2.launchgen.Launchgen.generate`; selecting the pre-defined template to use and specifying the output file. The rest either define variables used by the template (``CMD``, ``DONE`` and ``FAIL``) or additional variables used by the former ones (``ID`` and ``SIMID``, which are used to save some typing).

The ``CMD`` variable contains the command-line to run the simulator with the specified configuration file, as well as a specific benchmark along with its arguments. It also instructs the simulator to save its output in the value of the ``DONE`` variable. Note ``DONE`` and ``FAIL`` are used by the shell template, but have default values that we are overriding for clarity.

Finally, this also generates the file ``jobs.jd`` in the output directory. The :program:`launcher` program will use this file to detect the available experiments, and will use the values of the ``DONE`` and ``FAIL`` variables to known which experiments have already been run and, if so, which of these failed.

.. note::

   You should also take a look at `~sciexp2.launchgen.Launchgen.launcher`'s ``export`` argument, which will make the variables listed in it available to the :program:`launcher` program, so that you can, for example, run sub-sets of your experiments depending on their configuration parameters.

   Argument ``DEPENDS`` is also handy to know when an experiment is outdated and needs re-execution; for example, the compiled simulator or one benchmark binary is newer that the result of its last execution. Coupled with the behaviour of the file-copying and file-generation methods, `~sciexp2.launcher` will always keep track of what experiments get out-of-date.


Writing new templates
---------------------

Sometimes using some of the pre-defined templates is not enough, but the program :program:`launcher` is still very handy to keep track of the state of our experiments. You can override the contents of an existing template by creating a file with the same name as the template (e.g., for the previous example, create ``shell.tpl`` in the same directory where you have ``generate.py``).

For even greater flexibility, you can also extend the set of available templates by creating the appropriate files, which can reside in any of the directories listed in `~sciexp2.templates.SEARCH_PATH`, which by default includes the current directory.

.. seealso:: `sciexp2.templates`


Wrap-up
-------

To wrap things up, here's the contents of the ``generate.py`` file covering the whole example::

  #!/usr/bin/env python
  # -*- python -*-

  import math

  from sciexp2.launchgen.env import *

  l = Launchgen(out="./experiments")

  # compile & copy simulator
  l.execute("make", "-C", "./mysimulator")
  l.pack("./mysimulator/mysim", "bin/mysim")

  # find & compile & copy benchmarks
  l.find_files("./mybenchsuite/[0-9]*\.@benchmark@/",
               v_.benchmark != 'broken')
  l.execute("make", "-C", "@FILE@")
  l.pack("@FILE@/@benchmark@", "benchmarks/@benchmark@")


  # benchmark arguments
  with l.select(v_.benchmark == 'foo') as s:
      s.params(inputset="@args@",
               args=["small", "big"])
  with l.select(v_.benchmark == 'baz') as s:
      s.params((v_.arg1 != 0) | (v_.arg2 != 0),
               inputset="@arg1@@arg2@",
               args="@arg1@ @arg2@ @arg3@",
               arg1=range(2),
               arg2=range(2),
               arg3=defer(math.log, defer("arg1") + defer("arg2"), 2))

  # simulation parameters
  l.params(v_.l1 <= v_.l2,
           v_.l1_assoc <= v_.l2_assoc,
           cores=range(1, 5),
           l1=[2**x for x in range(1,  6)], # size in KB
           l2=[2**x for x in range(1, 10)],
           l1_assoc=[1, 2, 4],
           l2_assoc=[1, 2, 4, 8])

  # simulator config file
  l.generate("mysim.cfg.in", "conf/@cores@-@l1@-@l1_assoc@-@l2@-@l2_assoc@.cfg",
             # convert from KB into B
             l1=defer("l1") * 1024,
             l2=defer("l2") * 1024)

  # generate execution scripts
  l.launcher("shell", "jobs/@ID@.sh",
             # save some typing by defining these once and for all
             ID="@benchmark@-@inputset@-@SIMID@",
             SIMID="@cores@-@l1@-@l1_assoc@-@l2@-@l2_assoc@",

             DONE="res/@ID@.done",
             FAIL="res/@ID@.fail",

             CMD="""
  # Python multi-line strings are handy to write commands in multiple lines
  ./bin/mysim -config conf/@SIMID@.cfg -output @DONE@ -bench ./benchmarks/@benchmark@ @args@
  """)

Although this might look unnecessarily long, `~sciexp2.launchgen.Launchgen`'s ability to concisely specify parameter permutations and apply filters on them can keep large parameter explorations under control. If you couple that with the ability to track the execution state of experiments with the :program:`launcher` program, that becomes even more convenient.
