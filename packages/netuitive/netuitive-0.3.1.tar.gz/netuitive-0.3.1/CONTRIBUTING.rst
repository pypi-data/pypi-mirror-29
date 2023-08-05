===========================================
Contributing to the Netuitive Python Client
===========================================

Contributions are welcome and can be represented in many different ways as noted below. Help is greatly appreciated and credit will always be given.

Types of Contributions
----------------------

Reporting Bugs
~~~~~~~~~~~~~~
Report bugs on `the issues page <https://github.com/Netuitive/kbn/issues>`_. With your bug report, please include:

- Your operating system name and version.
- Any details about your local setup that might be helpful in troubleshooting the issue.
- Detailed steps to reproduce the bug.

Fixing Bugs
~~~~~~~~~~~~
Find bugs at `the issues page <https://github.com/Netuitive/kbn/issues>`_. Anything tagged with "bug" is open to be fixed. With your fix, please include:

- The issue number
- A detailed commit message

Implementing Features
~~~~~~~~~~~~~~~~~~~~~~
Find features at `the issues page <https://github.com/Netuitive/kbn/issues>`_. Anything tagged with "feature" is open to be implemented. With your feature, please include:

- The issue number
- A detailed commit message

Write Documentation
~~~~~~~~~~~~~~~~~~~
The Netuitive Python Client can always use documentation (more documentation is always better!). Please document your features or usage as part of the official docs, in docstrings, in blog posts, articles, or wherever you see fit.

Submit Feedback
~~~~~~~~~~~~~~~
File an issue at `the issues page <https://github.com/Netuitive/kbn/issues>`_. If you are proposing a feature:

- Explain how it would work in detail
- Keep the scope as narrow as possible to make it easier to implement

Workflow
------------

#. Create a branch directly in this repo or a fork (if you don't have push access). Please name branches within this repository ``feature/<description>`` or ``fix/description``. For example, something like ``feature/upgrade_agent_0.2.3-70``.

#. Create an issue or open a pull request (PR). If you aren't sure your PR will solve the issue or may be controversial, we're okay with you opening an issue separately and linking to it in your PR. That way, if the PR is not accepted, the issue will remain and be tracked.

#. Clone your fork locally::

    $ git clone git@github.com:your_name_here/netuitive.git

#. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development::

    $ mkvirtualenv netuitive
    $ cd netuitive/
    $ python setup.py develop

#. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

#. When you're done making changes, check that your changes pass flake8 and the tests, including testing other Python versions with tox::

    $ flake8 netuitive tests
    $ python setup.py test
    $ tox

   To get flake8 and tox, just pip install them into your virtualenv.
   
#. Close (and reference) issues by the ``closes #XXX`` or ``fixes #XXX`` notation in the commit message. Please use a descriptive, useful commit message that could be used to understand why a particular change was made.

#. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

#. Keep pushing commits to the initial branch using ``--amend``/``--rebase`` as necessary. Don't mix unrelated issues in a single branch.

#. Clean up the branch (rebase with master to synchronize, squash, edit commits, test, etc.) to prepare for it to be merged.

#. If you didn't open a pull request already, do so now. Ensure it meets the following guidelines:
    #. The pull request should include tests.
    #. If the pull request adds functionality, the docs should be updated. Put your new functionality into a function   with a docstring, and add the feature to the list in README.rst.
    #. The pull request should work for Python 2.6, 2.7, 3.3, and 3.4, and for PyPy.

#. After reviewing your commits for documentation, passed continuous integration (CI) tests, version bumps, changelogs, and good, descriptive commit messages, a project maintainer can merge your request.

#. Create/update the changelog if necessary.

Additional Information
-----------------------

Tips
~~~~~
To run a subset of tests::

    $ python -m unittest tests.test_netuitive
