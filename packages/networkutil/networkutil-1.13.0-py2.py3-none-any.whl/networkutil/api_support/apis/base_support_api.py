# -*- coding: utf-8 -*-

import json
import requests
import urllib
import webbrowser
import logging_helper
from classutils.api_support import JsonApiRequestResponse
from classutils.observer import Observer
from networkutil.web_socket import WebSocketSubscriber
from timingsutil.timers import Timeout, SECOND
from .._exceptions import APIError, APIMissing, APIUnresponsive

logging = logging_helper.setup_logging()


class BaseSupportApi(Observer):

    # PATH must be defined in subclass for versioned api's
    PATH = u''

    ALLOW_REDIRECTS = True  # Note: does not apply to websockets currently!

    # Request timeout settings
    TIMEOUT_MULTIPLIER = 1
    LONG_TIMEOUT = 1
    MEDIUM_TIMEOUT = 0.5
    SHORT_TIMEOUT = 0.1
    # Note minimum timeout will be SHORT_TIMEOUT * TIMEOUT_MULTIPLIER.

    # Custom Exceptions (DO NOT OVERRIDE exceptions here, these will be set by api_support_layer)
    API_ERROR = APIError
    MISSING_API = APIMissing
    UNRESPONSIVE_API = APIUnresponsive

    def __init__(self,
                 api_root,
                 *args,
                 **kwargs):  # args & kwargs provided here to sink any extra params that get passed to the api

        self._api_root = api_root

        self.last_request = None
        self._websockets = {}
        self._ws_notifications = {}

    @property
    def api_path(self):
        api_parts = [self._api_root]

        if self.PATH:
            api_parts.append(self.PATH)

        return u'/'.join(api_parts)


    @staticmethod
    def merge_request_parameters(quote=False,
                                 parameters=None,
                                 **additional_parameters):
        """
        Helper function to requesters to easily combine a
        dictionary of parameters and additional parameters
        supplied as keyword values

        Note: If the request itself takes a parameter called
              'parameters', it must be supplied inside
              a dict.
              i.e. parameters={u'parameters': <parameters values')

        :param quote: bool : Set to True to use urllib.quote
                              default False allows requests to
                              use the standard quote_plus encoding
        :param parameters: dict
        :param additional_parameters:
        :return: dict
        """
        merged_params = {}

        if parameters:
            merged_params.update(parameters)

        for param_name, param_value in iter(additional_parameters.items()):
            if param_name in merged_params:
                try:
                    merged_params[param_name].append(param_value)
                except AttributeError:
                    merged_params[param_name] = [merged_params[param_name],
                                                         param_value]
            else:
                merged_params[param_name] = param_value

        if not quote or not merged_params:
            return merged_params

        param_parts = []
        for param_name, param_value in iter(merged_params.items()):
            if isinstance(param_value, (list, tuple)):
                for field in param_value:
                    if param_value is None:
                        continue
                    try:
                        param_parts.append(u'{n}={v}'
                                           .format(n=param_name,
                                                   v=urllib.quote(field)))
                    except AttributeError:
                        param_parts.append(u'{n}={v}'
                                           .format(n=param_name,
                                                   v=field))
            elif param_value is None:
                continue
            else:
                try:
                    param_parts.append(u'{n}={v}'
                                       .format(n=param_name,
                                               v=urllib.quote(param_value)))
                except AttributeError:
                    param_parts.append(u'{n}={v}'
                                       .format(n=param_name,
                                               v=param_value))

        return u'&'.join(param_parts)

    def make_request(self,
                     method,
                     request,
                     data=None,
                     timeout=None,
                     in_browser=False,
                     request_params=None,
                     headers=None):

        request = u'http://{api}/{request}'.format(api=self.api_path,
                                                   request=request)

        self.last_request = request

        logging.debug(u'{method}:{request}'.format(method=method,
                                                   request=request))
        if in_browser:
            webbrowser.open_new_tab(request)

        headers = headers if headers else {}

        headers.update({u'Content-Type': u'text/plain; charset=utf-8'})

        params = dict(url=request,
                      headers=headers,
                      allow_redirects=self.ALLOW_REDIRECTS)

        if request_params is not None:
            params[u'params'] = request_params

        if timeout is not None:
            params[u'timeout'] = timeout * self.TIMEOUT_MULTIPLIER

        if timeout is None or params[u'timeout'] < self.SHORT_TIMEOUT:
            params[u'timeout'] = self.SHORT_TIMEOUT * self.TIMEOUT_MULTIPLIER

        try:
            if method.upper() == u'GET':
                # response = requests.get(request, headers = headers)
                response = requests.get(**params)
                response.encoding = u'utf-8'

            elif method.upper() == u'POST':
                if data is not None:
                    # TODO: Future edge cases: body might not be JSON/might already be a string
                    params[u'data'] = json.dumps(data)
                    params[u'headers'] = {u'Content-type': u'application/json',
                                          u'Accept': u'text/plain'}

                response = requests.post(**params)
                response.encoding = u'utf-8'

            else:
                return None

        except (requests.ConnectionError, requests.exceptions.ReadTimeout) as e:
            logging.exception(e)
            raise self.UNRESPONSIVE_API(request)

        logging.debug(u'Response Code: {rc}'.format(rc=response.status_code))

        if 200 > int(response.status_code) >= 300:
            raise self.API_ERROR(u'API Request Failed: {req}'.format(req=request),
                                 response=response)

        return JsonApiRequestResponse(request=request,
                                      response=response)

    def get(self,
            # request,
            # timeout=None,
            # in_browser=False
            *args,
            **kwargs):
        return self.make_request(method=u'GET',
                                 *args,
                                 **kwargs)

    def post(self,
             # request,
             # data=None,
             # timeout=None
             *args,
             **kwargs):
        return self.make_request(method=u'POST',
                                 *args,
                                 **kwargs)

    def ws_request(self,
                   request,
                   notify_function=None):

        logging.debug(self._websockets)

        if request not in self._websockets:
            request_url = (u'ws://{api}/{request}'.format(api=self.api_path,
                                                          request=request))
            logging.debug(u'Request: {r}'.format(r=request_url))

            self.last_request = request_url

            # Register requests notify function if provided
            if notify_function is not None:
                self._register_notification(request=request,
                                            notify_function=notify_function)

            # Setup websocket
            self._websockets[request] = WebSocketSubscriber(request=request_url,
                                                            name=request)
            self._websockets[request].register_observer(self)

            # Wait very short time for last_message to be updated
            timer = Timeout(SECOND)

            while not timer.expired and self._websockets[request].last_message is None:
                pass

        # Return last message on the websocket to match existing functionality
        return self._websockets[request].last_message

    def notification(self,
                     **kwargs):

        # If we have ws_name, lookup correct notification method and send notification
        if WebSocketSubscriber.WS_NAME in kwargs:
            request = kwargs[WebSocketSubscriber.WS_NAME]

            if request in self._ws_notifications:
                self._ws_notifications[request](**kwargs)

        # If websocket closes, unregister observation of websocket
        if WebSocketSubscriber.WS_STATE in kwargs:
            if kwargs[WebSocketSubscriber.WS_STATE] == WebSocketSubscriber.WS_CLOSED:
                kwargs[self.NOTIFIER_KEY].unregister_observer(self)

                if kwargs[self.NOTIFIER_KEY].name in self._ws_notifications:
                    del self._ws_notifications[kwargs[self.NOTIFIER_KEY].name]

    def _register_notification(self,
                               request,
                               notify_function):
        self._ws_notifications[request] = notify_function

    def close(self):
        for ws in list(self._websockets.keys()):
            self._websockets[ws].close()
            del self._websockets[ws]

    def __del__(self):
        self.close()
