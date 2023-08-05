# coding=utf-8
"""
This code was generated by
\ / _    _  _|   _  _
 | (_)\/(_)(_|\/| |(/_  v1.0.0
      /       /
"""

from twilio.base import deserialize
from twilio.base import serialize
from twilio.base import values
from twilio.base.instance_context import InstanceContext
from twilio.base.instance_resource import InstanceResource
from twilio.base.list_resource import ListResource
from twilio.base.page import Page
from twilio.rest.api.v2010.account.message.feedback import FeedbackList
from twilio.rest.api.v2010.account.message.media import MediaList


class MessageList(ListResource):
    """  """

    def __init__(self, version, account_sid):
        """
        Initialize the MessageList

        :param Version version: Version that contains the resource
        :param account_sid: The unique sid that identifies this account

        :returns: twilio.rest.api.v2010.account.message.MessageList
        :rtype: twilio.rest.api.v2010.account.message.MessageList
        """
        super(MessageList, self).__init__(version)

        # Path Solution
        self._solution = {'account_sid': account_sid, }
        self._uri = '/Accounts/{account_sid}/Messages.json'.format(**self._solution)

    def create(self, to, status_callback=values.unset, application_sid=values.unset,
               max_price=values.unset, provide_feedback=values.unset,
               validity_period=values.unset, max_rate=values.unset,
               force_delivery=values.unset, provider_sid=values.unset,
               content_retention=values.unset, address_retention=values.unset,
               smart_encoded=values.unset, from_=values.unset,
               messaging_service_sid=values.unset, body=values.unset,
               media_url=values.unset):
        """
        Create a new MessageInstance

        :param unicode to: The phone number to receive the message
        :param unicode status_callback: URL Twilio will request when the status changes
        :param unicode application_sid: The application to use for callbacks
        :param unicode max_price: The max_price
        :param bool provide_feedback: The provide_feedback
        :param unicode validity_period: The validity_period
        :param unicode max_rate: The max_rate
        :param bool force_delivery: The force_delivery
        :param unicode provider_sid: The provider_sid
        :param MessageInstance.ContentRetention content_retention: The content_retention
        :param MessageInstance.AddressRetention address_retention: The address_retention
        :param bool smart_encoded: The smart_encoded
        :param unicode from_: The phone number that initiated the message
        :param unicode messaging_service_sid: The messaging_service_sid
        :param unicode body: The body
        :param unicode media_url: The media_url

        :returns: Newly created MessageInstance
        :rtype: twilio.rest.api.v2010.account.message.MessageInstance
        """
        data = values.of({
            'To': to,
            'From': from_,
            'MessagingServiceSid': messaging_service_sid,
            'Body': body,
            'MediaUrl': serialize.map(media_url, lambda e: e),
            'StatusCallback': status_callback,
            'ApplicationSid': application_sid,
            'MaxPrice': max_price,
            'ProvideFeedback': provide_feedback,
            'ValidityPeriod': validity_period,
            'MaxRate': max_rate,
            'ForceDelivery': force_delivery,
            'ProviderSid': provider_sid,
            'ContentRetention': content_retention,
            'AddressRetention': address_retention,
            'SmartEncoded': smart_encoded,
        })

        payload = self._version.create(
            'POST',
            self._uri,
            data=data,
        )

        return MessageInstance(self._version, payload, account_sid=self._solution['account_sid'], )

    def stream(self, to=values.unset, from_=values.unset,
               date_sent_before=values.unset, date_sent=values.unset,
               date_sent_after=values.unset, limit=None, page_size=None):
        """
        Streams MessageInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.

        :param unicode to: Filter by messages to this number
        :param unicode from_: Filter by from number
        :param datetime date_sent_before: Filter by date sent
        :param datetime date_sent: Filter by date sent
        :param datetime date_sent_after: Filter by date sent
        :param int limit: Upper limit for the number of records to return. stream()
                          guarantees to never return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, stream() will attempt to read the
                              limit with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[twilio.rest.api.v2010.account.message.MessageInstance]
        """
        limits = self._version.read_limits(limit, page_size)

        page = self.page(
            to=to,
            from_=from_,
            date_sent_before=date_sent_before,
            date_sent=date_sent,
            date_sent_after=date_sent_after,
            page_size=limits['page_size'],
        )

        return self._version.stream(page, limits['limit'], limits['page_limit'])

    def list(self, to=values.unset, from_=values.unset,
             date_sent_before=values.unset, date_sent=values.unset,
             date_sent_after=values.unset, limit=None, page_size=None):
        """
        Lists MessageInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.

        :param unicode to: Filter by messages to this number
        :param unicode from_: Filter by from number
        :param datetime date_sent_before: Filter by date sent
        :param datetime date_sent: Filter by date sent
        :param datetime date_sent_after: Filter by date sent
        :param int limit: Upper limit for the number of records to return. list() guarantees
                          never to return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, list() will attempt to read the limit
                              with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[twilio.rest.api.v2010.account.message.MessageInstance]
        """
        return list(self.stream(
            to=to,
            from_=from_,
            date_sent_before=date_sent_before,
            date_sent=date_sent,
            date_sent_after=date_sent_after,
            limit=limit,
            page_size=page_size,
        ))

    def page(self, to=values.unset, from_=values.unset,
             date_sent_before=values.unset, date_sent=values.unset,
             date_sent_after=values.unset, page_token=values.unset,
             page_number=values.unset, page_size=values.unset):
        """
        Retrieve a single page of MessageInstance records from the API.
        Request is executed immediately

        :param unicode to: Filter by messages to this number
        :param unicode from_: Filter by from number
        :param datetime date_sent_before: Filter by date sent
        :param datetime date_sent: Filter by date sent
        :param datetime date_sent_after: Filter by date sent
        :param str page_token: PageToken provided by the API
        :param int page_number: Page Number, this value is simply for client state
        :param int page_size: Number of records to return, defaults to 50

        :returns: Page of MessageInstance
        :rtype: twilio.rest.api.v2010.account.message.MessagePage
        """
        params = values.of({
            'To': to,
            'From': from_,
            'DateSent<': serialize.iso8601_datetime(date_sent_before),
            'DateSent': serialize.iso8601_datetime(date_sent),
            'DateSent>': serialize.iso8601_datetime(date_sent_after),
            'PageToken': page_token,
            'Page': page_number,
            'PageSize': page_size,
        })

        response = self._version.page(
            'GET',
            self._uri,
            params=params,
        )

        return MessagePage(self._version, response, self._solution)

    def get_page(self, target_url):
        """
        Retrieve a specific page of MessageInstance records from the API.
        Request is executed immediately

        :param str target_url: API-generated URL for the requested results page

        :returns: Page of MessageInstance
        :rtype: twilio.rest.api.v2010.account.message.MessagePage
        """
        response = self._version.domain.twilio.request(
            'GET',
            target_url,
        )

        return MessagePage(self._version, response, self._solution)

    def get(self, sid):
        """
        Constructs a MessageContext

        :param sid: Fetch by unique message Sid

        :returns: twilio.rest.api.v2010.account.message.MessageContext
        :rtype: twilio.rest.api.v2010.account.message.MessageContext
        """
        return MessageContext(self._version, account_sid=self._solution['account_sid'], sid=sid, )

    def __call__(self, sid):
        """
        Constructs a MessageContext

        :param sid: Fetch by unique message Sid

        :returns: twilio.rest.api.v2010.account.message.MessageContext
        :rtype: twilio.rest.api.v2010.account.message.MessageContext
        """
        return MessageContext(self._version, account_sid=self._solution['account_sid'], sid=sid, )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Api.V2010.MessageList>'


