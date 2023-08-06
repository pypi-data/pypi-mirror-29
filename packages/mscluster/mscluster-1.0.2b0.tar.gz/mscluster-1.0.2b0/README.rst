Python module for Windows Server Failover Clustering
=====

This module manage the Windows Server Failover Clustering using the Windows API.

Features
--------
* List cluster nodes, resources and group
* Get node, resource and group status
* Move group between nodes
* Start and stop resources and group

Install
--------
::

    pip install pymscluster`

Example
--------
.. code-block:: python

    import mscluster
    c = mscluster.Cluster("Cluster address")
    
    # Print group list
    print(list(c.groups))
    
    r = c.openResource("Resource name")
    r.takeOffline()
    t.takeOnline()
