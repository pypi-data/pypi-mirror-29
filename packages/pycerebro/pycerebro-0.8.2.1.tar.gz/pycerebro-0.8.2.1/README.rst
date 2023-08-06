pycerebro
=========

Python client for RecordService implementations.

Dependencies
------------

Required:

-  Python 3.4+

-  ``six``, ``bit_array``, ``thriftpy >=0.3.9``

.. code:: shell

    pip3 install six bit_array 'thriftpy>=0.3.9'

Optional:

-  ``pandas`` for conversion to ``DataFrame`` objects

Installation
------------

.. code:: shell

    pip3 install pycerebro

To verify:

.. code:: python

    >>> import cerebro.cdas
    >>> cerebro.cdas.version()
    '0.8.0-beta3'

Usage
~~~~~

.. code:: python

    from cerebro import create_context, scan_as_pandas
    ctx = create_context()
    with ctx.connect_planner(host='localhost', port=12050) as planner:
        planner.list_databases()
        pd = scan_as_pandas(planner, "cerebro_sample.sample")
        pd

To enable a connection to a server with token-authentication:

.. code:: python

    from cerebro import create_context
    ctx = create_context()
    ctx.enable_token_auth(token_str='my-token')
    with ctx.connect_planner(host='localhost', port=12050) as planner:
        planner.list_databases()

To enable a connection to a server with kerberos-authentication:

.. code:: python

    from cerebro import create_context
    ctx = create_context()
    # Connecting to server principal 'cerebro/service@REALM'
    ctx.enable_kerberos('cerebro', host_override='service')
    with ctx.connect_planner(host='localhost', port=12050) as planner:
        planner.list_databases()
