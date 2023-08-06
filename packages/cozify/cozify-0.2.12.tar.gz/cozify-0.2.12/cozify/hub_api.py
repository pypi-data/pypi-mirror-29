"""Module for all Cozify Hub API 1:1 calls

Attributes:
    apiPath(str): Hub API endpoint path including version. Things may suddenly stop working if a software update increases the API version on the Hub. Incrementing this value until things work will get you by until a new version is published.
"""

import requests, json, logging

from cozify import cloud_api

from .Error import APIError
from requests.exceptions import RequestException

apiPath = '/cc/1.8'

def _getBase(host, port=8893, api=apiPath):
    return 'http://%s:%s%s' % (host, port, api)

def _headers(hub_token):
    return { 'Authorization': hub_token }

def get(call, hub_token_header=True, base=apiPath, **kwargs):
    """GET method for calling hub API.

    Args:
        call(str): API path to call after apiPath, needs to include leading /.
        hub_token_header(bool): Set to False to omit hub_token usage in call headers.
        base(str): Base path to call from API instead of global apiPath. Defaults to apiPath.
        **host(str): ip address or hostname of hub.
        **hub_token(str): Hub authentication token.
        **remote(bool): If call is to be local or remote (bounced via cloud).
        **cloud_token(str): Cloud authentication token. Only needed if remote = True.
    """
    return _call(method=requests.get,
            call=call,
            hub_token_header=hub_token_header,
            base=base,
            **kwargs
            )

def put(call, payload, hub_token_header=True, base=apiPath, **kwargs):
    """PUT method for calling hub API. For rest of kwargs parameters see get()

    Args:
        call(str): API path to call after apiPath, needs to include leading /.
        payload(str): json string to push out as the payload.
        hub_token_header(bool): Set to False to omit hub_token usage in call headers.
        base(str): Base path to call from API instead of global apiPath. Defaults to apiPath.
    """
    return _call(method=requests.put,
            call=call,
            hub_token_header=hub_token_header,
            base=base,
            payload=payload,
            **kwargs
            )

def _call(*, call, method, base, hub_token_header, payload=None, **kwargs):
    """Backend for get & put
    """
    response = None
    headers = None
    if hub_token_header:
        headers = _headers(kwargs['hub_token'])

    if kwargs['remote']: # remote call
        if 'cloud_token' not in kwargs:
            raise AttributeError('Asked to do remote call but no cloud_token provided.')
        logging.debug('_call routing to cloud.remote()')
        response = cloud_api.remote(apicall=base + call, payload=payload, **kwargs)
    else: # local call
        if not kwargs['host']:
            raise AttributeError('Local call but no hostname was provided. Either set keyword remote or host.')
        if hub_token_header:
            headers = _headers(kwargs['hub_token'])
        try:
            response = method(_getBase(host=kwargs['host'], api=base) + call, headers=headers, data=payload)
        except RequestException as e:
            raise APIError('connection failure', 'issues connection to \'{0}\': {1}'.format(kwargs['host'], e))

    # evaluate response, wether it was remote or local
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 410:
        raise APIError(response.status_code, 'API version outdated. Update python-cozify. %s - %s - %s' % (response.reason, response.url, response.text))
    else:
        raise APIError(response.status_code, '%s - %s - %s' % (response.reason, response.url, response.text))

def hub(**kwargs):
    """1:1 implementation of /hub API call. For kwargs see cozify.hub_api.get()

    Returns:
        dict: Hub state dict.
    """
    return get('hub', base='/', hub_token_header=False, **kwargs)

def tz(**kwargs):
    """1:1 implementation of /hub/tz API call. For kwargs see cozify.hub_api.get()

    Returns:
        str: Timezone of the hub, for example: 'Europe/Helsinki'
    """
    return get('/hub/tz', **kwargs)

def devices(**kwargs):
    """1:1 implementation of /devices API call. For remaining kwargs see cozify.hub_api.get()

    Args:
        **mock_devices(dict): If defined, returned as-is as if that were the result we received.

    Returns:
        dict: Full live device state as returned by the API
    """
    if 'mock_devices' in kwargs:
        return kwargs['mock_devices']

    return get('/devices', **kwargs)

def devices_command(command, **kwargs):
    """1:1 implementation of /devices/command. For kwargs see cozify.hub_api.put()

    Args:
        command(dict): dictionary of type DeviceData containing the changes wanted. Will be converted to json.

    Returns:
        str: What ever the API replied or an APIException on failure.
    """
    command = json.dumps(command)
    logging.debug('command json to send: {0}'.format(command))
    return put('/devices/command', command, **kwargs)
