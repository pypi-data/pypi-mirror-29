Temptation
==========

Temptation is a simple and straightforward template engine with an
extensible grammar.

Objectives
==========

Regular-expression-based
------------------------

Substitution in *temptation* templates is based on regular expressions.

Apart from the obvious limitations regarding nested
substitution-expressions (they may be supported to a certain extent)
this comes with two advantages:

-  Extensibility
-  Efficient regular-expression scanning rather than complex parsing.

Semantic expression substitution
--------------------------------

Rather than always expecting key-value pairs as input *temptation*
provides the ability to apply different substitution algorithms on
different template-expressions.

Extensibility
-------------

The regular-expression based grammar can be easily extended or
customized by adding custom resolvers.

MVC-based templating
--------------------

Template languages are a way to separate the view (presentation) from
the data model.

Many (if not most) template languages support control structures like
conditions or loops. So their templates combine presentation with
control.

*temptation* intentionally doesn’t.

This comes with limitations and with advantages. An obvious limitation
is that with using *temptation* on its own you can’t process data in a
non-linear way. There is only one path from the beginning to the end of
the template.

Advantages are:

-  The linear approach keeps templates simple and very well readable.
-  Templates are easy to test.
-  *temptation* templates can easily be be used by external controllers
   that care about more complex transformation-related issues like
   conditional processing or iteration.

   *ynot* is a transformator making use of the *temptation* grammar and
   this reference-implementation. See `ynot overview on
   github <https://github.com/yaccob/ynot/blob/master/README.md>`__.

Limited support for nested template expressions
-----------------------------------------------

This is not implemented yet because I didn’t find a reasonable use-case.
But it could be added quite easily if it turns out that it makes sense.

Setup
=====

.. code:: bash

    $ pip install temptation

By installing *temptation* via ``pip`` you automatically get the command
line interface of *temptation* installed as well.

Command-Line-Interface (CLI)
============================

The purpose of the command line interface is to support processing
data-files (``yaml`` or ``json``) against a single template-file.

To get help on the (currently quite limited) command-line options just
enter

``temtation -h``

and you’ll see an output like this:

::

    Usage: scripts/temptation [OPTION] -t template datafile...

    Resolve template for datafiles. Datafiles can be yaml or json

    Options:
      --version             show program version number and exit
      -h, --help            show this help message and exit
      -t TEMPLATEFILENAME, --template=TEMPLATEFILENAME
                            Template to be resoved

In the current version if you use multiple data-files as input they need
to be in ``yaml`` format and every file must begin with a
document-separator (``---``).

This limitation may be removed in future versions so that it will also
be possible to process multiple ‘json’ data-files which is currently not
possible because json doesn’t support multiple documents.

Command-line Expample
---------------------

Let’s say we have this text file …

``temlate.txt``:

::

    ${greeting} ${name}!

… and the following data-files:

``data1.yaml``:

.. code:: yaml

    ---
    greeting: Hello
    name: world

``data2.yaml``:

.. code:: yaml

    ---
    greeting: Good morning
    name: Donald Duck

Now let’s see how *temptation* applies the template to the data-files:

::

    $ temptation -t template.text data*.yaml
    Hello world!
    Good morning Donald Duck!

Quite simple, right?

Imports
=======

The following samples assume that you have imported the ``Template``
class like this:

.. code:: python

    >>> from temptation import Template

Samples
=======

Just static text
----------------

Any text that’s not a *temptation* expression is left unchanged.

.. code:: python

    >>> Template("Hello world").resolve()
    u'Hello world'

There are some pre-defined *temptation* expressions:

-  ``${key}``: Map resolution
-  ``@{jsonpath}``: Jsonpath resolution for single match
-  ``@*{jsonpath}``: Jsonpath resolution for multiple match
-  ``!{python expression}``: Python evaluation expression

If you need to use a literal that matches those expressions you need to
escape it with a backslash ``\`` like this:

``\${whatever}``

In the expanded template the backslash will be removed but the
expression won’t be evaluated.

Literal baskslashes can be escaped by a backslash as well. So ``\\`` in
the template will be presented as ``\`` in the output. You will see
samples for this further down.

Let’s now see samples for the pre-defined *temptation* expressions and
how they are expanded.

Map resolution: ``${key}``
--------------------------

One of the pre-defined *temptation* expressions is a simple key-value
substitution.

The expression’s value is interpreted as a key that will be substituted
by the corresponding value of the input data.

.. code:: python

    >>> Template("${greeting} ${name}").resolve({"greeting": "Hello", "name": "world"})
    u'Hello world'