class MessagePage(Page):
    """  """

    def __init__(self, version, response, solution):
        """
        Initialize the MessagePage

        :param Version version: Version that contains the resource
        :param Response response: Response from the API
        :param account_sid: The unique sid that identifies this account

        :returns: twilio.rest.api.v2010.account.message.MessagePage
        :rtype: twilio.rest.api.v2010.account.message.MessagePage
        """
        super(MessagePage, self).__init__(version, response)

        # Path Solution
        self._solution = solution

    def get_instance(self, payload):
        """
        Build an instance of MessageInstance

        :param dict payload: Payload response from the API

        :returns: twilio.rest.api.v2010.account.message.MessageInstance
        :rtype: twilio.rest.api.v2010.account.message.MessageInstance
        """
        return MessageInstance(self._version, payload, account_sid=self._solution['account_sid'], )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Api.V2010.MessagePage>'


class MessageContext(InstanceContext):
    """  """

    def __init__(self, version, account_sid, sid):
        """
        Initialize the MessageContext

        :param Version version: Version that contains the resource
        :param account_sid: The account_sid
        :param sid: Fetch by unique message Sid

        :returns: twilio.rest.api.v2010.account.message.MessageContext
        :rtype: twilio.rest.api.v2010.account.message.MessageContext
        """
        super(MessageContext, self).__init__(version)

        # Path Solution
        self._solution = {'account_sid': account_sid, 'sid': sid, }
        self._uri = '/Accounts/{account_sid}/Messages/{sid}.json'.format(**self._solution)

        # Dependents
        self._media = None
        self._feedback = None

    def delete(self):
        """
        Deletes the MessageInstance

        :returns: True if delete succeeds, False otherwise
        :rtype: bool
        """
        return self._version.delete('delete', self._uri)

    def fetch(self):
        """
        Fetch a MessageInstance

        :returns: Fetched MessageInstance
        :rtype: twilio.rest.api.v2010.account.message.MessageInstance
        """
        params = values.of({})

        payload = self._version.fetch(
            'GET',
            self._uri,
            params=params,
        )

        return MessageInstance(
            self._version,
            payload,
            account_sid=self._solution['account_sid'],
            sid=self._solution['sid'],
        )

    def update(self, body):
        """
        Update the MessageInstance

        :param unicode body: The body

        :returns: Updated MessageInstance
        :rtype: twilio.rest.api.v2010.account.message.MessageInstance
        """
        data = values.of({'Body': body, })

        payload = self._version.update(
            'POST',
            self._uri,
            data=data,
        )

        return MessageInstance(
            self._version,
            payload,
            account_sid=self._solution['account_sid'],
            sid=self._solution['sid'],
        )

    @property
    def media(self):
        """
        Access the media

        :returns: twilio.rest.api.v2010.account.message.media.MediaList
        :rtype: twilio.rest.api.v2010.account.message.media.MediaList
        """
        if self._media is None:
            self._media = MediaList(
                self._version,
                account_sid=self._solution['account_sid'],
                message_sid=self._solution['sid'],
            )
        return self._media

    @property
    def feedback(self):
        """
        Access the feedback

        :returns: twilio.rest.api.v2010.account.message.feedback.FeedbackList
        :rtype: twilio.rest.api.v2010.account.message.feedback.FeedbackList
        """
        if self._feedback is None:
            self._feedback = FeedbackList(
                self._version,
                account_sid=self._solution['account_sid'],
                message_sid=self._solution['sid'],
            )
        return self._feedback

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Api.V2010.MessageContext {}>'.format(context)


