==========
Py-Context
==========

.. image:: https://badge.fury.io/py/py-context.png
    :target: http://badge.fury.io/py/py-context

.. image:: https://travis-ci.org/dealertrack/py-context.png?branch=master
    :target: https://travis-ci.org/dealertrack/py-context

.. image:: https://coveralls.io/repos/dealertrack/py-context/badge.png?branch=master
    :target: https://coveralls.io/r/dealertrack/py-context?branch=master

Python dict with stacked context data

* Free software: MIT license
* GitHub: https://github.com/dealertrack/py-context

Installing
----------

You can install ``py-context`` using pip::

    $ pip install py-context

Example
-------

::

    >>> context = Context({'user': 'Fred', 'city': 'Bedrock'})
    >>> context['user']
    'Fred'
    >>> context['city']
    'Bedrock'
    >>> context.push({'user': 'Barney'})
    >>> context['user']
    'Barney'
    >>> context['city']
    'Bedrock'
    >>> context.pop()
    {'user': 'Barney'}
    >>> context['user']
    'Fred'

Context also supports signals.
Signal handler can be attached globally::

    >>> @context_key_changed.connect
    ... def handler(sender, context, key, new, old):
    ...     print(key, new, old)

    >>> context = Context()
    >>> context['hello'] = 'world'
    hello world <Missing>

Or to individual context instances::

    >>> def handler(sender, context, key, new, old):
    ...     print(key, new, old)
    >>> context = Context()
    >>> context_key_changed.connect(handler, sender=context)

Supported signals::

    >>> @context_initialized.connect
    ... def handler(sender, context):
    ...     pass

    >>> @pre_context_changed.connect
    ... def handler(sender, context):
    ...     pass

    >>> @post_context_changed.connect
    ... def handler(sender, context):
    ...     pass

    >>> @context_key_changed.connect
    ... def handler(sender, context, key, new, old):
    ...     pass

Additionally, ``ClassSignallingContext`` can be used to subscribe signals
by sender classes, not instances::

    >>> class TestContext(ClassSignallingContext):
    ...     pass
    >>> def context_key_changed_handler(sender, context, key, new, old):
    ...     print(key, new, old)
    >>> _ = context_key_changed.connect(context_key_changed_handler, sender=TestContext)

    >>> context = Context()
    >>> class_context = TestContext()

    >>> context['foo'] = 'bar'
    >>> class_context['foo'] = 'bar'
    foo bar <Missing>

Testing
-------

To run the tests you need to install testing requirements first::

    $ make install

Then to run tests, you can use ``nosetests`` or simply use Makefile command::

    $ nosetests -sv
    # or
    $ make test
