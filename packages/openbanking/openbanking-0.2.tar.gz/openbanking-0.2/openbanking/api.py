from .session import Session

DEFAULT_SESSION = None


def setup_default_session(**kwargs):
    """
    Set up a default session, passing through any parameters to the session
    constructor. There is no need to call this unless you wish to pass custom
    parameters, because a default session will be created for you.
    """
    global DEFAULT_SESSION
    bank = kwargs.pop('bank', None)
    DEFAULT_SESSION = Session(bank)


def _get_default_session(force=False, **kwargs):
    """
    Create a new Session instance or create a new one.

    :param force: flag used to force the a new Session instance.
    :param kwargs:
    :return:class:`~openbanking.session.Session` The default session.
    """
    if DEFAULT_SESSION is None or force:
        setup_default_session(**kwargs)
    return DEFAULT_SESSION


def credentials(**kwargs):
    """
    Set credentials, init instance vars etc.
    :param kwargs:
    :return:
    """
    return _get_default_session(force=True, **kwargs)


def discovery_endpoints(bank=None):
    """
    Returns 'Discovery Endpoints" for specified Bank.

    Example usage:

        Get discovery endpoint for 'ForgeRock' without a configuration setup:

        > import openbanking
        > ob = openbanking
        > r = ob.discovery_endpoints('ForgeRock')
        > print(r.response)
        > print (r.status_code)

        Get discovery endpoint for Ozone using a configuration setup:

        > ob = openbanking
        > ob.config(bank="Ozone")
        > r = ob.discovery_endpoints()
        > print(r.response)
        > print (r.status_code)

    :param bank:
    :return: class:`~openbanking.session.Session` The default session.
    """
    return _get_default_session().discovery_endpoints(bank)


def well_known(bank=None):
    """
    Returns Well Known endpoints for a specified Bank.

    Example usage:

        > import openbanking
        > ob = openbanking
        > ob.config(bank="ForgeRock")
        > r = ob.discovery_endpoints()
        > print(r.response)
        > print(r.status_code)

    :param bank:
    :return: class:`~openbanking.session.Session` The default session.
    """
    return _get_default_session().well_known(bank)
