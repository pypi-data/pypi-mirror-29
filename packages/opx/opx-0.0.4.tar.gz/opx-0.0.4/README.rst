OpenSwitch Development Tool
===========================

.. image:: https://img.shields.io/pypi/v/opx.svg
    :target: https://pypi.python.org/pypi/opx

.. image:: https://img.shields.io/pypi/l/opx.svg
    :target: https://pypi.python.org/pypi/opx

.. image:: https://img.shields.io/pypi/pyversions/opx.svg
    :target: https://pypi.python.org/pypi/opx

.. contents:: **Table of Contents**
    :backlinks: none

Installation
------------

.. code-block:: bash

    $ pip install opx

Requirements
~~~~~~~~~~~~

- `Docker <https://docs.docker.com/engine/installation/>`_
- `Git <https://git-scm.com/>`_
- `Repo <https://source.android.com/setup/downloading#installing-repo>`_

Getting Started
---------------

.. code-block:: bash

    # initialize your workspace
    $ opx init

    # build all packages
    $ opx build

    # enter a development shell and build a package however you like
    $ opx shell
    opx@XXXXXXXXXXXX:/mnt$ cd opx-logging
    opx@XXXXXXXXXXXX:/mnt$ mk-build-deps --root-cmd sudo --install --remove
    opx@XXXXXXXXXXXX:/mnt$ dpkg-buildpackage -us -uc
    opx@XXXXXXXXXXXX:/mnt$ fakeroot debian/rules binary
    opx@XXXXXXXXXXXX:/mnt$ exit

    # assemble an installer
    $ opx assemble --dist 2.2

    # remove persistent container
    $ opx remove

    # you can also choose to remove the container when a command finishes
    $ opx assemble --dist 2.2 --rm

    # clean up workspace completely
    $ rm -rf opx-*/ .repo
    $ opx cleanup

New Features (Over `opx-build <https://github.com/open-switch/opx-build>`_)
---------------------------------

* Persistent containers (if inside a workspace)

.. code-block:: bash

    $ opx shell
    opx@XXXXXXXXXXXX:/mnt$ echo foo > /bar
    opx@XXXXXXXXXXXX:/mnt$ exit
    $ opx shell
    opx@XXXXXXXXXXXX:/mnt$ cat /bar
    foo

* Build then tag repository for publishing

.. code-block:: bash

    $ opx release opx-logging

* Build and sort packages for easy sharing/publishing

.. code-block:: bash

    $ opx build opx-logging --sort
    $ tree ./pkg
    ./pkg
    └── opx-logging/
        ├── libopx-logging1_2.1.0_amd64.deb
        ├── libopx-logging-dev_2.1.0_amd64.deb
        ├── opx-logging_2.1.0_amd64.build
        ├── opx-logging_2.1.0_amd64.deb
        ├── opx-logging_2.1.0.dsc
        ├── opx-logging_2.1.0.tar.gz
        └── python-opx-logging_2.1.0_amd64.deb

Command Line Completion
-----------------------

Run the command corresponding with your shell. Add to your shell startup file for persistent autocomplete.

.. code-block:: bash

    # bash
    $ eval "$(_OPX_COMPLETE=source-bash opx)"

    # zsh
    $ eval "$(_OPX_COMPLETE=source-zsh opx)"

    # fish
    $ eval (env _OPX_COMPLETE=source-fish opx)

Planned Features
----------------

* Port ``opx_build`` from shell to python
* Port ``opx_rel_pkgasm`` from python script to module
* Port ``opx_get_packages`` from python script to module
* Port ``opx_bld_basics`` from python script to module

License
-------

opx is distributed under the terms of the
`MIT License <https://choosealicense.com/licenses/mit>`_.
