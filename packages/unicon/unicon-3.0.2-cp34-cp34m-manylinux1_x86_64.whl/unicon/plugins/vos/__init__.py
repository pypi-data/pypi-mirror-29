__copyright__ = "# Copyright (c) 2017 by cisco Systems, Inc. All rights reserved."
__author__ = "Dave Wapstra <dwapstra@cisco.com>"

from unicon.plugins.generic import GenericSingleRpConnection, service_implementation as svc
from unicon.plugins.generic.connection_provider import GenericSingleRpConnectionProvider

from unicon.plugins.generic import ServiceList, service_implementation as svc
from . import service_implementation as vos_svc
from .statemachine import VosStateMachine
from .settings import VosSettings


class VosConnectionProvider(GenericSingleRpConnectionProvider):
    """
        Connection provider class for vos connections.
    """
    def set_init_commands(self):
        con = self.connection

        if con.init_exec_commands is not None:
            self.init_exec_commands = con.init_exec_commands
        else:
            self.init_exec_commands = []

        if con.init_config_commands is not None:
            self.init_config_commands = con.init_config_commands
        else:
            self.init_config_commands = []

    def init_handle(self):
        con = self.connection
        con._is_connected = True
        con.connection_timeout = 300
        self.execute_init_commands()


class VosServiceList(ServiceList):
    """ vos services. """

    def __init__(self):
        self.send = svc.Send
        self.sendline = svc.Sendline
        self.expect = svc.Expect
        self.execute = vos_svc.Execute
        self.expect_log = svc.ExpectLogging
        self.log_user = svc.LogUser


class VosConnection(GenericSingleRpConnection):
    """
        Connection class for vos connections.
    """
    os = 'vos'
    series = None
    chassis_type = 'single_rp'
    state_machine_class = VosStateMachine
    connection_provider_class = VosConnectionProvider
    subcommand_list = VosServiceList
    settings = VosSettings()