class MessageInstance(InstanceResource):
    """  """

    class Status(object):
        QUEUED = "queued"
        SENDING = "sending"
        SENT = "sent"
        FAILED = "failed"
        DELIVERED = "delivered"
        UNDELIVERED = "undelivered"
        RECEIVING = "receiving"
        RECEIVED = "received"
        ACCEPTED = "accepted"

    class Direction(object):
        INBOUND = "inbound"
        OUTBOUND_API = "outbound-api"
        OUTBOUND_CALL = "outbound-call"
        OUTBOUND_REPLY = "outbound-reply"

    class ContentRetention(object):
        RETAIN = "retain"
        DISCARD = "discard"

    class AddressRetention(object):
        RETAIN = "retain"
        DISCARD = "discard"

    def __init__(self, version, payload, account_sid, sid=None):
        """
        Initialize the MessageInstance

        :returns: twilio.rest.api.v2010.account.message.MessageInstance
        :rtype: twilio.rest.api.v2010.account.message.MessageInstance
        """
        super(MessageInstance, self).__init__(version)

        # Marshaled Properties
        self._properties = {
            'account_sid': payload['account_sid'],
            'api_version': payload['api_version'],
            'body': payload['body'],
            'date_created': deserialize.rfc2822_datetime(payload['date_created']),
            'date_updated': deserialize.rfc2822_datetime(payload['date_updated']),
            'date_sent': deserialize.rfc2822_datetime(payload['date_sent']),
            'direction': payload['direction'],
            'error_code': deserialize.integer(payload['error_code']),
            'error_message': payload['error_message'],
            'from_': payload['from'],
            'messaging_service_sid': payload['messaging_service_sid'],
            'num_media': payload['num_media'],
            'num_segments': payload['num_segments'],
            'price': deserialize.decimal(payload['price']),
            'price_unit': payload['price_unit'],
            'sid': payload['sid'],
            'status': payload['status'],
            'subresource_uris': payload['subresource_uris'],
            'to': payload['to'],
            'uri': payload['uri'],
        }

        # Context
        self._context = None
        self._solution = {'account_sid': account_sid, 'sid': sid or self._properties['sid'], }

    @property
    def _proxy(self):
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions.  All instance actions are proxied to the context

        :returns: MessageContext for this MessageInstance
        :rtype: twilio.rest.api.v2010.account.message.MessageContext
        """
        if self._context is None:
            self._context = MessageContext(
                self._version,
                account_sid=self._solution['account_sid'],
                sid=self._solution['sid'],
            )
        return self._context

    @property
    def account_sid(self):
        """
        :returns: The unique sid that identifies this account
        :rtype: unicode
        """
        return self._properties['account_sid']

    @property
    def api_version(self):
        """
        :returns: The version of the Twilio API used to process the message.
        :rtype: unicode
        """
        return self._properties['api_version']

    @property
    def body(self):
        """
        :returns: The text body of the message. Up to 1600 characters long.
        :rtype: unicode
        """
        return self._properties['body']

    @property
    def date_created(self):
        """
        :returns: The date this resource was created
        :rtype: datetime
        """
        return self._properties['date_created']

    @property
    def date_updated(self):
        """
        :returns: The date this resource was last updated
        :rtype: datetime
        """
        return self._properties['date_updated']

    @property
    def date_sent(self):
        """
        :returns: The date the message was sent
        :rtype: datetime
        """
        return self._properties['date_sent']

    @property
    def direction(self):
        """
        :returns: The direction of the message
        :rtype: MessageInstance.Direction
        """
        return self._properties['direction']

    @property
    def error_code(self):
        """
        :returns: The error code associated with the message
        :rtype: unicode
        """
        return self._properties['error_code']

    @property
    def error_message(self):
        """
        :returns: Human readable description of the ErrorCode
        :rtype: unicode
        """
        return self._properties['error_message']

    @property
    def from_(self):
        """
        :returns: The phone number that initiated the message
        :rtype: unicode
        """
        return self._properties['from_']

    @property
    def messaging_service_sid(self):
        """
        :returns: The messaging_service_sid
        :rtype: unicode
        """
        return self._properties['messaging_service_sid']

    @property
    def num_media(self):
        """
        :returns: Number of media files associated with the message
        :rtype: unicode
        """
        return self._properties['num_media']

    @property
    def num_segments(self):
        """
        :returns: Indicates number of messages used to delivery the body
        :rtype: unicode
        """
        return self._properties['num_segments']

    @property
    def price(self):
        """
        :returns: The amount billed for the message
        :rtype: unicode
        """
        return self._properties['price']

    @property
    def price_unit(self):
        """
        :returns: The currency in which Price is measured
        :rtype: unicode
        """
        return self._properties['price_unit']

    @property
    def sid(self):
        """
        :returns: A string that uniquely identifies this message
        :rtype: unicode
        """
        return self._properties['sid']

    @property
    def status(self):
        """
        :returns: The status of this message
        :rtype: MessageInstance.Status
        """
        return self._properties['status']

    @property
    def subresource_uris(self):
        """
        :returns: The URI for any subresources
        :rtype: unicode
        """
        return self._properties['subresource_uris']

    @property
    def to(self):
        """
        :returns: The phone number that received the message
        :rtype: unicode
        """
        return self._properties['to']

    @property
    def uri(self):
        """
        :returns: The URI for this resource
        :rtype: unicode
        """
        return self._properties['uri']

    def delete(self):
        """
        Deletes the MessageInstance

        :returns: True if delete succeeds, False otherwise
        :rtype: bool
        """
        return self._proxy.delete()

    def fetch(self):
        """
        Fetch a MessageInstance

        :returns: Fetched MessageInstance
        :rtype: twilio.rest.api.v2010.account.message.MessageInstance
        """
        return self._proxy.fetch()

    def update(self, body):
        """
        Update the MessageInstance

        :param unicode body: The body

        :returns: Updated MessageInstance
        :rtype: twilio.rest.api.v2010.account.message.MessageInstance
        """
        return self._proxy.update(body, )

    @property
    def media(self):
        """
        Access the media

        :returns: twilio.rest.api.v2010.account.message.media.MediaList
        :rtype: twilio.rest.api.v2010.account.message.media.MediaList
        """
        return self._proxy.media

    @property
    def feedback(self):
        """
        Access the feedback

        :returns: twilio.rest.api.v2010.account.message.feedback.FeedbackList
        :rtype: twilio.rest.api.v2010.account.message.feedback.FeedbackList
        """
        return self._proxy.feedback

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Api.V2010.MessageInstance {}>'.format(context)
