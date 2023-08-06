Lweb: A light-weight python web framework, shameless copy from bottle.
======================================================================

.. image:: https://img.shields.io/pypi/v/lweb.svg
    :target: https://pypi.python.org/pypi/lweb

Lweb is a light-weight python wsgi framework, shameless copy from bottle.
No builtin template engine.
No builtin server, need thirdpart wsgi driver.

Installation
------------
The last stable release is available on PyPI and can be installed with ``pip``::

    $ pip install lweb

Example
--------
.. code:: python

    import lweb

    def r_index():
        return "hello!"

    urls = [
        ('/', r_index),
    ]

    app = lweb.Application()
    app.add_urls(urls)

    if __name__ == '__main__':
        import bjoern
        print 'Wsgi server start!'
        bjoern.run(app, '0.0.0.0', 7000)


For more examples, see `example.py <https://github.com/zii/lweb/blob/master/example.py>`_ and `example_project <https://github.com/zii/lweb/blob/master/example_project>`_

Features
--------
- Only pure WSGI app is provided
- Django style url router
- Concurrent safe
- Gevent friendly
