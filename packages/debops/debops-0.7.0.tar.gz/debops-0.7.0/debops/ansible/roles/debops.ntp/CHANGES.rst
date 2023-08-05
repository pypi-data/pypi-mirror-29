Changelog
=========

.. include:: includes/all.rst

**debops.ntp**

This project adheres to `Semantic Versioning <http://semver.org/spec/v2.0.0.html>`__
and `human-readable changelog <http://keepachangelog.com/en/1.0.0/>`__.

The current role maintainer_ is drybjed_.


`debops.ntp master`_ - unreleased
---------------------------------

.. _debops.ntp master: https://github.com/debops/ansible-ntp/compare/v0.2.4...master


`debops.ntp v0.2.4`_ - 2017-08-24
---------------------------------

.. _debops.ntp v0.2.4: https://github.com/debops/ansible-ntp/compare/v0.2.3...v0.2.4

Changed
~~~~~~~

- Ensure that NTP daemons get uninstalled when :envvar:`ntp__daemon`
  evaluates to ``False``. [ypid_]

- Use the internal Ansible facts to detect service manager. [ipr-cnrs]


`debops.ntp v0.2.3`_ - 2016-08-29
---------------------------------

.. _debops.ntp v0.2.3: https://github.com/debops/ansible-ntp/compare/v0.2.2...v0.2.3

Added
~~~~~

- Role will not uninstall the ``ntpdate`` package automatically if
  :envvar:`ntp__ignore_ntpdate` boolean variable is enabled. [drybjed_]

Changed
~~~~~~~

- The timezone configuration tasks are moved to a separate :file:`timezone.yml`
  file for ease of use. [le9i0nx_]

Fixed
~~~~~

- Timezone should now be set correctly on hosts with ``systemd-timesyncd``
  enabled. [drybjed_]

- Fix the idempotency loop when the :file:`/etc/localtime` file is a symlink to
  a timezone file, and ``dpkg-reconfigure tzdata`` is executed. [drybjed_]


`debops.ntp v0.2.2`_ - 2016-07-28
---------------------------------

.. _debops.ntp v0.2.2: https://github.com/debops/ansible-ntp/compare/v0.2.1...v0.2.2

Changed
~~~~~~~

- Remove the ``ntp`` package before installing the ``openntpd`` package to
  avoid issues with AppArmor profiles. [thiagotalma_]

- Use the ``timedatectl`` command to set the timezone on systems with
  ``systemd-timesyncd`` enabled. [thiagotalma_]

- Update documentation and Changelog. [drybjed_]

- Use different NTP server pools for Debian and ubuntu distributions. [drybjed_]

- By default, use ``systemd-timesyncd`` on Ubuntu with ``systemd`` installed,
  to avoid issues with changing NTP servers. You can still select a different
  NTP server as usual, by specifying it using :envvar:`ntp__daemon` variable. The
  current installations won't be changed. [drybjed_]

- Move the :command:`dpkg-reconfigure` task after the NTP installation and
  configuration tasks to avoid issues with idempotency on Ubuntu. [drybjed_]

- Move the NTP daemon installation condition to a new :envvar:`ntp__daemon_enabled`
  variable and remove ``ntp__root_flags`` since they are not needed anymore.
  [drybjed_]


`debops.ntp v0.2.1`_ - 2016-05-19
---------------------------------

.. _debops.ntp v0.2.1: https://github.com/debops/ansible-ntp/compare/v0.2.0...v0.2.1

Changed
~~~~~~~

- Completed namespace change to ``ntp__`` from v0.2.0. [ypid_]


`debops.ntp v0.2.0`_ - 2016-05-19
---------------------------------

.. _debops.ntp v0.2.0: https://github.com/debops/ansible-ntp/compare/v0.1.0...v0.2.0

Added
~~~~~

- Support configuration of ``openntpd`` startup options. This is needed to add
  the ``-s`` flag so that the daemon will synchronize time immediately on
  startup if the difference is large enough. [drybjed_]

- Add support for ``system-timesyncd`` configuration. If other daemons are
  enabled, role will automatically disable the ``system-timesyncd`` service so
  that it won't interfere with normal operations. [drybjed_]

Changed
~~~~~~~

- The ``tzdata`` package is frequently updated after the Debian Stable release
  and almost always newer version will be available from ``stable-updates``
  repository. This results in frequent e-mail messages informing about updated
  ``tzdata`` package available to install. This change ensures that on first
  configuration of a host, ``tzdata`` package will be updated automatically,
  which should help ensure that mentioned e-mails won't be sent. [drybjed_]

- Configure :file:`/etc/timezone` using template.

  In Ansible v2, using ``copy`` module with ``content`` parameter is
  unreliable, since the "end of line" character is rendered directly in the
  file. Switching to ``template`` module ensures that generated configuration
  file has correct formatting and should stop generating idempotency issues
  with ``tzdata`` package configuration. [drybjed_]

- Check if NTP daemon can be installed in Ansible facts. [drybjed_]

- Changed variable namespace from ``ntp_`` to ``ntp__``.
  ``ntp_[^_]`` variables are hereby deprecated.

  You might need to update your inventory. This oneliner might come in handy to
  do this:

  .. code:: shell

     git ls-files -z | xargs --null -I '{}' find '{}' -type f -print0 | xargs --null sed --in-place --regexp-extended 's/\<(ntp)_([^_])/\1__\2/g;'

  [drybjed_]

- Update documentation. [drybjed_]


debops.ntp v0.1.0 - 2015-11-13
------------------------------

Added
~~~~~

- Add Changelog [drybjed_]

- Added support for ``ntpdate``. [ypid_]

Changed
~~~~~~~

- Uninstall conflicting packages before installing the requested ones. This
  should fix `ntp and AppArmor issue`_ present in Ubuntu. [drybjed_]

.. _ntp and Apparmor issue: https://bugs.launchpad.net/ubuntu/+source/openntpd/+bug/458061

- Fixed ``ntp_listen: '*'`` for NTPd. [ypid_]

- Rewrite the installation tasks to work correctly on Ansible v2. [drybjed_]

- Drop the dependency on debops.ferm_ Ansible role, firewall configuration
  is now defined in role default variables, and can be used by other roles
  through playbooks. [drybjed_]
