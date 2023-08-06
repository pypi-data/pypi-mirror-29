"""
OpenBanking is a wrapper for Open Banking written in Python 3.6+
----------------------------------------------------------------

Usage:

Simple usage to get discovery endpoints for ForgeRock.

    ob = openbanking
    ob.discovery_endpoints('ForgeRock')
    print(ob.content)

Or use Ozone :

    ob = openbanking
    ob.discovery_endpoints('Ozone')
    print(ob.content)


The session object allows you to persist 'some' parameters:

    ob = openbanking.Session()
    ob.bank = 'ForgeRock'
    ob.discovery_endpoints()
    print(ob.content)

# A response content, status code or log is given for every get_, post_:

    ob.content
    ob.status_code
    ob.logs

Dynamic Registration:

    claims = dict(scope='', client_id='', software_statement='')
    ob.dynamic_registration(claims, signing_key)
    print(ob.content)

or set your signing key using a the Session or one time:

    ob = openbanking.Session()
    ob.signing_key = 'path to file'
    claims = dict(scope='', client_id='', software_statement='')
    ob.post_dynamic_registration(claims)
    print(ob.content)


Full documentation @

"""

from .__version__ import __title__, __description__, __url__, __version__
from .api import discovery_endpoints, credentials
