completion
=============================

|pypi-badge| |travis-badge| |codecov-badge| |doc-badge| |pyversions-badge|
|license-badge|

A library for tracking completion of blocks by learners in edX courses.

Overview
________

This repository provides a Django model `BlockCompletion` that is intended to be plugged into ``edx-platform``.  It
provides various handlers and services for the recording of completion data.  It also provides a DRF API for submitting
completion data in batches.

License
-------

The code in this repository is licensed under the AGPL 3.0 unless
otherwise noted.

Please see ``LICENSE.txt`` for details.

How To Contribute
-----------------

Contributions are very welcome.

Please read `How To Contribute <https://github.com/edx/edx-platform/blob/master/CONTRIBUTING.rst>`_ for details.

Even though they were written with ``edx-platform`` in mind, the guidelines
should be followed for Open edX code in general.

PR description template should be automatically applied if you are sending PR from github interface; otherwise you
can find it it at `PULL_REQUEST_TEMPLATE.md <https://github.com/edx/completion/blob/master/.github/PULL_REQUEST_TEMPLATE.md>`_

Issue report template should be automatically applied if you are sending it from github UI as well; otherwise you
can find it at `ISSUE_TEMPLATE.md <https://github.com/edx/completion/blob/master/.github/ISSUE_TEMPLATE.md>`_

Reporting Security Issues
-------------------------

Please do not report security issues in public. Please email security@edx.org.

Getting Help
------------

Have a question about this repository, or about Open edX in general?  Please
refer to this `list of resources`_ if you need any assistance.

.. _list of resources: https://open.edx.org/getting-help


.. |pypi-badge| image:: https://img.shields.io/pypi/v/completion.svg
    :target: https://pypi.python.org/pypi/completion/
    :alt: PyPI

.. |travis-badge| image:: https://travis-ci.org/edx/completion.svg?branch=master
    :target: https://travis-ci.org/edx/completion
    :alt: Travis

.. |codecov-badge| image:: http://codecov.io/github/edx/completion/coverage.svg?branch=master
    :target: http://codecov.io/github/edx/completion?branch=master
    :alt: Codecov

.. |doc-badge| image:: https://readthedocs.org/projects/completion/badge/?version=latest
    :target: http://completion.readthedocs.io/en/latest/
    :alt: Documentation

.. |pyversions-badge| image:: https://img.shields.io/pypi/pyversions/completion.svg
    :target: https://pypi.python.org/pypi/completion/
    :alt: Supported Python versions

.. |license-badge| image:: https://img.shields.io/github/license/edx/completion.svg
    :target: https://github.com/edx/completion/blob/master/LICENSE.txt
    :alt: License


Change Log
----------

..
   All enhancements and patches to completion will be documented
   in this file.  It adheres to the structure of http://keepachangelog.com/ ,
   but in reStructuredText instead of Markdown (for ease of incorporation into
   Sphinx documentation and the PyPI description).

   This project adheres to Semantic Versioning (http://semver.org/).

.. There should always be an "Unreleased" section for changes pending release.

Unreleased
~~~~~~~~~~
* Nothing

[0.0.7] - 2018-02-15
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Add settings and service method for determining completion-by-viewing delay.

  [0.0.6] - 2018-02-13
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Add the additional completion logic into the service and models from edx-platform

[0.0.2] - 2018-01-31
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Fix up edx-lint requirements shenanigans.


[0.0.1] - 2018-01-31
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Initial release


