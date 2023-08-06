import logging
import os
from io import BytesIO
from tempfile import NamedTemporaryFile
from facturacom.api_wrapper import ApiWrapper

LOG = logging.getLogger(__name__)

class Cfdi(object):
    """
    Manage cfdi from endpoints
    """
    def __init__(self):
        pass

    @staticmethod
    def list_all():
        """
        Get all cfdi's
        """
        return ApiWrapper.api_call('/v3/cfdi33/list', dict())

    @staticmethod
    def create(data):
        """
        Creates cfdi from api
        """
        return ApiWrapper.api_call('/v3/cfdi33/create', data, 'POST')

    @staticmethod
    def cancel(uid):
        """
        Cancels cfdi from api
        """
        return ApiWrapper.api_call('/v3/cfdi33/%s/cancel' % uid, dict())

    @staticmethod
    def xml(uid):
        """
        Downloads xml cfdi from api
        """
        request = ApiWrapper.api_call('/v3/cfdi33/%s/xml' % uid, dict(), file=True)
        with NamedTemporaryFile(
            prefix='%s_' % uid,
            suffix='.xml',
            delete=False
        ) as temp:
            temp.write(request.content)

            return temp

    @staticmethod
    def pdf(uid):
        """
        Downloads pdf cfdi from api
        """
        request = ApiWrapper.api_call('/v3/cfdi33/%s/pdf' % uid, dict(), file=True)
        with NamedTemporaryFile(
            prefix='%s_' % uid,
            suffix='.pdf',
            delete=False
        ) as temp:
            temp.write(request.content)

            return temp
