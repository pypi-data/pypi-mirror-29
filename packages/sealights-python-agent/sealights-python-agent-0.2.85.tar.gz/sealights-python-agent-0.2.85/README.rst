======================
sealights-python-agent
======================


The sealights-python-agent package integrates with the Sealights` Continuous Testing Platform.


****************
Language Support
****************
* Python 2.6
* Python 2.7


****************
Installation
****************

To install sealights-python-agent:
.. code-block::

    $ pip install sealights-python-agent

*****
Usage
*****

Build Scan
==========

To run the build scanner:
.. code-block::

    $ sealignts-admin --customer_id <customer_id> --app_name <app_name> --server https://prod-sealights-gw.sealights.co/api --branch <branch> --build <build> --env <env> build


1. Required
------------------
- customer_id
- app_name
- server

2. Optional
------------------
- env (default is "Unit Tests")
- build (default is "1")
- branch (default is "master")
- source - list of packages to scan (default is current working directory)
- include - Include only files whose paths match one of these patterns (default is empty)
- omit - Omit files whose paths match one of these patterns (default is empty)
 
Test Listener
=============

1. Supported Test Frameworks:
------------------------------
- unittest
- unittest2
- py.test
 
2. To run the Test Listener:
------------------------------

One Participant Mode (Tests and application on the same server)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block::

    $ sealignts-admin --customer_id <customer_id> --app_name <app_name> --server https://prod-sealights-gw.sealights.co/api --branch <branch> --build <build> --env <env> <unittest/unit2/pytest> <tests>

Multiple Participants (Tests on one server application on a second server)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    
Test Server
"""""""""""
.. code-block::

    $ sealignts-admin --test_phase <test_phase> --customer_id <customer_id> --app_name <app_name> --server https://prod-sealights-gw.sealights.co/api --branch <branch> --build <build> --env <env> <unittest/unit2/pytest> <tests>

Application Server
"""""""""""""""""""
- Run Build Scan
- Run Program using sealights-admin

.. code-block::

    $ sealignts-admin --test_phase <test_phase> --customer_id <customer_id> --app_name <app_name> --server https://prod-sealights-gw.sealights.co/api --branch <branch> --build <build> --env <env> run_program <program>
