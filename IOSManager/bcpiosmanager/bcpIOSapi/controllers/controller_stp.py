from bcpIOSapi.iosapi import IOSAPI

class StpAPI(object):
    def __init__(self, iosapi=None):
        if iosapi:
            self.iosapi = iosapi
        else:
            self.iosapi = IOSAPI()

    #Change Functions
    def set_stp_mode(self, mode):
        modes = ['mst', 'pvst', 'rapid-pvst']

        cmd = 'spanning-tree mode %s' %(mode)

        if mode in modes:
            output = self.iosapi.bcp_send_config_command(self.iosapi.netmiko_session, cmd)
            self.iosapi.bcp_log("info", "(%s) set_stp_mode() : Attempting to set STP mode to %s" %(__name__, mode))

            return(output)
        else:
            print("Mode %s is not valid" %(mode))
            self.iosapi.bcp_log("info", "(%s) set_stp_mode() : Failed - mode %s doesn't exist" %(__name__, mode))

    def set_stp_priority(self, vlan, priority):
        allowed_priorities = [0, 4096, 8192, 12288, 16384, 20480, 24576, 28672,
                             32768, 36864, 40960, 45046, 49152, 53248, 57344, 61440]

        if priority in allowed_priorites:
            cmd = 'spanning-tree vlan %s priority %s' %(vlan, priority)
            output = self.iosapi.bcp_send_config_command(self.iosapi.netmiko_session, cmd)
            self.iosapi.bcp_log("info", "(%s) set_stp_pirority() : Setting VLAN %s priority to %s" %(__name__, vlan, priority))
            return(output)
        else:
            print("%s is not a valid value. \nPriority must be increments of 4096, allowed priorities are: \n%s" %(priority, allowed_priorities))
            return

    #Gather Functions

    def get_stp_mode(self):
        stp_mode = self.get_stp_bridge()['protocol']

        if stp_mode == 'ieee':
            stp_mode = 'PVST+'

        if stp_mode == 'rstp':
            stp_mode = 'RPVST+'

        if stp_mode == 'mstp':
            stp_mode = 'MST'

        self.iosapi.bcp_log("info", "(%s) get_stp_mode() : Attempting to retreive STP mode" %(__name__))
        return(stp_mode)

    def get_stp_bridge(self):
        cmd = 'show spanning-tree bridge'
        output = self.iosapi.bcp_send_command(self.iosapi.netmiko_session, cmd)
        self.iosapi.bcp_log("info", "(%s) get_stp_bridge() : Attempting to retreive STP Bridge information" %(__name__))
        return(self.iosapi.textfsm_extractor('cisco_ios_show_stp_bridge.template', output)[0])