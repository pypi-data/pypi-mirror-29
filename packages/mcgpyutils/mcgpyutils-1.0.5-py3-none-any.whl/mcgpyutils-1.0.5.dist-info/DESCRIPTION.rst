mcgpyutils
==========

mcgpyutils(MCG Python Utilities) is a project containing utility classes
commonly used in Python projects at `MCG
Strategic <https://www.mcgstrategic.com/>`__.

Requirements
------------

-  Python3, version >= 3.6

Usage
-----

Example:

::

    from mcgpyutils import FileSystemUtils

    fsu = FileSystemUtils()
    print(fsu.get_path_to_script(__file__))

Development
-----------

Changes to this package can be tested by putting the path to the root of
this repository in the PYTHONPATH environment variable. PYTHONPATH will
take precedence over the installed package and allow new changes to be
used instead of the version installed via pip. To revert this, remove
the path to the root of this repository from the PYTHONPATH. Here are 2
aliases to make switching easy:

::

    # Enable development mode
    alias pyutilsdev='export PYTHONPATH="/path/to/mcgpyutils:$PYTHONPATH"'

    # Revert to installed package (this assumes there's nothing else in your PYTHONPATH)
    alias pyutilsprod='export PYTHONPATH=""'


