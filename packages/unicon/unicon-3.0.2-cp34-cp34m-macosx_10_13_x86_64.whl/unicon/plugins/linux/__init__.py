"""
Module:
    unicon.plugins.linux

Authors:
    ATS TEAM (ats-dev@cisco.com, CSG( STEP) - India)

Description:
    This subpackage implements Linux
"""

import time

from unicon.bases.linux.connection import BaseLinuxConnection
from unicon.bases.linux.connection_provider import BaseLinuxConnectionProvider
from unicon.eal.dialogs import Dialog
from unicon.plugins.linux.patterns import LinuxPatterns
from unicon.plugins.linux.statemachine import LinuxStateMachine
#from unicon.settings import Settings
from unicon.plugins.linux import service_implementation as lnx_svc
from unicon.plugins.generic import service_implementation as svc
from unicon.core.errors import ConnectionError
from .settings import LinuxSettings

p = LinuxPatterns()


def wait_and_enter(spawn):
    time.sleep(0.5)  # otherwise newline is sometimes lost?
    spawn.sendline()

def wait_and_send_yes(spawn):
    time.sleep(0.1)
    spawn.sendline('yes')

def password_handler(spawn, context):
    spawn.sendline(context['password'])

def username_handler(spawn, context):
    spawn.sendline(context['username'])

def permission_denied(spawn):
    """ handles connection refused scenarios
    """
    raise ConnectionError('Permission denied for device "%s"' % (str(spawn),))

def connection_refused(spawn):
    """ handles connection refused scenarios
    """
    raise ConnectionError('Connection refused to device "%s"' % (str(spawn),))

class LinuxConnectionProvider(BaseLinuxConnectionProvider):
    """
        Connection provided class for Linux connections.
    """
    def get_connection_dialog(self):
        return Dialog([
            [p.hit_enter,
                wait_and_enter,
                None, True, False],
            [p.continue_connect,
                wait_and_send_yes,
                None, True, False],
            [p.username,
                username_handler,
                None, True, False],
            [p.password,
                password_handler,
                None, True, False],
            [p.permission_denied,
                permission_denied,
                None, False, False],
            [p.connection_refused,
                connection_refused,
                None, False, False]
        ])


class LinuxServiceList:
    """ Linux services. """

    def __init__(self):
        self.send = svc.Send
        self.sendline = svc.Sendline
        self.expect = svc.Expect
        self.expect_log = svc.ExpectLogging
        self.log_user = svc.LogUser
        self.execute = lnx_svc.Execute
        self.ping = lnx_svc.Ping


class LinuxConnection(BaseLinuxConnection):
    """
        Connection class for Linux connections.
    """
    os = 'linux'
    series = None
    chassis_type = 'single_rp'
    # TODO Recheck this single_rp value for linux
    state_machine_class = LinuxStateMachine
    connection_provider_class = LinuxConnectionProvider
    subcommand_list = LinuxServiceList
    settings = LinuxSettings()
