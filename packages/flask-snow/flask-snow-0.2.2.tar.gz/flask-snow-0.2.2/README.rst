.. image:: https://coveralls.io/repos/github/rbw0/flask-snow/badge.svg?branch=master
    :target: https://coveralls.io/github/rbw0/flask-snow?branch=master
.. image:: https://travis-ci.org/rbw0/flask-snow.svg?branch=master
    :target: https://travis-ci.org/rbw0/flask-snow
.. image:: https://badge.fury.io/py/flask-snow.svg
    :target: https://pypi.python.org/pypi/flask-snow

flask-snow
============

Adds ServiceNow support to Flask.

**Why?**

Simplicity and responsiveness are two key ingredients to a successful UX, I believe the ServiceNow UI lacks both.


**What can be done differently with flask-snow?**

It lets you create a fully customizable Flask-powered platform on top of the ServiceNow REST API in a simple and seamless way with the help of the `pysnow library <https://github.com/rbw0/pysnow>`_.

Some usage examples:

- Create *your own software stack* that integrates with ServiceNow.
- Add ServiceNow support to *your current Flask project*.
- Create a *micro-service API relay*, and perhaps use with a project *written in another language*.


Documentation
-------------
The documentation can be found `here <http://flask-snow.readthedocs.org/>`_


Installation
------------

    $ pip install flask-snow

Usage
-----

Minimal example.

Reads the *config*, sets up the *snow extension* and creates a route accessed at */incidents* which returns a list of incidents.

.. code-block:: python

    from flask import Flask, request, jsonify
    from flask_snow import Snow

    app = Flask(__name__)
    app.config.from_object('settings')

    snow = Snow(app)


    @app.route('/incidents')
    def incident_list():
        limit = request.args.get('limit') or 10

        r = snow.resource(api_path='/table/incident')
        data = r.get(query={}, limit=limit).all()

        # Return a list of incidents
        return jsonify(list(data))


    if __name__ == '__main__':
        app.run()


Name it **server.py** and run with ``python server.py``


Check out the **examples directory** for more examples!


Compatibility
-------------
- Python 2 and 3
- Flask > 0.9

Author
------
Created by Robert Wikman <rbw@vault13.org> in 2018

JetBrains
---------
Thank you `Jetbrains <www.jetbrains.com>`_ for creating ``pycharm`` and for providing me with free licenses :thumbsup:


