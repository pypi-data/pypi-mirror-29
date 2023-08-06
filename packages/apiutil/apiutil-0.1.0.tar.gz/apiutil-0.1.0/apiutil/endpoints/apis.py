# encoding: utf-8

from future.utils import iteritems
from configurationutil import (CfgItems,
                               InheritableCfgItem,
                               DefaultInheritableConstant)
from .config import register_api_config
from ._constants import API_CONFIG, APIKeysConstant
from .hosts import Hosts
from .endpoints import Endpoints


class API(InheritableCfgItem):
    """ Representation of a single API, overrides InheritableCfgItem. """
    STRICT = False
    DEFAULT_PARAMS = {
        APIKeysConstant.host: u'',
        APIKeysConstant.endpoints: [u'default_root'],
        APIKeysConstant.params: None
    }

    def __getitem__(self, item):

        """ Extends InheritableCfgItem.__getitem__ to explode default params.

        Will get the API configuration as InheritableCfgItem.__getitem__ but will update
        the following:
            --> host:       Validate host config exists and retrieve the Host object from self.HOSTS.
            --> endpoints:  For each listed endpoint, validate endpoint config exists and retrieve
                            the Endpoint object from self.ENDPOINTS.
        Note: if host or any endpoints are invalid a KeyError will be raised.

        """

        item_value = super(API, self).__getitem__(item)

        # Attempt to explode Host
        if item == APIKeysConstant.host:
            try:
                return Hosts()[item_value]

            except LookupError:
                raise KeyError(u'No Host configuration exists for {host}! '
                               u'Please check your configuration!'.format(host=item_value))

        # Attempt to explode Endpoints
        if item == APIKeysConstant.endpoints:
            return Endpoints(allowed_endpoints=item_value,
                             host=self.host)

        return item_value

    def match_url(self,
                  url):

        """ Work out whether the url captured is from this endpoint.

        :param url:     (string)    Full URL to determine the matches for.
        :return:        (list)      List of matched endpoints for the url.
                                    Each item in the list is a tuple of the form:
                                        (API Family, API Name, Endpoint Name)
        """

        best_match = -1
        matched_endpoints = []

        for endpoint_name, endpoint in iteritems(self.endpoints):
            matched_len = endpoint.match_url(url)

            if matched_len > -1:
                match_ref = (self.family, self.key, endpoint_name)

                if matched_len > best_match:
                    # Better than our best match so restart the list
                    matched_endpoints = [match_ref]
                    best_match = matched_len

                elif matched_len == best_match and match_ref not in matched_endpoints:
                    # Same as best match to append to list
                    matched_endpoints.append(match_ref)

        return matched_endpoints, best_match


class APIS(CfgItems):

    """ API configuration.

    Get environments object:
    >>> apis = APIS()

    Get A list of available APIs:
    >>> list(apis)
    ['example_api', 'example_api_2']

    """

    def __init__(self):
        super(APIS, self).__init__(cfg_fn=register_api_config,
                                   cfg_root=API_CONFIG,
                                   key_name=DefaultInheritableConstant.name,
                                   item_class=API)

    def get_api_family(self,
                       family=None):

        """ Get and return a list of APIs belonging to an API family.

        :param family:  (string) The API family to get a list of APIs for.
                        default=None (the default family)
        :return:        (list)   List of API names for this family.
        """

        return [api_name for api_name, api in iteritems(self) if api.family == family]

    def get_endpoint_for_request(self,
                                 url):

        """ Determine and return the API / Endpoint config for a URL.

        :param url:     (string)    Full URL to determine the config for.
        :return:        (tuple)     Match tuple values: (API Family, API Name, Endpoint Name)

        Examples:
        ---------
        Work out the Env / API configuration for a request:
        >>> APIS().get_endpoint_for_request(u'http://api.example.com/1.1/sometest')
        'example_api'

        """

        best_match = -1
        matched_endpoints = []

        for _, api in iteritems(self):
            matches, match_length = api.match_url(url)

            if match_length > best_match:
                matched_endpoints = matches

            elif match_length == best_match:
                matched_endpoints += matches

        if len(matched_endpoints) == 1:
            return matched_endpoints.pop()

        if len(matched_endpoints) == 0:
            raise LookupError(u'No Endpoint match for: {url}'.format(url=url))

        raise LookupError(u'Multiple matching Endpoints for: {url}\n'
                          u'(Check your config)'.format(url=url))
