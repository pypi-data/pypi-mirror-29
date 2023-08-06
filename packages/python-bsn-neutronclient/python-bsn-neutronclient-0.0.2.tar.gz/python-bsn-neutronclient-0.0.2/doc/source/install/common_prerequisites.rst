Prerequisites
-------------

Before you install and configure the python_bsn_neutronclient service,
you must create a database, service credentials, and API endpoints.

#. To create the database, complete these steps:

   * Use the database access client to connect to the database
     server as the ``root`` user:

     .. code-block:: console

        $ mysql -u root -p

   * Create the ``python_bsn_neutronclient`` database:

     .. code-block:: none

        CREATE DATABASE python_bsn_neutronclient;

   * Grant proper access to the ``python_bsn_neutronclient`` database:

     .. code-block:: none

        GRANT ALL PRIVILEGES ON python_bsn_neutronclient.* TO 'python_bsn_neutronclient'@'localhost' \
          IDENTIFIED BY 'PYTHON_BSN_NEUTRONCLIENT_DBPASS';
        GRANT ALL PRIVILEGES ON python_bsn_neutronclient.* TO 'python_bsn_neutronclient'@'%' \
          IDENTIFIED BY 'PYTHON_BSN_NEUTRONCLIENT_DBPASS';

     Replace ``PYTHON_BSN_NEUTRONCLIENT_DBPASS`` with a suitable password.

   * Exit the database access client.

     .. code-block:: none

        exit;

#. Source the ``admin`` credentials to gain access to
   admin-only CLI commands:

   .. code-block:: console

      $ . admin-openrc

#. To create the service credentials, complete these steps:

   * Create the ``python_bsn_neutronclient`` user:

     .. code-block:: console

        $ openstack user create --domain default --password-prompt python_bsn_neutronclient

   * Add the ``admin`` role to the ``python_bsn_neutronclient`` user:

     .. code-block:: console

        $ openstack role add --project service --user python_bsn_neutronclient admin

   * Create the python_bsn_neutronclient service entities:

     .. code-block:: console

        $ openstack service create --name python_bsn_neutronclient --description "python_bsn_neutronclient" python_bsn_neutronclient

#. Create the python_bsn_neutronclient service API endpoints:

   .. code-block:: console

      $ openstack endpoint create --region RegionOne \
        python_bsn_neutronclient public http://controller:XXXX/vY/%\(tenant_id\)s
      $ openstack endpoint create --region RegionOne \
        python_bsn_neutronclient internal http://controller:XXXX/vY/%\(tenant_id\)s
      $ openstack endpoint create --region RegionOne \
        python_bsn_neutronclient admin http://controller:XXXX/vY/%\(tenant_id\)s
