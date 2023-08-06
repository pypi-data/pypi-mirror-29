MondialRelay
============

Python API MondialRelay carrier.

Features
--------

- Services
- Test connection
- Create/Send shipments to MondialRelay
- Label shipment - PDF

Usage Examples
--------------

Example API in test.py file

Test connection
---------------

.. code-block:: python

    with Picking(username, password, mondialrelay_customerid,
            debug=debug) as mondialrelay_api:
        print mondialrelay_api.test_connection()

Create/send shipment to MondialRelay
------------------------------------

.. code-block:: python

    with Picking(username, password, mondialrelay_customerid,
            debug=debug) as mondialrelay_api:
        data = {...}
        reference, label, error = mondialrelay_api.create(data)

Get label shipment
------------------

.. code-block:: python

    with Picking(username, password, mondialrelay_customerid,
            debug=debug) as mondialrelay_api:
        data = {...}
        label = mondialrelay_api.label(data)


