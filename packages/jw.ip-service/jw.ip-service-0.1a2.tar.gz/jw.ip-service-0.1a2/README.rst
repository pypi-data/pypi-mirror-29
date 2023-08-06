Set IP for network interface
============================

Introduction
------------

This is a simple utility to set an IP for a network interface for as long as the utility or a sub-command is running. When it is
terminated, the IP will be removed from the network interface. This makes a network IP controllable as a service. Tools like
Nomad can then dynamically enable and disabled IPs where certain services run. If a command is specified, ip-service runs it and
waits for the program to terminate. The command would ideally provide a network-based service which would be available on the
specified IP.

Usage
-----

The program is intended to be run by the simple command like::

  ip-service -a 192.168.0.130

or::

  ip-service -a 192.168.0.130 docker start -ai myservice

positional arguments::
  command               command to run (optional)

optional arguments::
  -h, --help                        show help and exit
  --version, -V                     display version and license information
  --log-level / -L LOG_LEVEL        one of {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                                    set log level (default INFO)
  --log-file / -l LOG_FILE
                                    set log file (default: /var/log/ip-service)
  --interface / -i INTERFACE        set network interface (default: the one attached to the default route)
  --ip IP / -a IP                   IP to set (more than one possible)

Installation
------------

The software can be installed easily from the Python software repository, either on the command line or by downloading the
package and installing it explicitly.

.. note::

  Python packages should not be installed using *pip* or *easy_install* globally in the system environment under Gentoo Linux.
  There is a carefully crafted system to make system-provided Python scripts available under Python 2 as well as Python 3 which
  is disturbed by packagages deliberately installed by *pip* or *easy_install*. 

Installation using *pip*
~~~~~~~~~~~~~~~~~~~~~~~~

On the command line, type::

  pip install --user jw.ip-service

Explicit Installation from a downloaded package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Download the package from https://pypi.python.org/pypi/jw.ip-service. Unpack it, ``cd`` into the unpacked directory and type the
command::

  python setup.py install --user

Bug reports
-----------

Please report bugs and enhancement requests to https://bitbucket.org/JohnnyWezel/jw.ip-service/issues.
