    :Author: jianglin

.. contents::

1 flask-avatar
--------------

.. image:: https://img.shields.io/badge/pypi-v0.1.2-brightgreen.svg
    :target: https://pypi.python.org/pypi/Flask-Avatar
.. image:: https://img.shields.io/badge/python-3.4-brightgreen.svg
    :target: https://pypi.python.org/pypi/Flask-Avatar
.. image:: https://img.shields.io/badge/license-BSD-blue.svg
    :target: LICENSE

1.1 Example
~~~~~~~~~~~

.. image:: //raw.githubusercontent.com/honmaple/flask-avatar/master/example/avatar1.png

.. image:: //raw.githubusercontent.com/honmaple/flask-avatar/master/example/avatar2.png

.. image:: //raw.githubusercontent.com/honmaple/flask-avatar/master/example/avatar3.png

1.2 Installation
~~~~~~~~~~~~~~~~

To install Flask-Avatar:

.. code:: shell

    pip install flask-avatar

Or alternatively, you can download the repository and install manually by doing:

.. code:: sehll

    git clone git@github.com:honmaple/flask-avatar.git
    cd flask-avatar
    python setup.py install

1.3 Usage
~~~~~~~~~

.. code:: python

    from flask_avatar import Avatar
    [...]
    Avatar(app)
    # or use cachefunc
    Avatar(app, cache=cachefunc)

**cachefunc** must be a decorator:
example:

.. code:: python

    def cachefunc(func):
        @wrap(func)
        def _cache(*args, **kwargs):
            r = cacheclient.get("cache key")
            if r is not None:
                return r
            return func(*args, **kwargs)
        return _cache

Templates:

.. code:: html

    {{ url_for('avatar',text = user.username )}}

or set **width** with:

.. code:: html

    {{ url_for('avatar',text = user.username,width=60)}}

1.4 Config
~~~~~~~~~~

.. code:: python

    AVATAR_URL = '/avatar' #The avatar url,default '/avatar/<text>/<width>'
    AVATAR_RANGE = [0,512] #set avatar range to allow generate,if disallow,abort(404).Default [0,512]

1.5 Thanks to
~~~~~~~~~~~~~

`https://github.com/maethor/avatar-generator <https://github.com/maethor/avatar-generator>`_
