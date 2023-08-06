Basic concepts
==============

The SciExp² framework uses a few concepts across the whole documentation, which are defined here.


Python and Numpy constructs
---------------------------

* `Default argument values <http://docs.python.org/2/tutorial/controlflow.html#default-argument-values>`_
* `Keyword arguments <http://docs.python.org/2/tutorial/controlflow.html#keyword-arguments>`_
* `Argument lists <http://docs.python.org/2/tutorial/controlflow.html#arbitrary-argument-lists>`_
* `Numpy's data arrays <https://docs.scipy.org/doc/numpy-dev/user/quickstart.html>`_


Elements
--------

.. glossary::

   variable

      Just like in any programming language, a user-specified textual name that holds a value.


   value

      The specific value of a variable.


   instance

      A mapping between variables and a specific value for each of these variables (see `~sciexp2.common.instance.Instance`, which is, indeed, a python :class:`dict`), like::

          Instance(var1=84, var2="something")


   instance group

      An ordered container for storing instances (see `~sciexp2.common.instance.InstanceGroup`)::

          InstanceGroup([Instance(var1=84, var2="something"),
                         Instance(var1=48, var2="something"),
                         Instance(var1=84, var2="else")])


   expression

      A string with references to an arbitrary number of variables.

      The default format for referencing variables is ``@variablename@``::

          "sometext-@var1@/@var2@:moretext"


   filter

      A string to express a set of conditions that the values of an instance must match (see `~sciexp2.common.filter.Filter`)::

          "var1 > 30*2 && var2 == 'something'"

      You can also use *programmatic filters* to have a more streamlined interface  (see `~sciexp2.common.filter.PFilter`)::

          (v_.var1 > 30*2) & (v_.var2 == 'something')


Operations
----------

.. glossary::

   translation

      :term:`Expressions <expression>` can be *translated* into strings.

      The most common translation process is a *dictionary-based translation* through an :term:`instance`, which substitutes references to :term:`variables <variable>` in an expression with the values in the given instance.

      For example, translating the expression ``"sometext-@var1@/@var2@:moretext"`` with the instance::

          Instance(var1=84, var2="something")

      yields ``"sometext-84/something:moretext"``.

      For the sake of completeness, translators other than dictionary-based are also provided (see the class hierarchy for `~sciexp2.common.varref.Xlator` in the `~sciexp2.common.varref` module).

   expansion

      :term:`Expressions <expression>` can be *expanded* with a given reference `instance group` (see `~sciexp2.common.instance.Expander`).

      The result is (roughly) an ordered dictionary of instance groups, where each group contains all instances that have the same :term:`translation` for the expanded expression, so that expanding ``"foo @var1@ bar"`` with the previous example :term:`instance group` would return::

          {"foo 84 bar": InstanceGroup([Instance(var1=84, var2="something"),
                                        Instance(var1=84, var2="else")])),
           "foo 48 bar": InstanceGroup([Instance(var1=48, var2="something")])}

   extraction

      :term:`Instances <instance>` can be *extracted* from a given reference `expression` (see `~sciexp2.common.instance.InstanceExtractor`).

      The result is one instance with the variables in the reference expression and the values that appear on the input string. This can be thought of as the inverse of :term:`translation`, so that extracting an instance from the text ``"sometext-100/baz:moretext"`` with the reference expression ``"sometext-@var1@/@var2@:moretext"`` yields::

          Instance(var1=100, var2="baz")
