.. image:: https://travis-ci.org/cdumay/flask-graylog-bundle.svg?branch=master
    :target: https://travis-ci.org/cdumay/flask-graylog-bundle

====================
flask-graylog-bundle
====================

Graylog extension for Flask

----------
Quickstart
----------

First, install flask-graylog-bundle using `pip <https://pip.pypa.io/en/stable/>`_::

    pip install flask-graylog-bundle

--------------
Auth extension
--------------

To enable Graylog auth, add a :code:`GraylogAuth` instance to your code:

.. code-block:: python

    from flask import current_app as app
    from flask_graylog_bundle.auth import GraylogAuth
    
    app.config.update({
       "GRAYLOG_API_URL": "http://127.0.0.1:12900"
    })
    
    auth = GraylogAuth(app)
    

You can take a look at `examples/auth.py <examples/auth.py>`_ for more complete example. Flask's
`application factories <http://flask.pocoo.org/docs/patterns/appfactories/>`_
and `blueprints <http://flask.pocoo.org/docs/blueprints/) can be used too>`_.

It provides a login decorator :code:`login_required`. To use it just wrap a view function:

.. code-block:: python

    @app.route('/secret-page')
    @auth.login_required
    def secret_page():
        return jsonify({
            "message": "hello",
            "username": auth.username
        })

Additionnal info can be accessed using :code:`g.user` (see: Graylog REST API result of GET /users/{username})

**NOTE:** Graylog tokens are supported, take a look at the Graylog REST API documentation.

----------
API client
----------

To use query Graylog API, add a :code:`GraylogAPIServer` instance to your code:

.. code-block:: python

    from flask import Flask
    from flask_graylog_bundle.server import GraylogAPIServer
    
    app = Flask(__name__)
    app.config.update({
        "GRAYLOG_API_URL": "http://127.0.0.1:12900",
        "GRAYLOG_API_USERNAME": "admin",
        "GRAYLOG_API_PASSWORD": "admin"
    })
    
    api = GraylogAPIServer(app)

You can take a look at `examples/api.py <examples/api.py>`_ for a complete example.

-------
License
-------

Apache License 2.0