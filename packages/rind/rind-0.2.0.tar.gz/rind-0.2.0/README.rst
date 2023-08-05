Rind
====

Rind (Run in Docker) is a simple command line tool for executing things inside docker containers.


Installation
------------

Whilst Rind is a Python package and can be installed with `pip`, the preferred method of installed is to download the latest binary release and place it somewhere on the system ``PATH``


Configuration
-------------

To `rind` enable a container a  ``app.rind`` label needs to be added. Do do this in a ``docker-compose.yml`` you would do the following:

.. code-block:: yaml

    services:
        a_service:
            image: an_image
            labels:
                - app.rind


Rind also has the ability to run pre-steps when executing inside the container. For example activating a Python virtualenv.

To enable a pre-step you need to add it as a value to your label.

.. code-block:: yaml

    services:
        a_service:
            image: an_image
            labels:
                app.rind: "source /venv/bin/activate"


This assumes you virtualenv is at ``/venv`` within your docker container. It will be combined with the actual command passed in. e.g.: ``rind /bin/sh``  would be run in your container as ``source /venv/bin/activate && /bin/sh``


Running
-------

Effectively anything passed as a command line argument is executed directly within the rind enabled container. e.g.

.. code-block:: bash

    rind ./manage.py migration


Would run the ``manage.py`` script in the containers working directory, passing it the ``migrate`` argument

If no parameters are passed to ``rind`` then the default ``/bin/sh`` is used which will give you and interactive terminal.

