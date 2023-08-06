Dmpy
====

`DistributedMake <https://github.com/wkretzsch/DM>`_ for Python.

This project uses `Semantic versioning <http://semver.org/spec/v2.0.0.html>`_.

Installation from pypi
----------------------
::

    pip install dmpy

Installation from github
------------------------
::

    pip install git+git://github.com/kvg/dmpy.git attrs

Examples
--------
Contents of an example dmpy script::

    # example.py
    from dmpy import DistributedMake, get_dm_arg_parser

    args = get_dm_arg_parser().parse_args()
    m = DistributedMake(args_object=args)

    m.add("test_output_file", None, "echo 'hi world'")
    m.execute()

Then run example.py::

    # get a dry-run of all commands to be executed
    python example.py

    # run all commands
    python example.py -r

Tests
-----
::

    make test

Bugs
----

Please raise an issue on `the github page <https://github.com/kvg/dmpy>`_ to report a bug.

Development
-----------

We now have a Pipfile and Pipfile.lock for use with `pipenv <http://docs.pipenv.org/en/latest/>`_ !

Please always update your Pipfile.lock (`pipenv lock`) before making a PR.
