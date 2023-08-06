FluidDevOps is a small package which provides some console scripts to
make DevOps easier.

See directory ``docker`` for more on running Docker containers.

Installation
------------

::

    python setup.py develop

Features
--------

-  ``python -m fluiddevops.mirror`` or ``fluidmirror`` to setup hg to
   git mirroring for a group of packages and periodically check for
   updates

::

    usage: fluidmirror [-h] [-c CFG] {list,clone,set-remote,pull,push,sync} ...

    works on a specific / all configured repositories (default)

    positional arguments:
      {list,clone,set-remote,pull,push,sync}
                            sub-command
        list                list configuration
        clone               hg clone
        set-remote          set remote (push) path in hgrc
        pull                hg pull -u
        push                hg push
        sync                sync: pull and push

    optional arguments:
      -h, --help            show this help message and exit
      -c CFG, --cfg CFG     config file


