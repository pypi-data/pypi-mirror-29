.. _install-obs:


Install and configure for openSUSE and SUSE Linux Enterprise
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section describes how to install and configure the python_bsn_neutronclient service
for openSUSE Leap 42.1 and SUSE Linux Enterprise Server 12 SP1.

.. include:: common_prerequisites.rst

Install and configure components
--------------------------------

#. Install the packages:

   .. code-block:: console

      # zypper --quiet --non-interactive install

.. include:: common_configure.rst


Finalize installation
---------------------

Start the python_bsn_neutronclient services and configure them to start when
the system boots:

.. code-block:: console

   # systemctl enable openstack-python_bsn_neutronclient-api.service

   # systemctl start openstack-python_bsn_neutronclient-api.service
