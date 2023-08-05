Bonsai Config
=============

A python library reading and writing bonsai configuration files.

Installation
------------

Install the latest stable from PyPI:

::

    $ pip install bonsai-config

Install the latest in-development version:

::

    $ pip install https://github.com/BonsaiAI/bonsai-config

Usage
-----

Once installed, import ``bonsai_config`` in order to access methods to
read and write configuration files used by
`bonsai-cli <https://github.com/BonsaiAI/bonsai-cli>`__ and
`bonsai-python <https://github.com/BonsaiAI/bonsai-python>`__.

::

    from bonsai_config import BonsaiConfig

    # Read properties from the main bonsai config file:
    bonsai_config = BonsaiConfig()
    print(bonsai_config.username())
    print(bonsai_config.access_key())

    # Write properties to the main bonsai config file:
    bonsai_config = BonsaiConfig()
    bonsai_config.update_access_key_and_username('new_access_key', 'new_username')


