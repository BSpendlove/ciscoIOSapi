from bcpIOSapi.iosapi import IOSAPI
from pprint import pprint

class CdpAPI(object):
    def __init__(self, iosapi=None):
        if iosapi:
            self.iosapi = iosapi
        else:
            self.iosapi = IOSAPI()

    def set_cdp(self, enabled=True, version=2):
        cmds = []

        if enabled:
            cmds.append('cdp run')
            if version == 2:
                cmds.append('cdp advertise-v2')
            else:
                cmds.append('no cdp advertise-v2')

            self.iosapi.bcp_log("info", "(%s) set_cdp() : Attempting to set CDP enabled=%s version=%s" %(__name__, enabled, version))
        else:
            cmds.append('no cdp run')
            self.iosapi.bcp_log("info", "(%s) set_cdp() : Attempting to set CDP enabled=%s" %(__name__, enabled))

        output = self.iosapi.bcp_send_config_command(self.iosapi.netmiko_session, cmds)
        return(output)

    def set_cdp_timer(self, time=60):
        cdp_valid_range = '<5-254>'
        cmd = 'cdp timer %s' %(time)

        if time not in range(5,255):
            print("CDP Time %s is invalid, valid range is %s" %(cdp_valid_range))
            return
        else:
            output = self.iosapi.bcp_send_config_command(self.iosapi.netmiko_session, cmd)
            self.iosapi.bcp_log("info", "(%s) set_cdp_timer() : Attempting to set CDP timer" %(__name__))
            return(output)

    def get_cdp_neighbors_detail(self):
        cmd = 'show cdp neighbors detail'
        output = self.iosapi.bcp_send_command(self.iosapi.netmiko_session, cmd)
        self.iosapi.bcp_log("info", "(%s) get_cdp_neighbors_detail() : Attempting to retreive CDP detailed facts" %(__name__))
        return(self.iosapi.textfsm_extractor('cisco_ios_show_cdp_neighbors_detail.template', output))
