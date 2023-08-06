=================================
Nagios Plug-in Process Controller
=================================


.. image:: https://img.shields.io/pypi/v/nppc.svg
        :target: https://pypi.python.org/pypi/nppc

.. image:: https://img.shields.io/travis/maartenq/nppc.svg
        :target: https://travis-ci.org/maartenq/nppc

.. image:: https://readthedocs.org/projects/nppc/badge/?version=latest
        :target: https://nppc.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


NPPC, Nagios Plug-in Process Controller, is a set of scripts and configuration
files that let you periodically runs Nagios_ Plug-in parallel using systemd_
and systemd.timer_. Results can be posted via HTTPS to a NSCAweb_ server.

NPPC consists of:

* A wrapper around Nagios_ Plug-in that controls the output, exit status and
  time-outs to have it safely run by a systemd.timer_
* A script, systemd.service script and configuration file that creates the
  systemd.timer_ files.
* A script, systemd.timer_ and configuration file that sends periodically
  output to NSCAweb_


* Free software: https://opensource.org/licenses/ISC
* Documentation: https://nppc.readthedocs.io.
* GitHub: https://github.com/maartenq/nppc
* PyPi: https://pypi.python.org/pypi/nppc
* Travis CI: https://travis-ci.org/maartenq/nppc
* Codecov: https://codecov.io/github/maartenq/nppc


Features
--------

* Parallel execution of Nagios_ Plug-ins.
* Termination of Nagios_ Plug-ins if maximum time exceeds.
* Posts check results external commands.
* Command definition in YAML or text format.
* Configuration in YAML.
* Simple modular implementation.

Credits
-------

This package was created with Cookiecutter_ and the
`audreyr/cookiecutter-pypackage`_ project template.


References
----------

.. _systemd: https://www.freedesktop.org/software/systemd
.. _systemd.timer: https://www.freedesktop.org/software/systemd/man/systemd.timer.html
.. _NSCAweb: https://github.com/smetj/nscaweb
.. _Nagios: https://www.nagios.org/
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
