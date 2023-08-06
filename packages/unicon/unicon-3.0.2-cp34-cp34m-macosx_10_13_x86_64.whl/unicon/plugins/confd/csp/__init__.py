__copyright__ = "# Copyright (c) 2017 by cisco Systems, Inc. All rights reserved."
__author__ = "Dave Wapstra <dwapstra@cisco.com>"


from unicon.plugins.confd import ConfdServiceList, ConfdConnection, ConfdConnectionProvider
from .statemachine import CspStateMachine
from .settings import CspSettings


class CspServiceList(ConfdServiceList):
    def __init__(self):
        super().__init__()
        delattr(self, 'cli_style')


class CspSingleRPConnection(ConfdConnection):
    os = 'confd'
    series = 'csp'
    chassis_type = 'single_rp'
    state_machine_class = CspStateMachine
    connection_provider_class = ConfdConnectionProvider
    subcommand_list = CspServiceList
    settings = CspSettings()
