# coding=utf-8
"""
This code was generated by
\ / _    _  _|   _  _
 | (_)\/(_)(_|\/| |(/_  v1.0.0
      /       /
"""

from twilio.base import deserialize
from twilio.base import values
from twilio.base.instance_resource import InstanceResource
from twilio.base.list_resource import ListResource
from twilio.base.page import Page


class DependentHostedNumberOrderList(ListResource):
    """ PLEASE NOTE that this class contains preview products that are subject
    to change. Use them with caution. If you currently do not have developer
    preview access, please contact help@twilio.com. """

    def __init__(self, version, signing_document_sid):
        """
        Initialize the DependentHostedNumberOrderList

        :param Version version: Version that contains the resource
        :param signing_document_sid: LOA document sid.

        :returns: twilio.rest.preview.hosted_numbers.authorization_document.dependent_hosted_number_order.DependentHostedNumberOrderList
        :rtype: twilio.rest.preview.hosted_numbers.authorization_document.dependent_hosted_number_order.DependentHostedNumberOrderList
        """
        super(DependentHostedNumberOrderList, self).__init__(version)

        # Path Solution
        self._solution = {'signing_document_sid': signing_document_sid, }
        self._uri = '/AuthorizationDocuments/{signing_document_sid}/DependentHostedNumberOrders'.format(**self._solution)

    def stream(self, status=values.unset, phone_number=values.unset,
               incoming_phone_number_sid=values.unset, friendly_name=values.unset,
               unique_name=values.unset, limit=None, page_size=None):
        """
        Streams DependentHostedNumberOrderInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.

        :param DependentHostedNumberOrderInstance.Status status: The Status of this HostedNumberOrder.
        :param unicode phone_number: An E164 formatted phone number.
        :param unicode incoming_phone_number_sid: IncomingPhoneNumber sid.
        :param unicode friendly_name: A human readable description of this resource.
        :param unicode unique_name: A unique, developer assigned name of this HostedNumberOrder.
        :param int limit: Upper limit for the number of records to return. stream()
                          guarantees to never return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, stream() will attempt to read the
                              limit with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[twilio.rest.preview.hosted_numbers.authorization_document.dependent_hosted_number_order.DependentHostedNumberOrderInstance]
        """
        limits = self._version.read_limits(limit, page_size)

        page = self.page(
            status=status,
            phone_number=phone_number,
            incoming_phone_number_sid=incoming_phone_number_sid,
            friendly_name=friendly_name,
            unique_name=unique_name,
            page_size=limits['page_size'],
        )

        return self._version.stream(page, limits['limit'], limits['page_limit'])

    def list(self, status=values.unset, phone_number=values.unset,
             incoming_phone_number_sid=values.unset, friendly_name=values.unset,
             unique_name=values.unset, limit=None, page_size=None):
        """
        Lists DependentHostedNumberOrderInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.

        :param DependentHostedNumberOrderInstance.Status status: The Status of this HostedNumberOrder.
        :param unicode phone_number: An E164 formatted phone number.
        :param unicode incoming_phone_number_sid: IncomingPhoneNumber sid.
        :param unicode friendly_name: A human readable description of this resource.
        :param unicode unique_name: A unique, developer assigned name of this HostedNumberOrder.
        :param int limit: Upper limit for the number of records to return. list() guarantees
                          never to return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, list() will attempt to read the limit
                              with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[twilio.rest.preview.hosted_numbers.authorization_document.dependent_hosted_number_order.DependentHostedNumberOrderInstance]
        """
        return list(self.stream(
            status=status,
            phone_number=phone_number,
            incoming_phone_number_sid=incoming_phone_number_sid,
            friendly_name=friendly_name,
            unique_name=unique_name,
            limit=limit,
            page_size=page_size,
        ))

    def page(self, status=values.unset, phone_number=values.unset,
             incoming_phone_number_sid=values.unset, friendly_name=values.unset,
             unique_name=values.unset, page_token=values.unset,
             page_number=values.unset, page_size=values.unset):
        """
        Retrieve a single page of DependentHostedNumberOrderInstance records from the API.
        Request is executed immediately

        :param DependentHostedNumberOrderInstance.Status status: The Status of this HostedNumberOrder.
        :param unicode phone_number: An E164 formatted phone number.
        :param unicode incoming_phone_number_sid: IncomingPhoneNumber sid.
        :param unicode friendly_name: A human readable description of this resource.
        :param unicode unique_name: A unique, developer assigned name of this HostedNumberOrder.
        :param str page_token: PageToken provided by the API
        :param int page_number: Page Number, this value is simply for client state
        :param int page_size: Number of records to return, defaults to 50

        :returns: Page of DependentHostedNumberOrderInstance
        :rtype: twilio.rest.preview.hosted_numbers.authorization_document.dependent_hosted_number_order.DependentHostedNumberOrderPage
        """
        params = values.of({
            'Status': status,
            'PhoneNumber': phone_number,
            'IncomingPhoneNumberSid': incoming_phone_number_sid,
            'FriendlyName': friendly_name,
            'UniqueName': unique_name,
            'PageToken': page_token,
            'Page': page_number,
            'PageSize': page_size,
        })

        response = self._version.page(
            'GET',
            self._uri,
            params=params,
        )

        return DependentHostedNumberOrderPage(self._version, response, self._solution)

    def get_page(self, target_url):
        """
        Retrieve a specific page of DependentHostedNumberOrderInstance records from the API.
        Request is executed immediately

        :param str target_url: API-generated URL for the requested results page

        :returns: Page of DependentHostedNumberOrderInstance
        :rtype: twilio.rest.preview.hosted_numbers.authorization_document.dependent_hosted_number_order.DependentHostedNumberOrderPage
        """
        response = self._version.domain.twilio.request(
            'GET',
            target_url,
        )

        return DependentHostedNumberOrderPage(self._version, response, self._solution)

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Preview.HostedNumbers.DependentHostedNumberOrderList>'


