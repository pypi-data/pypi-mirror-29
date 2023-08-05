pyinfra
=======

|PyPI version| |Travis.CI status|

pyinfra manages the state of one or more servers. It can be used for
app/service deployment, config management and ad-hoc command execution.
Deploys are asynchronous, highly performant and can target thousands of
hosts in parallel. The inventory of servers and deploy state are written
in Python, allowing for near-infinite extendability. pyinfra is
available via the command line and as a Python API.

-  `Getting
   started <https://pyinfra.readthedocs.org/page/getting_started.html>`__
-  `Documentation <https://pyinfra.readthedocs.org>`__
-  `Example deploy <example>`__
-  `API
   Example <https://pyinfra.readthedocs.org/page/api/example.html>`__
-  `How the deploy
   works <https://pyinfra.readthedocs.org/page/deploy_process.html>`__

|image2|

Design Features
---------------

pyinfra was designed to enable us to deploy things in a consistent,
debuggable and maintainable manner. Notable design decisions:

-  properly agentless - even Python isn’t required on the remote side
   (just a shell!)
-  always print raw stderr on operation failure for *instant* debugging
-  ``-v`` means print out remote stdout & stderr in realtime
-  outputs shell commands and files to upload
-  two-step deploy that enables dry-runs
-  fail fast where possible (eg touching a directory)
-  uses pure, 100% Python for the inventory and deploy scripts

   -  with operations/hooks to safely use Python mid-deploy

.. |PyPI version| image:: https://badge.fury.io/py/pyinfra.svg
   :target: https://pypi.python.org/pypi/pyinfra
.. |Travis.CI status| image:: https://travis-ci.org/Fizzadar/pyinfra.svg?branch=develop
   :target: https://travis-ci.org/Fizzadar/pyinfra
.. |image2| image:: docs/example_deploy.png



