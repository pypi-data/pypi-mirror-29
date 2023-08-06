import time
import requests
from werkzeug.contrib.cache import SimpleCache
# Application Libs
from .config import model_banks
from .exceptions import ConfigurationException, UnsupportedException


class Session(object):
    """
    A session stores configuration state.
    """

    def __init__(self, bank=None):

        self.header = "test"
        self.bank = bank

        self._response = None
        self._status_code = None

        # if self.bank:
        #     self._set_endpoint_properties(bank)


    @property
    def response(self):
        return self._response

    @property
    def status_code(self):
        return self._status_code

    @staticmethod
    def _load_config_for_bank(bank_name: str) -> dict:
        """Returns a dictionary configuration for a particular Bank."""

        banks = [bank for bank in model_banks if bank['name'] == bank_name]

        if len(banks) != 1:
            raise ConfigurationException("Could not load bank configuration for {}.".format(bank_name))
        return banks[0]

    # def _set_endpoint_properties(self, bank):
    #     """Sets the discovery endpoint urls as properties."""
    #     if not bank:
    #         bank = self.bank
    #     for item in self.discovery_endpoints(bank):
    #         print(item)



    def get_config_args(self, bank: str, key: str) -> str:
        """Return a value from config."""
        bank_config = self._load_config_for_bank(bank)
        return bank_config.get(key, None)

    def discovery_endpoints(self, bank=None):
        """
        Return discovery endpoint for a chosen back.

        :param bank: str, optional if configured during initialisation.
        :return: class:`~openbanking.session.Session`
        """
        if not bank:
            bank = self.bank
        url = self.get_config_args(bank, "discovery_endpoint")
        if not url:
            raise UnsupportedException()
        self._make_request('get', url, verify=False)

        return self

    def well_known(self, bank=None):
        """
        Return well known endpoint for a chosen bank.

        :param bank: str, optional if configured during initialisation.
        :return: class:`~openbanking.session.Session`
        """
        if not bank:
            bank = self.bank
        url = self.get_config_args(bank, "well_known")
        self._make_request('get', url, verify=False)

        return self

    def _make_request(self, method, url, verify=True):
        """
        Using Requests, make a HTTP call and record the response and status codes.
        :param method: the method i.e. get, post, delete.
        :param url: the resource url.
        :param verify: (optional), boolean, controls whether we verify the server's TLS certificate. Defaults to True.
        :return:
        """
        r = requests.get(url, verify=verify, )
        # set the response regardless or errors
        self._response = r.json()
        self._status_code = r.status_code




