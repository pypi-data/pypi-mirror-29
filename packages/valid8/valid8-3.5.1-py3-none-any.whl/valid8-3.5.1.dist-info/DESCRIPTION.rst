python-validate (valid8)
========================

|Build Status| |Tests Status| |codecov| |Documentation| |PyPI|

*"valid8ing is not a crime" ;-)*

``valid8`` provides user-friendly tools for

-  general-purpose inline validation,
-  function inputs/outputs validation
-  class fields validation.

All entry points raise consistent ``ValidationError`` including all
contextual details, with dynamic inheritance of
``ValueError``/``TypeError`` as appropriate. Originally from the
`autoclass <https://smarie.github.io/python-autoclass/>`__ project.

This is the readme for developers. The documentation for users is
available here: https://smarie.github.io/python-valid8/

Want to contribute ?
--------------------

Contributions are welcome ! Simply fork this project on github, commit
your contributions, and create pull requests.

Here is a non-exhaustive list of interesting open topics:
https://github.com/smarie/python-valid8/issues

Running the tests
-----------------

This project uses ``pytest``.

.. code:: bash

    pytest -v valid8/tests/

You may need to install requirements for setup beforehand, using

.. code:: bash

    pip install -r ci_tools/requirements-test.txt

Packaging
---------

This project uses ``setuptools_scm`` to synchronise the version number.
Therefore the following command should be used for development snapshots
as well as official releases:

.. code:: bash

    python setup.py egg_info bdist_wheel rotate -m.whl -k3

You may need to install requirements for setup beforehand, using

.. code:: bash

    pip install -r ci_tools/requirements-setup.txt

Generating the documentation page
---------------------------------

This project uses ``mkdocs`` to generate its documentation page.
Therefore building a local copy of the doc page may be done using:

.. code:: bash

    mkdocs build

You may need to install requirements for doc beforehand, using

.. code:: bash

    pip install -r ci_tools/requirements-doc.txt

Generating the test reports
---------------------------

The following commands generate the html test report and the associated
badge.

.. code:: bash

    pytest --junitxml=junit.xml -v valid8/tests/
    ant -f ci_tools/generate-junit-html.xml
    python ci_tools/generate-junit-badge.py

PyPI Releasing memo
~~~~~~~~~~~~~~~~~~~

This project is now automatically deployed to PyPI when a tag is
created. Anyway, for manual deployment we can use:

.. code:: bash

    twine upload dist/* -r pypitest
    twine upload dist/*

.. |Build Status| image:: https://travis-ci.org/smarie/python-valid8.svg?branch=master
   :target: https://travis-ci.org/smarie/python-valid8
.. |Tests Status| image:: https://smarie.github.io/python-valid8/junit/junit-badge.svg?dummy=8484744
   :target: https://smarie.github.io/python-valid8/junit/report.html
.. |codecov| image:: https://codecov.io/gh/smarie/python-valid8/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/smarie/python-valid8
.. |Documentation| image:: https://img.shields.io/badge/docs-latest-blue.svg
   :target: https://smarie.github.io/python-valid8/
.. |PyPI| image:: https://img.shields.io/badge/PyPI-valid8-blue.svg
   :target: https://pypi.python.org/pypi/valid8/


