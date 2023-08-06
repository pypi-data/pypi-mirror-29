*****
PulpFiction
*****

.. image:: ./images/jules.png

*English, *****! Do you speak it?*

A simple tool to detect non-English commments in a code base (directory).

Inspired by the fictional character, `Jules Winnfield, played by Samuel L Jackson in the film, Pulp Fiction`__.

.. __: https://www.urbandictionary.com/define.php?term=Jules%20Winnfield

Install
#######

.. code-block:: bash

    # requires Python3
    $ pip install pulpfiction

Usage
#####

.. code-block:: bash

    $ jules --help

    Usage: jules [OPTIONS]

      Simple tool to detect non-English commments in a code base..

    Options:
      --path TEXT           path to project or repository
      --help                Show this message and exit.


.. code-block:: bash

    # by default, it looks at the current directory or $PWD
    # alternatively,
    $ jules --path=~/personal/my-awesome-git-project


Script exits with `sys.exit(0)` if successful, else the earliest invalid comment is found and raised.

Known Issues
############

- Commented-out code will be considered non-English; false positive.

