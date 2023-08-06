import logging
import requests
import facturacom

LOG = logging.getLogger(__name__)

class ApiWrapper(object):
    """
    Wrapper for API calls
    """
    def __init__(self):
        pass

    @staticmethod
    def api_call(endpoint, data, method='GET', file=False):
        """
        Makes api call
        @param method: type of REST request
        @param endpoint: endpoint to which generate the request
        @param data: payload for request
        """
        headers = {
            'Content-Type': 'application/json',
            'F-API-KEY': facturacom.FACTURACOM_API_KEY,
            'F-SECRET-KEY': facturacom.FACTURACOM_SECRET_KEY,
        }
        url = ApiWrapper.get_url(endpoint)
        if method.lower() == 'post':
            req = requests.post(url, json=data, headers=headers)
        else:
            req = requests.get(url, params=data, headers=headers)

        LOG.debug(req)
        if req.status_code >= 400:
            return req
        elif req.status_code <= 299 and file:
            return req
        else:
            return req.json()

    @staticmethod
    def get_url(endpoint):
        """
        Generates url for API requests
        @param endpoint: endpoint to construct url
        """
        host = facturacom.FACTURACOM_PRODUCTION
        if facturacom.DEBUG:
            host = facturacom.FACTURACOM_SANDBOX

        return "{0}{1}{2}".format(
            host,
            facturacom.FACTURACOM_NAMESPACE,
            endpoint
        )
