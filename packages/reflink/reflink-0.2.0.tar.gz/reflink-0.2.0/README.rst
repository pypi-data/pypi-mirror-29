==============
Python reflink
==============


.. image:: https://img.shields.io/pypi/v/reflink.svg
        :target: https://pypi.python.org/pypi/reflink

.. image:: https://gitlab.com/rubdos/pyreflink/badges/master/build.svg
        :target: https://gitlab.com/rubdos/pyreflink/pipelines

.. image:: https://ci.appveyor.com/api/projects/status/ta2rn0irw52ua5sw?svg=true
        :target: https://ci.appveyor.com/project/RubenDeSmet/pyreflink
        :alt: Windows build status

.. image:: https://readthedocs.org/projects/reflink/badge/?version=latest
        :target: https://reflink.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://readthedocs.org/projects/reflink/badge/?version=latest
        :target: https://rubdos.gitlab.io/pyreflink/docs
        :alt: Documentation Status

.. image:: https://gitlab.com/rubdos/pyreflink/badges/master/coverage.svg
        :target: https://rubdos.gitlab.io/pyreflink/coverage
        :alt: Coverage report


Python wrapper around the ``reflink`` system calls.


* Free software: MIT license
* Documentation: https://reflink.readthedocs.io.
* Documentation for master branch: https://rubdos.gitlab.io/pyreflink/docs


Features
--------

* Btrfs, XFS, OCFS2 ``reflink`` support. Btrfs is tested the most.
* Apple macOS APFS ``clonefile`` support. Little testing, be careful. It might eat data.
* A convenience method that checks support for reflinks within a specific directory.

Quick start example
-------------------

To use Python reflink in a project::

    from reflink import reflink
    # Reflink copy 'large_file.img' to 'copy_of_file.img'
    reflink("large_file.img", "copy_of_file.img")

Help wanted
-----------

Someone to implement a `Windows/ReFS implementation <https://gitlab.com/rubdos/pyreflink/issues/1>`__


Support
_______

Support on `the GitLab repository <https://gitlab.com/rubdos/pyreflink/issues>`__,
feel free to file an issue.

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