class DependentHostedNumberOrderPage(Page):
    """ PLEASE NOTE that this class contains preview products that are subject
    to change. Use them with caution. If you currently do not have developer
    preview access, please contact help@twilio.com. """

    def __init__(self, version, response, solution):
        """
        Initialize the DependentHostedNumberOrderPage

        :param Version version: Version that contains the resource
        :param Response response: Response from the API
        :param signing_document_sid: LOA document sid.

        :returns: twilio.rest.preview.hosted_numbers.authorization_document.dependent_hosted_number_order.DependentHostedNumberOrderPage
        :rtype: twilio.rest.preview.hosted_numbers.authorization_document.dependent_hosted_number_order.DependentHostedNumberOrderPage
        """
        super(DependentHostedNumberOrderPage, self).__init__(version, response)

        # Path Solution
        self._solution = solution

    def get_instance(self, payload):
        """
        Build an instance of DependentHostedNumberOrderInstance

        :param dict payload: Payload response from the API

        :returns: twilio.rest.preview.hosted_numbers.authorization_document.dependent_hosted_number_order.DependentHostedNumberOrderInstance
        :rtype: twilio.rest.preview.hosted_numbers.authorization_document.dependent_hosted_number_order.DependentHostedNumberOrderInstance
        """
        return DependentHostedNumberOrderInstance(
            self._version,
            payload,
            signing_document_sid=self._solution['signing_document_sid'],
        )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Preview.HostedNumbers.DependentHostedNumberOrderPage>'


