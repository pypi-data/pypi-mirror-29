# coding=utf-8
"""
This code was generated by
\ / _    _  _|   _  _
 | (_)\/(_)(_|\/| |(/_  v1.0.0
      /       /
"""

from twilio.base import deserialize
from twilio.base import values
from twilio.base.instance_context import InstanceContext
from twilio.base.instance_resource import InstanceResource
from twilio.base.list_resource import ListResource
from twilio.base.page import Page
from twilio.rest.proxy.v1.service.phone_number import PhoneNumberList
from twilio.rest.proxy.v1.service.session import SessionList
from twilio.rest.proxy.v1.service.short_code import ShortCodeList


class ServiceList(ListResource):
    """ PLEASE NOTE that this class contains beta products that are subject to
    change. Use them with caution. """

    def __init__(self, version):
        """
        Initialize the ServiceList

        :param Version version: Version that contains the resource

        :returns: twilio.rest.proxy.v1.service.ServiceList
        :rtype: twilio.rest.proxy.v1.service.ServiceList
        """
        super(ServiceList, self).__init__(version)

        # Path Solution
        self._solution = {}
        self._uri = '/Services'.format(**self._solution)

    def stream(self, limit=None, page_size=None):
        """
        Streams ServiceInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.

        :param int limit: Upper limit for the number of records to return. stream()
                          guarantees to never return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, stream() will attempt to read the
                              limit with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[twilio.rest.proxy.v1.service.ServiceInstance]
        """
        limits = self._version.read_limits(limit, page_size)

        page = self.page(page_size=limits['page_size'], )

        return self._version.stream(page, limits['limit'], limits['page_limit'])

    def list(self, limit=None, page_size=None):
        """
        Lists ServiceInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.

        :param int limit: Upper limit for the number of records to return. list() guarantees
                          never to return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, list() will attempt to read the limit
                              with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[twilio.rest.proxy.v1.service.ServiceInstance]
        """
        return list(self.stream(limit=limit, page_size=page_size, ))

    def page(self, page_token=values.unset, page_number=values.unset,
             page_size=values.unset):
        """
        Retrieve a single page of ServiceInstance records from the API.
        Request is executed immediately

        :param str page_token: PageToken provided by the API
        :param int page_number: Page Number, this value is simply for client state
        :param int page_size: Number of records to return, defaults to 50

        :returns: Page of ServiceInstance
        :rtype: twilio.rest.proxy.v1.service.ServicePage
        """
        params = values.of({'PageToken': page_token, 'Page': page_number, 'PageSize': page_size, })

        response = self._version.page(
            'GET',
            self._uri,
            params=params,
        )

        return ServicePage(self._version, response, self._solution)

    def get_page(self, target_url):
        """
        Retrieve a specific page of ServiceInstance records from the API.
        Request is executed immediately

        :param str target_url: API-generated URL for the requested results page

        :returns: Page of ServiceInstance
        :rtype: twilio.rest.proxy.v1.service.ServicePage
        """
        response = self._version.domain.twilio.request(
            'GET',
            target_url,
        )

        return ServicePage(self._version, response, self._solution)

    def create(self, unique_name, default_ttl=values.unset,
               callback_url=values.unset, geo_match_level=values.unset,
               number_selection_behavior=values.unset,
               intercept_callback_url=values.unset,
               out_of_session_callback_url=values.unset):
        """
        Create a new ServiceInstance

        :param unicode unique_name: The human-readable string that uniquely identifies this Service.
        :param unicode default_ttl: Default TTL for a Session, in seconds.
        :param unicode callback_url: URL Twilio will send callbacks to
        :param ServiceInstance.GeoMatchLevel geo_match_level: Whether to find proxy numbers in the same areacode.
        :param ServiceInstance.NumberSelectionBehavior number_selection_behavior: What behavior to use when choosing a proxy number.
        :param unicode intercept_callback_url: A URL for Twilio call before each Interaction.
        :param unicode out_of_session_callback_url: A URL for Twilio call when a new Interaction has no Session.

        :returns: Newly created ServiceInstance
        :rtype: twilio.rest.proxy.v1.service.ServiceInstance
        """
        data = values.of({
            'UniqueName': unique_name,
            'DefaultTtl': default_ttl,
            'CallbackUrl': callback_url,
            'GeoMatchLevel': geo_match_level,
            'NumberSelectionBehavior': number_selection_behavior,
            'InterceptCallbackUrl': intercept_callback_url,
            'OutOfSessionCallbackUrl': out_of_session_callback_url,
        })

        payload = self._version.create(
            'POST',
            self._uri,
            data=data,
        )

        return ServiceInstance(self._version, payload, )

    def get(self, sid):
        """
        Constructs a ServiceContext

        :param sid: A string that uniquely identifies this Service.

        :returns: twilio.rest.proxy.v1.service.ServiceContext
        :rtype: twilio.rest.proxy.v1.service.ServiceContext
        """
        return ServiceContext(self._version, sid=sid, )

    def __call__(self, sid):
        """
        Constructs a ServiceContext

        :param sid: A string that uniquely identifies this Service.

        :returns: twilio.rest.proxy.v1.service.ServiceContext
        :rtype: twilio.rest.proxy.v1.service.ServiceContext
        """
        return ServiceContext(self._version, sid=sid, )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Proxy.V1.ServiceList>'


