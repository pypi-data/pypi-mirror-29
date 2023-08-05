# coding=utf-8
"""
This code was generated by
\ / _    _  _|   _  _
 | (_)\/(_)(_|\/| |(/_  v1.0.0
      /       /
"""

from twilio.base import serialize
from twilio.base import values
from twilio.base.instance_resource import InstanceResource
from twilio.base.list_resource import ListResource
from twilio.base.page import Page


class UsageRecordList(ListResource):
    """ PLEASE NOTE that this class contains beta products that are subject to
    change. Use them with caution. """

    def __init__(self, version, sim_sid):
        """
        Initialize the UsageRecordList

        :param Version version: Version that contains the resource
        :param sim_sid: The sim_sid

        :returns: twilio.rest.wireless.v1.sim.usage_record.UsageRecordList
        :rtype: twilio.rest.wireless.v1.sim.usage_record.UsageRecordList
        """
        super(UsageRecordList, self).__init__(version)

        # Path Solution
        self._solution = {'sim_sid': sim_sid, }
        self._uri = '/Sims/{sim_sid}/UsageRecords'.format(**self._solution)

    def stream(self, end=values.unset, start=values.unset, granularity=values.unset,
               limit=None, page_size=None):
        """
        Streams UsageRecordInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.

        :param datetime end: The end
        :param datetime start: The start
        :param UsageRecordInstance.Granularity granularity: The granularity
        :param int limit: Upper limit for the number of records to return. stream()
                          guarantees to never return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, stream() will attempt to read the
                              limit with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[twilio.rest.wireless.v1.sim.usage_record.UsageRecordInstance]
        """
        limits = self._version.read_limits(limit, page_size)

        page = self.page(end=end, start=start, granularity=granularity, page_size=limits['page_size'], )

        return self._version.stream(page, limits['limit'], limits['page_limit'])

    def list(self, end=values.unset, start=values.unset, granularity=values.unset,
             limit=None, page_size=None):
        """
        Lists UsageRecordInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.

        :param datetime end: The end
        :param datetime start: The start
        :param UsageRecordInstance.Granularity granularity: The granularity
        :param int limit: Upper limit for the number of records to return. list() guarantees
                          never to return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, list() will attempt to read the limit
                              with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[twilio.rest.wireless.v1.sim.usage_record.UsageRecordInstance]
        """
        return list(self.stream(
            end=end,
            start=start,
            granularity=granularity,
            limit=limit,
            page_size=page_size,
        ))

    def page(self, end=values.unset, start=values.unset, granularity=values.unset,
             page_token=values.unset, page_number=values.unset,
             page_size=values.unset):
        """
        Retrieve a single page of UsageRecordInstance records from the API.
        Request is executed immediately

        :param datetime end: The end
        :param datetime start: The start
        :param UsageRecordInstance.Granularity granularity: The granularity
        :param str page_token: PageToken provided by the API
        :param int page_number: Page Number, this value is simply for client state
        :param int page_size: Number of records to return, defaults to 50

        :returns: Page of UsageRecordInstance
        :rtype: twilio.rest.wireless.v1.sim.usage_record.UsageRecordPage
        """
        params = values.of({
            'End': serialize.iso8601_datetime(end),
            'Start': serialize.iso8601_datetime(start),
            'Granularity': granularity,
            'PageToken': page_token,
            'Page': page_number,
            'PageSize': page_size,
        })

        response = self._version.page(
            'GET',
            self._uri,
            params=params,
        )

        return UsageRecordPage(self._version, response, self._solution)

    def get_page(self, target_url):
        """
        Retrieve a specific page of UsageRecordInstance records from the API.
        Request is executed immediately

        :param str target_url: API-generated URL for the requested results page

        :returns: Page of UsageRecordInstance
        :rtype: twilio.rest.wireless.v1.sim.usage_record.UsageRecordPage
        """
        response = self._version.domain.twilio.request(
            'GET',
            target_url,
        )

        return UsageRecordPage(self._version, response, self._solution)

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Wireless.V1.UsageRecordList>'


class UsageRecordPage(Page):
    """ PLEASE NOTE that this class contains beta products that are subject to
    change. Use them with caution. """

    def __init__(self, version, response, solution):
        """
        Initialize the UsageRecordPage

        :param Version version: Version that contains the resource
        :param Response response: Response from the API
        :param sim_sid: The sim_sid

        :returns: twilio.rest.wireless.v1.sim.usage_record.UsageRecordPage
        :rtype: twilio.rest.wireless.v1.sim.usage_record.UsageRecordPage
        """
        super(UsageRecordPage, self).__init__(version, response)

        # Path Solution
        self._solution = solution

    def get_instance(self, payload):
        """
        Build an instance of UsageRecordInstance

        :param dict payload: Payload response from the API

        :returns: twilio.rest.wireless.v1.sim.usage_record.UsageRecordInstance
        :rtype: twilio.rest.wireless.v1.sim.usage_record.UsageRecordInstance
        """
        return UsageRecordInstance(self._version, payload, sim_sid=self._solution['sim_sid'], )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Wireless.V1.UsageRecordPage>'


class UsageRecordInstance(InstanceResource):
    """ PLEASE NOTE that this class contains beta products that are subject to
    change. Use them with caution. """

    class Granularity(object):
        HOURLY = "hourly"
        DAILY = "daily"
        ALL = "all"

    def __init__(self, version, payload, sim_sid):
        """
        Initialize the UsageRecordInstance

        :returns: twilio.rest.wireless.v1.sim.usage_record.UsageRecordInstance
        :rtype: twilio.rest.wireless.v1.sim.usage_record.UsageRecordInstance
        """
        super(UsageRecordInstance, self).__init__(version)

        # Marshaled Properties
        self._properties = {
            'sim_sid': payload['sim_sid'],
            'account_sid': payload['account_sid'],
            'period': payload['period'],
            'commands': payload['commands'],
            'data': payload['data'],
        }

        # Context
        self._context = None
        self._solution = {'sim_sid': sim_sid, }

    @property
    def sim_sid(self):
        """
        :returns: The sim_sid
        :rtype: unicode
        """
        return self._properties['sim_sid']

    @property
    def account_sid(self):
        """
        :returns: The account_sid
        :rtype: unicode
        """
        return self._properties['account_sid']

    @property
    def period(self):
        """
        :returns: The period
        :rtype: dict
        """
        return self._properties['period']

    @property
    def commands(self):
        """
        :returns: The commands
        :rtype: dict
        """
        return self._properties['commands']

    @property
    def data(self):
        """
        :returns: The data
        :rtype: dict
        """
        return self._properties['data']

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Wireless.V1.UsageRecordInstance>'