class DependentHostedNumberOrderInstance(InstanceResource):
    """ PLEASE NOTE that this class contains preview products that are subject
    to change. Use them with caution. If you currently do not have developer
    preview access, please contact help@twilio.com. """

    class Status(object):
        RECEIVED = "received"
        PENDING_VERIFICATION = "pending-verification"
        VERIFIED = "verified"
        PENDING_LOA = "pending-loa"
        CARRIER_PROCESSING = "carrier-processing"
        TESTING = "testing"
        COMPLETED = "completed"
        FAILED = "failed"
        ACTION_REQUIRED = "action-required"

    class VerificationType(object):
        PHONE_CALL = "phone-call"
        PHONE_BILL = "phone-bill"

    def __init__(self, version, payload, signing_document_sid):
        """
        Initialize the DependentHostedNumberOrderInstance

        :returns: twilio.rest.preview.hosted_numbers.authorization_document.dependent_hosted_number_order.DependentHostedNumberOrderInstance
        :rtype: twilio.rest.preview.hosted_numbers.authorization_document.dependent_hosted_number_order.DependentHostedNumberOrderInstance
        """
        super(DependentHostedNumberOrderInstance, self).__init__(version)

        # Marshaled Properties
        self._properties = {
            'sid': payload['sid'],
            'account_sid': payload['account_sid'],
            'incoming_phone_number_sid': payload['incoming_phone_number_sid'],
            'address_sid': payload['address_sid'],
            'signing_document_sid': payload['signing_document_sid'],
            'phone_number': payload['phone_number'],
            'capabilities': payload['capabilities'],
            'friendly_name': payload['friendly_name'],
            'unique_name': payload['unique_name'],
            'status': payload['status'],
            'failure_reason': payload['failure_reason'],
            'date_created': deserialize.iso8601_datetime(payload['date_created']),
            'date_updated': deserialize.iso8601_datetime(payload['date_updated']),
            'verification_attempts': deserialize.integer(payload['verification_attempts']),
            'email': payload['email'],
            'cc_emails': payload['cc_emails'],
            'verification_type': payload['verification_type'],
            'verification_document_sid': payload['verification_document_sid'],
            'extension': payload['extension'],
            'call_delay': deserialize.integer(payload['call_delay']),
            'verification_code': payload['verification_code'],
            'verification_call_sids': payload['verification_call_sids'],
        }

        # Context
        self._context = None
        self._solution = {'signing_document_sid': signing_document_sid, }

    @property
    def sid(self):
        """
        :returns: HostedNumberOrder sid.
        :rtype: unicode
        """
        return self._properties['sid']

    @property
    def account_sid(self):
        """
        :returns: Account sid.
        :rtype: unicode
        """
        return self._properties['account_sid']

    @property
    def incoming_phone_number_sid(self):
        """
        :returns: IncomingPhoneNumber sid.
        :rtype: unicode
        """
        return self._properties['incoming_phone_number_sid']

    @property
    def address_sid(self):
        """
        :returns: Address sid.
        :rtype: unicode
        """
        return self._properties['address_sid']

    @property
    def signing_document_sid(self):
        """
        :returns: LOA document sid.
        :rtype: unicode
        """
        return self._properties['signing_document_sid']

    @property
    def phone_number(self):
        """
        :returns: An E164 formatted phone number.
        :rtype: unicode
        """
        return self._properties['phone_number']

    @property
    def capabilities(self):
        """
        :returns: A mapping of phone number capabilities.
        :rtype: unicode
        """
        return self._properties['capabilities']

    @property
    def friendly_name(self):
        """
        :returns: A human readable description of this resource.
        :rtype: unicode
        """
        return self._properties['friendly_name']

    @property
    def unique_name(self):
        """
        :returns: A unique, developer assigned name of this HostedNumberOrder.
        :rtype: unicode
        """
        return self._properties['unique_name']

    @property
    def status(self):
        """
        :returns: The Status of this HostedNumberOrder.
        :rtype: DependentHostedNumberOrderInstance.Status
        """
        return self._properties['status']

    @property
    def failure_reason(self):
        """
        :returns: Why a hosted_number_order reached status "action-required"
        :rtype: unicode
        """
        return self._properties['failure_reason']

    @property
    def date_created(self):
        """
        :returns: The date this HostedNumberOrder was created.
        :rtype: datetime
        """
        return self._properties['date_created']

    @property
    def date_updated(self):
        """
        :returns: The date this HostedNumberOrder was updated.
        :rtype: datetime
        """
        return self._properties['date_updated']

    @property
    def verification_attempts(self):
        """
        :returns: The number of attempts made to verify ownership of the phone number.
        :rtype: unicode
        """
        return self._properties['verification_attempts']

    @property
    def email(self):
        """
        :returns: Email.
        :rtype: unicode
        """
        return self._properties['email']

    @property
    def cc_emails(self):
        """
        :returns: A list of emails.
        :rtype: unicode
        """
        return self._properties['cc_emails']

    @property
    def verification_type(self):
        """
        :returns: The method used for verifying ownership of the number to be hosted.
        :rtype: DependentHostedNumberOrderInstance.VerificationType
        """
        return self._properties['verification_type']

    @property
    def verification_document_sid(self):
        """
        :returns: Verification Document Sid.
        :rtype: unicode
        """
        return self._properties['verification_document_sid']

    @property
    def extension(self):
        """
        :returns: Phone extension to use for ownership verification call.
        :rtype: unicode
        """
        return self._properties['extension']

    @property
    def call_delay(self):
        """
        :returns: Seconds (0-30) to delay ownership verification call by.
        :rtype: unicode
        """
        return self._properties['call_delay']

    @property
    def verification_code(self):
        """
        :returns: The digits passed during the ownership verification call.
        :rtype: unicode
        """
        return self._properties['verification_code']

    @property
    def verification_call_sids(self):
        """
        :returns: List of IDs for ownership verification calls.
        :rtype: unicode
        """
        return self._properties['verification_call_sids']

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Preview.HostedNumbers.DependentHostedNumberOrderInstance>'
