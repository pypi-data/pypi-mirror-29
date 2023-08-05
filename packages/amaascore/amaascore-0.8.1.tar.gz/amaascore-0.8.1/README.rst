=========================
AMaaS Core SDK for Python
=========================

This is the Asset Management as a Service (AMaaS) Software Development Kit (SDK)
for Python.

What is AMaaS?
--------------
AMaaS is a modular platform for Asset Managers with an open, RESTful API for programmatic access to its functionality.


AMaaS Core features a secure, encrypted database, which serves as the foundation for asset management platforms and
FinTech solutions. AMaaS also provides portfolio visualizations and analytics through AMaaS Web, and exception
management & financial event notification through AMaaS Monitor.

Quick Start
-----------
Install the AMaaS Core library from PyPI:

.. code-block:: sh

    $ pip install amaascore

This module can then be immediately embedded into your Python applications to take advantage of the standardised class
structure.  In order to fully utilise the power of the AMaaS platform, sign-up for an account at http://www.amaas.com/.

Once you have your credentials, generate your API key by following these instructions:

* Currently this can only be done with help from support@amaas.com

Configuring Credentials
-----------------------
When calling the AMaaS APIs, the AMaaS Core library will search for your credentials from different locations.  The order in which credentials are searched are as follows:

1. Credentials passed in the AMaaS API Interface constructors
2. Environment variables
3. AMaaS configuration file (~/.amaas.cfg) [Recommended]

Constructor Parameter
---------------------
.. code-block:: python

    assets_interface = AssetsInterface(username='myusername', password='mypassword')
Environment Variables
---------------------
The AMaaS Core library will check these environment variables for your credentials

- AMAAS_USERNAME
- AMAAS_PASSWORD
AMaaS configuration file
------------------------
This is the recommended way of configuring your credentials. Create a file called .amaas.cfg in your homedir, with the following:

.. code-block:: none

    [auth]
    username=YOUR_USERNAME
    password=YOUR_PASSWORD

Note that the password is never transferred across the wire as AMaaS uses the Secure Remote Password protocol:
https://en.wikipedia.org/wiki/Secure_Remote_Password_protocol


Example code and demonstrations
-------------------------------
For examples of how the Python SDK can be used, clone the "AMaaS Core SDK for Python Examples" repository from:
https://github.com/amaas-fintech/amaas-core-sdk-python-examples.

A variety of demos are available such as:

  * Book a set of transactions and then view the cumulative position
  * Back-dated transaction handling
  * Signup clients and then book ETFs on their behalf, while managing their cash
  * A simulation of a simplified robo-advisor

Testing
-------
The SDK contains wide-ranging unit tests within the AMaaS Core package itself.  The easiest way to run the whole suite
is to install tox, then run it from the root directory (where the tox.ini file resides).

.. code-block:: sh

    $ pip install tox
    $ tox

Individual test modules can be run using unittest in the usual fashion.

API Documentation
-----------------
The complete API documentation can be found at: TBD.

Support
-------
For support with the SDKs, please raise issues on GitHub.  The AMaaS team can be contacted at support@amaas.com.
Customers who have purchased a support plan can find the contact details within AMaaS Admin.
