Installing
==========

It is recommended you install SciExp² either as a system package or in the home directory (as a PyPi package).


From a Debian package
~~~~~~~~~~~~~~~~~~~~~

First, make sure you have package *apt-transport-https* installed::

  sudo apt-get install apt-transport-https

Then you can add the provided repository and install the packages::

  sudo sh -c 'echo "deb https://people.gso.ac.upc.edu/vilanova/packages/sciexp2/debian/ unstable main" > /etc/apt/sources.list.d/sciexp2.list'
  sudo apt-get update
  sudo apt-get install python-sciexp2 python-sciexp2-doc


From the Python Package Index (PyPi)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is the simplest system-agnostic way to use SciExp², using the official Python Package Index (https://pypi.python.org).

1. Install :program:`virtualenv` and :program:`pip` [#virtualenv]_.
2. Create a python package "environment"::

    virtualenv --system-site-packages ~/my-sciexp2

  You can create as many as you want; e.g., one for each different version of the SciExp² package that you want to test.

  If you want to ignore the python packages installed on the system, you can instead run::

    virtualenv ~/my-sciexp2

3. Install SciExp²::

     . ~/my-sciexp2/bin/activate
     pip install sciexp2

   Or to install a specific version (version ``0.0.0`` in the example)::

     . ~/my-sciexp2/bin/activate
     pip install "sciexp2==0.0.0"

.. [#virtualenv] http://www.pip-installer.org/en/latest/installing.html


From a source checkout
~~~~~~~~~~~~~~~~~~~~~~

You can also use a copy of the upstream repositories [#repos]_. By default it will use the latest stable version, but you can feel the thrill of using the latest and greatest development version by getting a checkout of the ``develop`` branch.

To install a checkout (of the stable branch), you can::

  git clone https://code.gso.ac.upc.edu/git/sciexp2
  cd sciexp2
  python ./setup.py sdist

  virtualenv --system-site-packages ~/my-sciexp2
  . ~/my-sciexp2/bin/activate
  pip install dist/sciexp2-some_version.tar.gz

.. [#repos]  https://projects.gso.ac.upc.edu/projects/sciexp2/repository


Running
=======

If you have installed SciExp² using :program:`pip`, just remember to activate your environment before using it::

  . ~/my-sciexp2/bin/activate
  # programs and paths are now properly set up

If you want to run a source checkout without installing it, set you `PYTHONPATH <http://docs.python.org/2/using/cmdline.html#envvar-PYTHONPATH>`_ to point to the directory that contains your copy of SciExp²::

  git clone https://code.gso.ac.upc.edu/git/sciexp2 ~/sciexp2
  PYTHONPATH=~/sciexp2 /path/to/my/script.py

.. note::

   Many potentially long operations provide a feedback in the form of progress indicators; you can control whether they are shown through `sciexp2.common.progress.level`.


Interactive execution
~~~~~~~~~~~~~~~~~~~~~

You can use SciExp² in an interactive python shell, but it is recommended to use the nicer interactive `Jupyter <http://jupyter.org>`_ interface instead (formerly the `IPython <http://ipython.org>`_ project). You can execute it in the command line (``jupyter-console``), as a graphical application (``jupyter-qtconsole``) or as a browser page (``jupyter-notebook``; it allows you to run the code in one machine, while the browser to edit it is in another machine).

All three interfaces provide dynamic object information [#info]_ and help visualizing error back-traces. In addition, the last two can show you data plots in-line (for your interactive data analysis needs),

.. [#info] http://ipython.org/ipython-doc/stable/interactive/reference.html#dynamic-object-information


Automated execution
~~~~~~~~~~~~~~~~~~~

It is highly recommended to have a local SciExp² installation of a specific version for each of your projects. This will make sure your scripts always use the same SciExp² version to avoid any possible future version incompatibilities.

In case you are using :program:`make` to automate the execution of your scripts, here is a simple snippet you can add to your ``Makefile`` (the example pins SciExp² to version ``0.0.0``)::

  all: deps/sciexp2
        # run our script using sciexp2
  	( . deps/sciexp2/bin/activate && /path/to/my/script.py )

  # install sciexp2 as a dependency
  # the ".done" file ensures a partial installation will not count as a success
  deps/sciexp2: deps/sciexp2/.done
  	$(RM) -R $@
        mkdir -p $(dir $@)
  	virtualenv --system-site-packages $@
  	( . $@/bin/activate && pip install "sciexp2==0.0.0" )
  	touch $<


Debugging aids
~~~~~~~~~~~~~~

You can start your scripts with ``ipython --pdb /path/to/my/script.py`` to get into a debugging shell whenever an error occurs [#pdb]_.

Sometimes it is also useful to start an IPython shell [#embed]_ somewhere deep in your code to interactively evaluate its current state::

  from IPython import embed
  embed()

Exiting the debugging shell will returning to normal execution.

.. [#pdb] http://ipython.org/ipython-doc/stable/interactive/reference.html#post-mortem-debugging
.. [#embed] http://ipython.org/ipython-doc/stable/interactive/reference.html#embedding-ipython