class ServicePage(Page):
    """ PLEASE NOTE that this class contains beta products that are subject to
    change. Use them with caution. """

    def __init__(self, version, response, solution):
        """
        Initialize the ServicePage

        :param Version version: Version that contains the resource
        :param Response response: Response from the API

        :returns: twilio.rest.proxy.v1.service.ServicePage
        :rtype: twilio.rest.proxy.v1.service.ServicePage
        """
        super(ServicePage, self).__init__(version, response)

        # Path Solution
        self._solution = solution

    def get_instance(self, payload):
        """
        Build an instance of ServiceInstance

        :param dict payload: Payload response from the API

        :returns: twilio.rest.proxy.v1.service.ServiceInstance
        :rtype: twilio.rest.proxy.v1.service.ServiceInstance
        """
        return ServiceInstance(self._version, payload, )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Proxy.V1.ServicePage>'


class ServiceContext(InstanceContext):
    """ PLEASE NOTE that this class contains beta products that are subject to
    change. Use them with caution. """

    def __init__(self, version, sid):
        """
        Initialize the ServiceContext

        :param Version version: Version that contains the resource
        :param sid: A string that uniquely identifies this Service.

        :returns: twilio.rest.proxy.v1.service.ServiceContext
        :rtype: twilio.rest.proxy.v1.service.ServiceContext
        """
        super(ServiceContext, self).__init__(version)

        # Path Solution
        self._solution = {'sid': sid, }
        self._uri = '/Services/{sid}'.format(**self._solution)

        # Dependents
        self._sessions = None
        self._phone_numbers = None
        self._short_codes = None

    def fetch(self):
        """
        Fetch a ServiceInstance

        :returns: Fetched ServiceInstance
        :rtype: twilio.rest.proxy.v1.service.ServiceInstance
        """
        params = values.of({})

        payload = self._version.fetch(
            'GET',
            self._uri,
            params=params,
        )

        return ServiceInstance(self._version, payload, sid=self._solution['sid'], )

    def delete(self):
        """
        Deletes the ServiceInstance

        :returns: True if delete succeeds, False otherwise
        :rtype: bool
        """
        return self._version.delete('delete', self._uri)

    def update(self, unique_name=values.unset, default_ttl=values.unset,
               callback_url=values.unset, geo_match_level=values.unset,
               number_selection_behavior=values.unset,
               intercept_callback_url=values.unset,
               out_of_session_callback_url=values.unset):
        """
        Update the ServiceInstance

        :param unicode unique_name: A human readable description of this resource.
        :param unicode default_ttl: Default TTL for a Session, in seconds.
        :param unicode callback_url: URL Twilio will send callbacks to
        :param ServiceInstance.GeoMatchLevel geo_match_level: Whether to find proxy numbers in the same areacode.
        :param ServiceInstance.NumberSelectionBehavior number_selection_behavior: What behavior to use when choosing a proxy number.
        :param unicode intercept_callback_url: A URL for Twilio call before each Interaction.
        :param unicode out_of_session_callback_url: A URL for Twilio call when a new Interaction has no Session.

        :returns: Updated ServiceInstance
        :rtype: twilio.rest.proxy.v1.service.ServiceInstance
        """
        data = values.of({
            'UniqueName': unique_name,
            'DefaultTtl': default_ttl,
            'CallbackUrl': callback_url,
            'GeoMatchLevel': geo_match_level,
            'NumberSelectionBehavior': number_selection_behavior,
            'InterceptCallbackUrl': intercept_callback_url,
            'OutOfSessionCallbackUrl': out_of_session_callback_url,
        })

        payload = self._version.update(
            'POST',
            self._uri,
            data=data,
        )

        return ServiceInstance(self._version, payload, sid=self._solution['sid'], )

    @property
    def sessions(self):
        """
        Access the sessions

        :returns: twilio.rest.proxy.v1.service.session.SessionList
        :rtype: twilio.rest.proxy.v1.service.session.SessionList
        """
        if self._sessions is None:
            self._sessions = SessionList(self._version, service_sid=self._solution['sid'], )
        return self._sessions

    @property
    def phone_numbers(self):
        """
        Access the phone_numbers

        :returns: twilio.rest.proxy.v1.service.phone_number.PhoneNumberList
        :rtype: twilio.rest.proxy.v1.service.phone_number.PhoneNumberList
        """
        if self._phone_numbers is None:
            self._phone_numbers = PhoneNumberList(self._version, service_sid=self._solution['sid'], )
        return self._phone_numbers

    @property
    def short_codes(self):
        """
        Access the short_codes

        :returns: twilio.rest.proxy.v1.service.short_code.ShortCodeList
        :rtype: twilio.rest.proxy.v1.service.short_code.ShortCodeList
        """
        if self._short_codes is None:
            self._short_codes = ShortCodeList(self._version, service_sid=self._solution['sid'], )
        return self._short_codes

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Proxy.V1.ServiceContext {}>'.format(context)


