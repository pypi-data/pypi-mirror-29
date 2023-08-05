========================================
ITS Private Cloud Command Line Interface
========================================
.. image:: https://gitlab-ee.eis.utoronto.ca/vss/vsscli/badges/master/build.svg
   :target: https://gitlab-ee.eis.utoronto.ca/vss/vsscli/commits/master

.. image:: https://gitlab-ee.eis.utoronto.ca/vss/vsscli/badges/master/coverage.svg
   :target: https://gitlab-ee.eis.utoronto.ca/vss/vsscli/commits/master

.. image:: https://img.shields.io/pypi/v/vsscli.svg
    :target: https://pypi.python.org/pypi/vsscli

.. image:: https://img.shields.io/pypi/pyversions/vsscli.svg
    :target: https://pypi.python.org/pypi/vsscli

.. image:: https://img.shields.io/docker/pulls/uofteis/vsscli.svg
    :target: https://hub.docker.com/r/uofteis/vsscli/

.. image:: https://images.microbadger.com/badges/image/uofteis/vsscli.svg
    :target: https://microbadger.com/images/uofteis/vsscli

.. image:: https://images.microbadger.com/badges/version/uofteis/vsscli.svg
    :target: https://microbadger.com/images/uofteis/vsscli

This package provides a unified command line interface to the ITS Private Cloud.

-------------
Documentation
-------------

Package documentation is now available at `DOCS <https://eis.utoronto.ca/~vss/vsscli/>`__.

------------
Installation
------------

.. note:: Windows users, download and install
  `Python Releases for Windows <https://www.python.org/downloads/windows/>`__ prior
  running `pip`_.

The fastest way to install VSS CLI is to use `pip`_:

.. code-block:: bash

    $ pip install vsscli

If you have the VSS CLI installed and want to upgrade to the latest version
you can run:

.. code-block:: bash

    $ pip install --upgrade vsscli

This will install VSS CLI as well as all dependencies. You can also just `download the tarball`_.
Once you have the `vsscli` directory structure on your workstation, you can just run:

.. code-block:: bash

    $ cd <path_to_vsscli>
    $ python setup.py install

------------
CLI Releases
------------

The release notes for the VSS CLI can be found
`CHANGELOG <https://gitlab-ee.eis.utoronto.ca/vss/vsscli/blob/master/CHANGELOG.rst>`__
in the gitlab repo.

---------------
Getting Started
---------------

Before using VSS CLI, you need setup your VSS credentials. You can do this in a couple of ways:

* Environment variables
* Configuration file

The quickest way to get started is to run the ``vss configure`` command:

.. code-block:: bash

    $ vss configure
    Username []:
    Endpoint [https://vss-api.eis.utoronto.ca]:
    Password:
    Repeat for confirmation:

To use environment variables, set ``VSS_API_USER`` and ``VSS_API_USER_PASS`` or ``VSS_API_TOKEN``:

.. code-block:: bash

    $ export VSS_API_USER=<vss_user>
    $ export VSS_API_USER_PASS=<vss_user_pass>
    # or
    $ export VSS_API_TOKEN=<vss_api_token>

To use a config file, create a configuration as follows:

.. code-block:: json

    {
    "https://vss-api.eis.utoronto.ca": {
        "auth": "<encoded_creds>",
        "token": "<access_token"
        }
    }

Place it in ``~/.vss/config.json`` (or in ``%UserProfile%\.vss\config.json`` on Windows).
If you place the config file in a different location than ``~/.vss/config.json``
you need to inform VSS CLI the full path. Do this by setting
the appropriate environment variable:

.. code-block:: bash

    $ export VSS_CONFIG_FILE=/path/to/config_file.json

Or use the ``-c/--config`` option in the ``vss`` command as follows:

.. code-block:: bash

    $ vss -c ~/.secret/vss-config.json

By default VSS CLI output is text, and this can be configured either by ``-o/--output``
option or the ``VSS_DEFAULT_OUTPUT`` environment variable as follows:

.. code-block:: bash

    $ export VSS_DEFAULT_OUTPUT=json
    #or
    $ export VSS_DEFAULT_OUTPUT=text

--------------------
JSON Parameter Input
--------------------

VSS CLI options vary from simple string, boolean or numeric values to
JSON data structures as input parameters on the command line.

For example, consider the following command to deploy a new virtual
machine from a given template and provide a guest operating system
specification to reconfigure hostname, domain, dns, ip, subnet
and gateway:

.. code-block:: bash

    $ vss compute vm mk from-template --source $TEMPLATE_UUID \
      --description 'New virtual machine' \
      --custom-spec '{"hostname": "fe1", "domain": "eis.utoronto.ca", "interfaces": [{"dhcp": true}]}'

Where ``$TEMPLATE_UUID`` is an environment variable storing the UUID of
the source template.


---------------
Bash completion
---------------

Bash completion support is provided by `Click`_ and will complete
sub commands and parameters. Subcommands are always listed whereas parameters
only if at least a dash has been provided. Example:

.. code-block:: bash

    $ vss compute <TAB><TAB>
    account    compute    configure  request    stor       token

    $ vss -<TAB><TAB>
     --config      --no-verbose  --output      --verbose     --version     -c            -o

Activating Bash completion can be done by executing the following command:

.. code-block:: bash

    $ eval "$(_VSS_COMPLETE=source vss)"

The above activation example will always invoke your application on startup
and may slow down the shell activation. VSS-CLI ships with a Bash completion
activation script named ``vss_bash_completer`` which can be either loaded manually
or added to your ``basrc``:

.. code-block:: bash

    $ . $(dirname `which vss`)/vss_bash_completer

---------
VSS Shell
---------

The VSS CLI provides a REPL interactive shell with tab-completion, suggestions and
command history.

.. code-block:: bash

    Usage: vss shell [OPTIONS]

      REPL interactive shell

    Options:
      -i, --history TEXT  File path to save history
      --help              Show this message and exit.

To enter the shell just execute ``vss shell`` and you will get the following welcome message:

.. code-block:: bash

        __   _____ ___
        \ \ / / __/ __|      Tab-completion & suggestions
         \ V /\__ \__ \      Prefix external commands with "!"
          \_/ |___/___/      History will be saved: /Users/vss/.vss/history
           CLI v0.2.6

        Exit shell with :exit, :q, :quit, ctrl+d

    vss >


------------
Getting Help
------------

We use GitLab issues for tracking bugs, enhancements and feature requests.
If it turns out that you may have found a bug, please `open an issue <https://gitlab-ee.eis.utoronto.ca/vss/vsscli/issues/new>`__

.. _pip: http://www.pip-installer.org/en/latest/
.. _`download the tarball`: https://pypi.python.org/pypi/vsscli
.. _`Click`: http://click.pocoo.org/6/

