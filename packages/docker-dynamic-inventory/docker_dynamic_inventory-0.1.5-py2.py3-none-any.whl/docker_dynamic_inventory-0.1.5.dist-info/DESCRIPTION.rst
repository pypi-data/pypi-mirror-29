========================
Docker Dynamic Inventory
========================


.. image:: https://img.shields.io/pypi/v/docker_dynamic_inventory.svg
        :target: https://pypi.python.org/pypi/docker_dynamic_inventory

.. image:: https://img.shields.io/travis/inhumantsar/docker_dynamic_inventory.svg
        :target: https://travis-ci.org/inhumantsar/docker_dynamic_inventory

.. image:: https://readthedocs.org/projects/docker-dynamic-inventory/badge/?version=latest
        :target: https://docker-dynamic-inventory.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Generates a dynamic inventory of Docker containers for Ansible.


* Free software: BSD license
* Documentation: https://docker-dynamic-inventory.readthedocs.io.


Features
--------

* Able to filter out a single host by name.
* Optionally includes Docker metadata in Ansible's hostvars.
* Optionally pretty-prints output for readability.
* Operates on the local Docker instance by default but can work with a remote host as well.
* Can be used as a Python module (if you really want to)


Usage
-----

::

  Usage: docker-dynamic-inventory [OPTIONS]

  Dynamic inventories of Docker containers, served up fresh just for
  Ansible.

  Options:
    --host TEXT                 Only match containers with this name.
    --metadata / --no-metadata  Include container metadata.
    --pretty / --ugly           Pretty print JSON for output.
    --docker_tls TEXT           Use TLS for Docker connections.
    --docker_host TEXT          Docker host to connect to.
    --help                      Show this message and exit.



Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage


=======
History
=======

0.1.0 (2018-02-23)
------------------

* First release on PyPI.


