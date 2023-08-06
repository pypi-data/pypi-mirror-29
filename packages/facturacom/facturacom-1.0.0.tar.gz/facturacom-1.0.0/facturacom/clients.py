import logging
from facturacom.api_wrapper import ApiWrapper

LOG = logging.getLogger(__name__)

class Clients(object):
    """
    Manage clients from endpoints
    """
    def __init__(self):
        pass

    @staticmethod
    def list_all():
        """
        Get all Clients
        """
        return ApiWrapper.api_call('/v1/clients', dict())

    @staticmethod
    def find(rfc):
        """
        Gets single client from api
        """
        return ApiWrapper.api_call('/v1/clients/%s' % rfc, dict())

    @staticmethod
    def create(data):
        """
        Creates client from api
        """
        return ApiWrapper.api_call('/v1/clients/create', data, 'POST')

    @staticmethod
    def update(uid, data):
        """
        Updates client from api
        """
        return ApiWrapper.api_call('/v1/clients/%s/update' % uid, data, 'POST')
