2. Edit the ``/etc/python_bsn_neutronclient/python_bsn_neutronclient.conf`` file and complete the following
   actions:

   * In the ``[database]`` section, configure database access:

     .. code-block:: ini

        [database]
        ...
        connection = mysql+pymysql://python_bsn_neutronclient:PYTHON_BSN_NEUTRONCLIENT_DBPASS@controller/python_bsn_neutronclient