Escaping tags: ``\${key}``
--------------------------

Any pre-defined (or custom) *temptation* expression can be escaped by
preceding it with a backslash. A backslash itself can be escaped by
another backslash.

.. code:: python

    >>> Template(r"Hello \${name}").resolve({"name": "world"})
    u'Hello ${name}'

    >>> Template(r"Hello \\${name}").resolve({"name": "world"})
    u'Hello \\world'

Jsonpath resolution for single match: ``@{jsonpath-espression}``
----------------------------------------------------------------

The jsonpath expansion is based on the
`jsonpath-ng <https://pypi.python.org/pypi/jsonpath-ng/1.4.3>`__
implementation, so the syntax is predetermined by this implementation.
Please read the linked documentation for details.

A jsonpath result always returns an array of matches. This array may
contain 0..n items. To represent a result that matches multiple items
*temptation* is enclosing the matches in brackets:
``[item1, item2, ...]``.

In a template you’re often interested in a single match and don’t want
this to be enclosed in brackets. That’s why *temptation* supports the
*single match* resolution. It will omit the enclosing brackets if there
is a single match. In case of multiple matches it will log a warning and
enclose the result in brackets.

.. code:: python

    >>> context = {"items": [{"item": "first item"}, {"item": "second item"}]}
    >>> Template("Hello @{$.items[0].item} and @{$.items[1].item}").resolve(context)
    u'Hello first item and second item'

    >>> Template(u"Hello @{$..item}").resolve(context)
    u"Hello ['first item', 'second item']"

Jsonpath resolution for multiple matches: ``@*{jsonpath expression}``
---------------------------------------------------------------------

Whenever you don’t expect a single match but want to consistently
present the result as a list, you can use this *temptation* expression.

.. code:: python

    >>> context = {"items": [{"item": "first item"}, {"item": "second item"}]}
    >>> Template("Hello @*{$.items[0].item} and @*{$.items[1].item}").resolve(context)
    u"Hello ['first item'] and ['second item']"

    >>> Template(u"Hello @*{$..item}").resolve(context)
    u"Hello ['first item', 'second item']"

Evaluation resolution: ``!{python expression}``
-----------------------------------------------

The python-evaluation resolution allows to expand a *temptation*
expression to the result of any python expression.

Currently the pre-defined evaluation expression is limited to the use of
modules that are imported in the ``template.resolvers`` module. It’s
planned to provide a more flexible solution for importing additional
modules to be accessible from evaluation expressions.

.. code:: python

    >>> Template(u"Hello !{7 + 5}").resolve()
    u'Hello 12'

    >>> context = {"values": [1, 3, 5, 7]}
    >>> Template(u"Hello !{context['values'][2] + context['values'][3]}").resolve(context)
    u'Hello 12'

Adding your own resolvers
=========================

You can extend *temptation*\ ’s capabilities by implementing your own
resolvers.

To do so you must first import the ``Resolvers`` class:

Import Resolvers
----------------

.. code:: python

    >>> from temptation import Resolvers, Resolver

Custom resolver sample
----------------------

.. code:: python

    >>> def resolve_foo(expression, match, context):
    ...     return "foofoo"
    >>> def resolve_bar(expression, match, context):
    ...     return "barbar"
    >>> resolvers = Resolvers().add(
    ...     Resolver("foomatcher", tag=r"\$foo", samples=["$foo{}"], processor=resolve_foo)).add(
    ...     Resolver("barmatcher", tag=r"\$bar", samples=["$bar{}"], processor=resolve_bar))
    >>> Template("Hello $foo{} and $bar{}", resolvers).resolve()
    u'Hello foofoo and barbar'

Resolvers are validated against samples
---------------------------------------

It is also ensured that samples don’t match with other resolvers. This
is an attempt to help avoiding ambiguities (but obviously doesn’t
guarantee that there is no intersection between regular expressions of
different resolvers).

.. code:: python

    >>> def resolve_foo(expression, match, context):
    ...     return "foofoo"
    >>> def resolve_bar(expression, match, context):
    ...     return "barbar"
    >>> resolvers = Resolvers().add(
    ...     Resolver("foomatcher", tag=r"\$x", samples=["$x{whatever}"], processor=resolve_foo)).add(
    ...     Resolver("barmatcher", tag=r"\$xx*", samples=["$xxx{whatever}"], processor=resolve_bar))
    Traceback (most recent call last):
     ...
    Exception: sample '$x{whatever}' for resolver 'barmatcher' also matches resolver 'foomatcher'



