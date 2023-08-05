Changelog
=========

.. include:: includes/all.rst

**debops.ansible_plugins**

This project adheres to `Semantic Versioning <http://semver.org/spec/v2.0.0.html>`__
and `human-readable changelog <http://keepachangelog.com/en/1.0.0/>`__.

The current role maintainer_ is drybjed_.


`debops.ansible_plugins master`_ - unreleased
---------------------------------------------

.. _debops.ansible_plugins master: https://github.com/debops/ansible-ansible_plugins/compare/v0.1.2...master


`debops.ansible_plugins v0.1.2`_ - 2017-09-03
---------------------------------------------

.. _debops.ansible_plugins v0.1.2: https://github.com/debops/ansible-ansible_plugins/compare/v0.1.1...v0.1.2

Added
~~~~~

- Allow use of ``copy_id_from`` parameter with lists of values. [drybjed_]

Changed
~~~~~~~

- When ``copy_id_from`` parameter is used, add any additional ``weight`` of
  a given entry as well. This should allow for more intuitive sorting.
  [drybjed_]


`debops.ansible_plugins v0.1.1`_ - 2017-08-21
---------------------------------------------

.. _debops.ansible_plugins v0.1.1: https://github.com/debops/ansible-ansible_plugins/compare/v0.1.0...v0.1.1

Changed
~~~~~~~

- In the DebOps filter plugins, don't add a dictionary entry with state
  ``append`` when an existing dictionary entry with state ``init`` is present.
  [drybjed_]


debops.ansible_plugins v0.1.0 - 2017-08-08
------------------------------------------

Added
~~~~~

- Initial release. [drybjed_]
