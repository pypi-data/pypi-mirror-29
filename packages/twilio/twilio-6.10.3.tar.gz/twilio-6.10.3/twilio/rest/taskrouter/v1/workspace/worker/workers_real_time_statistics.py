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


class WorkersRealTimeStatisticsList(ListResource):
    """  """

    def __init__(self, version, workspace_sid):
        """
        Initialize the WorkersRealTimeStatisticsList

        :param Version version: Version that contains the resource
        :param workspace_sid: The workspace_sid

        :returns: twilio.rest.taskrouter.v1.workspace.worker.workers_real_time_statistics.WorkersRealTimeStatisticsList
        :rtype: twilio.rest.taskrouter.v1.workspace.worker.workers_real_time_statistics.WorkersRealTimeStatisticsList
        """
        super(WorkersRealTimeStatisticsList, self).__init__(version)

        # Path Solution
        self._solution = {'workspace_sid': workspace_sid, }

    def get(self):
        """
        Constructs a WorkersRealTimeStatisticsContext

        :returns: twilio.rest.taskrouter.v1.workspace.worker.workers_real_time_statistics.WorkersRealTimeStatisticsContext
        :rtype: twilio.rest.taskrouter.v1.workspace.worker.workers_real_time_statistics.WorkersRealTimeStatisticsContext
        """
        return WorkersRealTimeStatisticsContext(self._version, workspace_sid=self._solution['workspace_sid'], )

    def __call__(self):
        """
        Constructs a WorkersRealTimeStatisticsContext

        :returns: twilio.rest.taskrouter.v1.workspace.worker.workers_real_time_statistics.WorkersRealTimeStatisticsContext
        :rtype: twilio.rest.taskrouter.v1.workspace.worker.workers_real_time_statistics.WorkersRealTimeStatisticsContext
        """
        return WorkersRealTimeStatisticsContext(self._version, workspace_sid=self._solution['workspace_sid'], )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Taskrouter.V1.WorkersRealTimeStatisticsList>'


class WorkersRealTimeStatisticsPage(Page):
    """  """

    def __init__(self, version, response, solution):
        """
        Initialize the WorkersRealTimeStatisticsPage

        :param Version version: Version that contains the resource
        :param Response response: Response from the API
        :param workspace_sid: The workspace_sid

        :returns: twilio.rest.taskrouter.v1.workspace.worker.workers_real_time_statistics.WorkersRealTimeStatisticsPage
        :rtype: twilio.rest.taskrouter.v1.workspace.worker.workers_real_time_statistics.WorkersRealTimeStatisticsPage
        """
        super(WorkersRealTimeStatisticsPage, self).__init__(version, response)

        # Path Solution
        self._solution = solution

    def get_instance(self, payload):
        """
        Build an instance of WorkersRealTimeStatisticsInstance

        :param dict payload: Payload response from the API

        :returns: twilio.rest.taskrouter.v1.workspace.worker.workers_real_time_statistics.WorkersRealTimeStatisticsInstance
        :rtype: twilio.rest.taskrouter.v1.workspace.worker.workers_real_time_statistics.WorkersRealTimeStatisticsInstance
        """
        return WorkersRealTimeStatisticsInstance(
            self._version,
            payload,
            workspace_sid=self._solution['workspace_sid'],
        )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Taskrouter.V1.WorkersRealTimeStatisticsPage>'


class WorkersRealTimeStatisticsContext(InstanceContext):
    """  """

    def __init__(self, version, workspace_sid):
        """
        Initialize the WorkersRealTimeStatisticsContext

        :param Version version: Version that contains the resource
        :param workspace_sid: The workspace_sid

        :returns: twilio.rest.taskrouter.v1.workspace.worker.workers_real_time_statistics.WorkersRealTimeStatisticsContext
        :rtype: twilio.rest.taskrouter.v1.workspace.worker.workers_real_time_statistics.WorkersRealTimeStatisticsContext
        """
        super(WorkersRealTimeStatisticsContext, self).__init__(version)

        # Path Solution
        self._solution = {'workspace_sid': workspace_sid, }
        self._uri = '/Workspaces/{workspace_sid}/Workers/RealTimeStatistics'.format(**self._solution)

    def fetch(self, task_channel=values.unset):
        """
        Fetch a WorkersRealTimeStatisticsInstance

        :param unicode task_channel: The task_channel

        :returns: Fetched WorkersRealTimeStatisticsInstance
        :rtype: twilio.rest.taskrouter.v1.workspace.worker.workers_real_time_statistics.WorkersRealTimeStatisticsInstance
        """
        params = values.of({'TaskChannel': task_channel, })

        payload = self._version.fetch(
            'GET',
            self._uri,
            params=params,
        )

        return WorkersRealTimeStatisticsInstance(
            self._version,
            payload,
            workspace_sid=self._solution['workspace_sid'],
        )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Taskrouter.V1.WorkersRealTimeStatisticsContext {}>'.format(context)


class WorkersRealTimeStatisticsInstance(InstanceResource):
    """  """

    def __init__(self, version, payload, workspace_sid):
        """
        Initialize the WorkersRealTimeStatisticsInstance

        :returns: twilio.rest.taskrouter.v1.workspace.worker.workers_real_time_statistics.WorkersRealTimeStatisticsInstance
        :rtype: twilio.rest.taskrouter.v1.workspace.worker.workers_real_time_statistics.WorkersRealTimeStatisticsInstance
        """
        super(WorkersRealTimeStatisticsInstance, self).__init__(version)

        # Marshaled Properties
        self._properties = {
            'account_sid': payload['account_sid'],
            'activity_statistics': payload['activity_statistics'],
            'total_workers': deserialize.integer(payload['total_workers']),
            'workspace_sid': payload['workspace_sid'],
            'url': payload['url'],
        }

        # Context
        self._context = None
        self._solution = {'workspace_sid': workspace_sid, }

    @property
    def _proxy(self):
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions.  All instance actions are proxied to the context

        :returns: WorkersRealTimeStatisticsContext for this WorkersRealTimeStatisticsInstance
        :rtype: twilio.rest.taskrouter.v1.workspace.worker.workers_real_time_statistics.WorkersRealTimeStatisticsContext
        """
        if self._context is None:
            self._context = WorkersRealTimeStatisticsContext(
                self._version,
                workspace_sid=self._solution['workspace_sid'],
            )
        return self._context

    @property
    def account_sid(self):
        """
        :returns: The account_sid
        :rtype: unicode
        """
        return self._properties['account_sid']

    @property
    def activity_statistics(self):
        """
        :returns: The activity_statistics
        :rtype: dict
        """
        return self._properties['activity_statistics']

    @property
    def total_workers(self):
        """
        :returns: The total_workers
        :rtype: unicode
        """
        return self._properties['total_workers']

    @property
    def workspace_sid(self):
        """
        :returns: The workspace_sid
        :rtype: unicode
        """
        return self._properties['workspace_sid']

    @property
    def url(self):
        """
        :returns: The url
        :rtype: unicode
        """
        return self._properties['url']

    def fetch(self, task_channel=values.unset):
        """
        Fetch a WorkersRealTimeStatisticsInstance

        :param unicode task_channel: The task_channel

        :returns: Fetched WorkersRealTimeStatisticsInstance
        :rtype: twilio.rest.taskrouter.v1.workspace.worker.workers_real_time_statistics.WorkersRealTimeStatisticsInstance
        """
        return self._proxy.fetch(task_channel=task_channel, )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Taskrouter.V1.WorkersRealTimeStatisticsInstance {}>'.format(context)
