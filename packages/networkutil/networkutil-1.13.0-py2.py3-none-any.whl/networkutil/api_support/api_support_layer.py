# encoding: utf-8

import logging_helper
from ._exceptions import APIError, APIMissing, APIUnresponsive

logging = logging_helper.setup_logging()


class APISupportLayer(object):

    """ Base class that provides a common interface to versioned HTTP / WS API's.
        Create one Versioned API support per host:port combination.
    """

    APIS = []  # List of api modules to make available as part of this support layer (must be populated by subclass)

    DEFAULT_PORT = 443  # Assume HTTPS unless told otherwise
    PATH_PREFIX = u''

    # Custom Exceptions
    API_ERROR = APIError
    MISSING_API = APIMissing
    UNRESPONSIVE_API = APIUnresponsive

    def __init__(self,
                 host,
                 port=None,
                 path_prefix=None,
                 active_api_versions=None):
        """
        :param host:
        :param port:
        :param path_prefix:
        :param active_api_versions: Dictionary of API name to version number.
                                    This will override the latest and fallback
                                    versions.
        """

        if port is None:
            try:
                host, port = host.split(u':')
            except ValueError:
                port = self.DEFAULT_PORT

        if path_prefix is None:
            path_prefix = self.PATH_PREFIX

        # API Root components
        self._host = host
        self._port = port
        self._path_prefix = path_prefix

        self._apis = {}
        self._api_versions = {}
        self._api_mappings = {}
        self._active_api_versions = active_api_versions if active_api_versions else {}
        self.api_parameters = dict(api_root=self.api_root)

        self._load_apis()

    @property
    def api_root(self):
        api_parts = [u'{host}:{port}'.format(host=self._host,
                                             port=self._port)]

        if self._path_prefix:
            api_parts.append(self._path_prefix)

        return u'/'.join(api_parts)

    def _load_apis(self):
        for api in self.APIS:
            # Register the API
            self.add_api(api.NAME, api.VERSIONS)

            # Pass on exception classes of the API layer to the API
            api.API_ERROR = self.API_ERROR
            api.MISSING_API = self.MISSING_API
            api.UNRESPONSIVE_API = self.UNRESPONSIVE_API

    def add_api(self,
                api,
                versions):

        if api in self._api_mappings:
            logging.warning(u'API {api} already registered, Updating API registration'.format(api=api))

        self._api_mappings[api] = versions

    def available_apis(self):
        return self._api_mappings.keys()

    def available_api_versions(self,
                               api):
        return self._api_mappings[api].keys()

    def _get_api_version(self,
                         api):

        """ Implement in subclass for a versioned API.
            If this is not overridden then all API's will get a version = 0

        This method is used to determine the current API version for a specific api.

        :param api: The api to get the version for.
        :return:    The current version number for the API.
                    return 0 if no version found or API is un-versioned.
        """

        return 0

    def api_version(self,
                    api):

        """ This method is used to determine the current API version for a specific api.

        DO NOT OVERRIDE

        :param api: The api to get the version for.
        :return:    The current version number for the API.
                    return 0 if no version found or API is un-versioned.
        """

        try:
            return self._api_versions[api]

        except KeyError:
            pass

        self._api_versions[api] = self._active_api_versions.get(api, self._get_api_version(api))

        return self._api_versions[api]

    def api(self,
            api,
            **params):

        try:
            return self._apis[api]

        except KeyError:
            pass

        real_api_version = self.api_version(api)

        try:
            supported_api_versions = self._api_mappings[api]

        except KeyError:
            raise AttributeError(u'No API named {api}'.format(api=api))

        params.update(self.api_parameters)

        for api_version in range(real_api_version, -1, -1):
            try:
                versioned_api_class = supported_api_versions[api_version]

                if real_api_version != api_version:
                    logging.warning(u'API ({api}) v{real_api_version} not available. '
                                    u'Using v{api_version} as fallback.'.format(api=api,
                                                                                real_api_version=real_api_version,
                                                                                api_version=api_version))

                self._apis[api] = versioned_api_class(**params)

                return self._apis[api]

            except KeyError:
                pass

        raise self.MISSING_API(u'API ({api}) v{real_api_version} not available. '
                               u'No fallback version available. '
                               u'Available versions:{available}'.format(api=api,
                                                                        real_api_version=real_api_version,
                                                                        available=supported_api_versions.keys()
                                                                        if supported_api_versions
                                                                        else None))

    def close(self):
        for api in list(self._apis.values()):
            api.close()

    def __del__(self):
        self.close()

    def __getattr__(self,
                    api):
        return self.api(api)
