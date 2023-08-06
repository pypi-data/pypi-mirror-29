SSLCheck |PyPI version|
=======================

A simple command line SSL validator

Features
--------

-  Validate SSL Certificate for host.
-  Allows to specify server, in case DNS records do not point to the
   server.
-  Use any port (443, 8443, 993 etc.)

Installation
------------

SSLCheck requires Python 3 to run.

**Python package**

You can easily install SSLCheck using pip:

``pip3 install sslcheck``

**Manual**

Alternatively, to get the latest development version, you can clone this
repository and then manually install it:

::

    git clone git@gitlab.com:radek-sprta/sslcheck.git
    cd sslcheck
    python3 setup.py install

Usage
-----

Simply run SSLCheck with hostname as argument:

``sslcheck radeksprta.eu``

SSLCheck takes two optional arguments: - ``--server``/``-s`` - Server to
connect to. - ``--port``/``-s`` - Specify port, i.e. 993 for encrypted
IMAP.

Contributing
------------

For information on how to contribute to the project, please check the
`Contributor's
Guide <https://gitlab.com/radek-sprta/sslcheck/blob/master/CONTRIBUTING.md>`__

Contact
-------

mail@radeksprta.eu

`incoming+radek-sprta/sslcheck@gitlab.com <incoming+radek-sprta/sslcheck@gitlab.com>`__

License
-------

MIT License

Credits
-------

This package was created with
`Cookiecutter <https://github.com/audreyr/cookiecutter>`__ and the
`python-cookiecutter <https://gitlab.com/radek-sprta/python-cookiecutter>`__
project template.

.. |PyPI version| image:: https://badge.fury.io/py/sslcheck.svg
   :target: https://badge.fury.io/py/sslcheck


