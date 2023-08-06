Argus Toolbelt
====================================================================================
Argus has, for a long time, had a large number of separate "tools", or python scripts,
used to interact with the API and perform a number of different tasks - some automated,
and some not so automated. 

Toolbelt provides a framework to unify tools like these under one command. building commandline tools with Argus' API.
This is done via a plugin approach.

We aim to make it as simple as possible for developers to write and run their plugins
without having to deal with authentication, HTTP requests, argument handling and 
commandline formatting.


Installation
-----------------------------------------------------------------------------------
To install the framework run `pip install argus-toolbelt`.
This will install 3 packages to your python install and
start a setup that creates the settings-file required by *argus_cli*.

The packages installed are:

- *argus_api*: Generates and provides functions for communicating with Argus API
- *argus_cli*: Provides a standardized framework for writing commandline scripts that interact with Argus
- *argus_plugins*: Default set of plugins loaded by `argus_cli`, and instructions on how to add your own

The setup script can be run at any time by running `toolbelt-setup`.
This script should be in your `PATH` after installation.


Usage
-----------------------------------------------------------------------------------
After the script is installed it can be run as `argus-cli` anywhere on the system.
The syntax for running a command is `argus-cli <plugin> <command> [arguments]`

If you for example want to check statistics for all cases, you can write: `argus-cli cases statistics`,
but for a full list of commands, try `argus-cli --help`
