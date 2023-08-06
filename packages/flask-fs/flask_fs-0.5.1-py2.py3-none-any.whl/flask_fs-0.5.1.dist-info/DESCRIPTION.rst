========
Flask-FS
========

.. image:: https://travis-ci.org/noirbizarre/flask-fs.svg?tag=v0.5.1
    :target: https://travis-ci.org/noirbizarre/flask-fs
    :alt: Build status
.. image:: https://coveralls.io/repos/noirbizarre/flask-fs/badge.svg?tag=v0.5.1
    :target: https://coveralls.io/r/noirbizarre/flask-fs?tag=v0.5.1
    :alt: Code coverage
.. image:: https://readthedocs.org/projects/flask-fs/badge/?version=0.5.1
    :target: http://flask-fs.readthedocs.org/en/latest/
    :alt: Documentation status

Simple and easy file storages for Flask


Compatibility
=============

Flask-FS requires Python 2.7/3.4+ and Flask 0.10+.

Amazon S3 support requires Boto3.

GridFS support requires PyMongo 3+.

OpenStack Swift support requires python-swift-client.


Installation
============

You can install Flask-FS with pip:

.. code-block:: console

    $ pip install flask-fs
    # or
    $ pip install flask-fs[s3]  # For Amazon S3 backend support
    $ pip install flask-fs[swift]  # For OpenStack swift backend support
    $ pip install flask-fs[gridfs]  # For GridFS backend support
    $ pip install flask-fs[all]  # To include all dependencies for all backends


Quick start
===========

.. code-block:: python

    from flask import Flask
    import flask_fs as fs

    app = Flask(__name__)
    fs.init_app(app)

    images = fs.Storage('images')


    if __name__ == '__main__':
        app.run(debug=True)


Documentation
=============

The full documentation is hosted `on Read the Docs <http://flask-fs.readthedocs.org/en/latest/>`_

Changelog
=========

0.5.1 (2018-03-12)
------------------

- Fix ``local`` backend ``list_files()`` nested directories handling

0.5.0 (2018-03-12)
------------------

- Added ``metadata`` method to ``Storage`` to retrieve file metadata
- Force ``boto3 >= 1.4.5`` because of API change (lifecycle)
- Drop Python 3.3 support
- Create parent directories when opening a local file in write mode

0.4.1 (2017-06-24)
------------------

- Fix broken packaging for Python 2.7

0.4.0 (2017-06-24)
------------------

- Added backend level configuration ``FS_{BACKEND_NAME}_{KEY}``
- Improved backend documentation
- Use setuptools entry points to register backends.
- Added `NONE` extensions specification
- Added `list_files` to `Storage` to list the current bucket files
- Image optimization preserve file type as much as possible
- Ensure images are not overwritted before rerendering

0.3.0 (2017-03-05)
------------------

- Switch to pytest
- ``ImageField`` optimization/compression.
  Resized images are now compressed.
  Default image can also be optimized on upload with ``FS_IMAGES_OPTIMIZE = True``
  or by specifying `optimize=True` as field parameter.
- ``ImageField`` has now the ability to rerender images with the ``rerender()`` method.

0.2.1 (2017-01-17)
------------------

- Expose Python 3 compatibility

0.2.0 (2016-10-11)
------------------

- Proper github publication
- Initial S3, GridFS and Swift backend implementations
- Python 3 fixes


0.1 (2015-04-07)
----------------

- Initial release



