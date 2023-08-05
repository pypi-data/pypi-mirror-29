# coding=utf-8
"""
This code was generated by
\ / _    _  _|   _  _
 | (_)\/(_)(_|\/| |(/_  v1.0.0
      /       /
"""

from twilio.base.version import Version
from twilio.rest.preview.deployed_devices.fleet import FleetList


class DeployedDevices(Version):

    def __init__(self, domain):
        """
        Initialize the DeployedDevices version of Preview

        :returns: DeployedDevices version of Preview
        :rtype: twilio.rest.preview.deployed_devices.DeployedDevices.DeployedDevices
        """
        super(DeployedDevices, self).__init__(domain)
        self.version = 'DeployedDevices'
        self._fleets = None

    @property
    def fleets(self):
        """
        :rtype: twilio.rest.preview.deployed_devices.fleet.FleetList
        """
        if self._fleets is None:
            self._fleets = FleetList(self)
        return self._fleets

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Preview.DeployedDevices>'
