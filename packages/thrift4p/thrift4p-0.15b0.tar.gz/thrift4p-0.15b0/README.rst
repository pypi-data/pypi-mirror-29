========
thrift4p
========

Installation
============

Install with pip.

.. code:: bash

    $ pip install thrift4p
    
Code Demo
=========

.. code:: python

	from thrift4p import generate_client_from_zk
	
	client = generate_client_from_zk("com.didapinche.thrift.dm.hub.holder.DmOperationHubService","ip1:port1,ip2:port2")
