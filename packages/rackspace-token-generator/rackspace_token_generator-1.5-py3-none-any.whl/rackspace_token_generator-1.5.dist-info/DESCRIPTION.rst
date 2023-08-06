rackspace-token-generator
=========================

A script to generate authentication tokens for use with Rackspace Cloud
Identity. This was specifically created for the Rackspace Private Cloud
Insights API, though it is generally applicable to anything that needs
to be given a token.

Install
*******

To install the `get_token.py` script::

    pip install rackspace-token-generator

Run
***

The `get_token.py` script has a complete help text by running
`get_token.py -h`. The following are the most common usages::

    $ get_token.py --username <your username> --password
    Enter password: <your password>
    Token:
      <token>

    $ get_token.py --username <your username> --api-key
    Enter API key: <your API key>
    Token:
      <token>