class ServiceInstance(InstanceResource):
    """ PLEASE NOTE that this class contains beta products that are subject to
    change. Use them with caution. """

    class GeoMatchLevel(object):
        AREA_CODE = "area-code"
        OVERLAY = "overlay"
        RADIUS = "radius"
        COUNTRY = "country"

    class NumberSelectionBehavior(object):
        AVOID_STICKY = "avoid-sticky"
        PREFER_STICKY = "prefer-sticky"

    def __init__(self, version, payload, sid=None):
        """
        Initialize the ServiceInstance

        :returns: twilio.rest.proxy.v1.service.ServiceInstance
        :rtype: twilio.rest.proxy.v1.service.ServiceInstance
        """
        super(ServiceInstance, self).__init__(version)

        # Marshaled Properties
        self._properties = {
            'sid': payload['sid'],
            'unique_name': payload['unique_name'],
            'account_sid': payload['account_sid'],
            'callback_url': payload['callback_url'],
            'default_ttl': deserialize.integer(payload['default_ttl']),
            'number_selection_behavior': payload['number_selection_behavior'],
            'geo_match_level': payload['geo_match_level'],
            'intercept_callback_url': payload['intercept_callback_url'],
            'out_of_session_callback_url': payload['out_of_session_callback_url'],
            'date_created': deserialize.iso8601_datetime(payload['date_created']),
            'date_updated': deserialize.iso8601_datetime(payload['date_updated']),
            'url': payload['url'],
            'links': payload['links'],
        }

        # Context
        self._context = None
        self._solution = {'sid': sid or self._properties['sid'], }

    @property
    def _proxy(self):
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions.  All instance actions are proxied to the context

        :returns: ServiceContext for this ServiceInstance
        :rtype: twilio.rest.proxy.v1.service.ServiceContext
        """
        if self._context is None:
            self._context = ServiceContext(self._version, sid=self._solution['sid'], )
        return self._context

    @property
    def sid(self):
        """
        :returns: A string that uniquely identifies this Service.
        :rtype: unicode
        """
        return self._properties['sid']

    @property
    def unique_name(self):
        """
        :returns: A human readable description of this resource.
        :rtype: unicode
        """
        return self._properties['unique_name']

    @property
    def account_sid(self):
        """
        :returns: Account Sid.
        :rtype: unicode
        """
        return self._properties['account_sid']

    @property
    def callback_url(self):
        """
        :returns: URL Twilio will send callbacks to
        :rtype: unicode
        """
        return self._properties['callback_url']

    @property
    def default_ttl(self):
        """
        :returns: Default TTL for a Session, in seconds.
        :rtype: unicode
        """
        return self._properties['default_ttl']

    @property
    def number_selection_behavior(self):
        """
        :returns: What behavior to use when choosing a proxy number.
        :rtype: ServiceInstance.NumberSelectionBehavior
        """
        return self._properties['number_selection_behavior']

    @property
    def geo_match_level(self):
        """
        :returns: Whether to find proxy numbers in the same areacode.
        :rtype: ServiceInstance.GeoMatchLevel
        """
        return self._properties['geo_match_level']

    @property
    def intercept_callback_url(self):
        """
        :returns: A URL for Twilio call before each Interaction.
        :rtype: unicode
        """
        return self._properties['intercept_callback_url']

    @property
    def out_of_session_callback_url(self):
        """
        :returns: A URL for Twilio call when a new Interaction has no Session.
        :rtype: unicode
        """
        return self._properties['out_of_session_callback_url']

    @property
    def date_created(self):
        """
        :returns: The date this Service was created
        :rtype: datetime
        """
        return self._properties['date_created']

    @property
    def date_updated(self):
        """
        :returns: The date this Service was updated
        :rtype: datetime
        """
        return self._properties['date_updated']

    @property
    def url(self):
        """
        :returns: The URL of this resource.
        :rtype: unicode
        """
        return self._properties['url']

    @property
    def links(self):
        """
        :returns: Nested resource URLs.
        :rtype: unicode
        """
        return self._properties['links']

    def fetch(self):
        """
        Fetch a ServiceInstance

        :returns: Fetched ServiceInstance
        :rtype: twilio.rest.proxy.v1.service.ServiceInstance
        """
        return self._proxy.fetch()

    def delete(self):
        """
        Deletes the ServiceInstance

        :returns: True if delete succeeds, False otherwise
        :rtype: bool
        """
        return self._proxy.delete()

    def update(self, unique_name=values.unset, default_ttl=values.unset,
               callback_url=values.unset, geo_match_level=values.unset,
               number_selection_behavior=values.unset,
               intercept_callback_url=values.unset,
               out_of_session_callback_url=values.unset):
        """
        Update the ServiceInstance

        :param unicode unique_name: A human readable description of this resource.
        :param unicode default_ttl: Default TTL for a Session, in seconds.
        :param unicode callback_url: URL Twilio will send callbacks to
        :param ServiceInstance.GeoMatchLevel geo_match_level: Whether to find proxy numbers in the same areacode.
        :param ServiceInstance.NumberSelectionBehavior number_selection_behavior: What behavior to use when choosing a proxy number.
        :param unicode intercept_callback_url: A URL for Twilio call before each Interaction.
        :param unicode out_of_session_callback_url: A URL for Twilio call when a new Interaction has no Session.

        :returns: Updated ServiceInstance
        :rtype: twilio.rest.proxy.v1.service.ServiceInstance
        """
        return self._proxy.update(
            unique_name=unique_name,
            default_ttl=default_ttl,
            callback_url=callback_url,
            geo_match_level=geo_match_level,
            number_selection_behavior=number_selection_behavior,
            intercept_callback_url=intercept_callback_url,
            out_of_session_callback_url=out_of_session_callback_url,
        )

    @property
    def sessions(self):
        """
        Access the sessions

        :returns: twilio.rest.proxy.v1.service.session.SessionList
        :rtype: twilio.rest.proxy.v1.service.session.SessionList
        """
        return self._proxy.sessions

    @property
    def phone_numbers(self):
        """
        Access the phone_numbers

        :returns: twilio.rest.proxy.v1.service.phone_number.PhoneNumberList
        :rtype: twilio.rest.proxy.v1.service.phone_number.PhoneNumberList
        """
        return self._proxy.phone_numbers

    @property
    def short_codes(self):
        """
        Access the short_codes

        :returns: twilio.rest.proxy.v1.service.short_code.ShortCodeList
        :rtype: twilio.rest.proxy.v1.service.short_code.ShortCodeList
        """
        return self._proxy.short_codes

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Proxy.V1.ServiceInstance {}>'.format(context)
