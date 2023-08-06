class OpenBankingBaseError(Exception):
    """Base class for all Open Banking errors."""
    pass


class ConfigurationException(OpenBankingBaseError):
    pass

class UnsupportedException(OpenBankingBaseError):
    pass
