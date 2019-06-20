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

    def set_stp_vlan_forward_timer(self, vlan, fwd_timer):
        valid_fwd_time = '<4-30>'

        if fwd_timer in range(4,31):
            cmd = 'spanning-tree vlan %s forward-time %s' %(vlan, fwd_timer)
            output = self.iosapi.bcp_send_config_set(self.iosapi.netmiko_session, cmd)
            self.iosapi.bcp_log("info", "(%s) set_stp_vlan_forward_timer() : Attempting to set VLAN %s STP fwd_timer to %s" %(__name__, vlan, fwd_timer))
            return(output)
        else:
            self.iosapi.bcp_log("info", "(%s) set_stp_vlan_forward_timer() : Failed to set vlan %s STP fwd_timer to %s" %(__name__, vlan, fwd_timer))
            return("%s is not a valid value. Foward Timer range is between %s" %(fwd_timer, valid_fwd_time))

    def set_stp_vlan_hello_timer(self, vlan, hello_timer):
        valid_hello_timer = '<1-10>'

        if hello_timer in range(1,11):
            cmd = 'spanning-tree vlan %s hello-time %s' %(vlan, hello_timer)
            output = self.iosapi.bcp_send_config_set(self.iosapi.netmiko_session, cmd)
            self.iosapi.bcp_log("info", "(%s) set_stp_vlan_hello_timer() : Attempting to set vlan %s STP hello_timer to %s" %(__name__, vlan, hello_timer))
            return(output)
        else:
            self.iosapi.bcp_log("info", "(%s) set_stp_vlan_hello_timer() : Failed to set vlan %s STP hello_timer to %s" %(__name__, vlan, hello_timer))
            return("%s is not a valid value. Hello Timer range is between %s" %(hello_timer, valid_hello_timer))

    def set_stp_vlan_max_age(self, vlan, max_age):
        valid_max_age = '<6-40>'

        if max_age in range(6,41):
            cmd = 'spanning-tree vlan %s max-age %s' %(vlan, max_age)
            output = self.iosapi.bcp_send_config_set(self.iosapi.netmiko_session, cmd)
            self.iosapi.bcp_log("info", "(%s) set_stp_vlan_max_age() : Attempting to set vlan %s STP max_age to %s" %(__name__, vlan, max_age))
            return(output)
        else:
            self.iosapi.bcp_log("info", "(%s) set_stp_vlan_max_age() : Failed to set vlan %s STP max_age to %s" %(__name__, vlan, max_age))
            return("%s is not a valid value. Max Age range is between %s" %(max_age, valid_max_age))

    def set_stp_vlan_priority(self, vlan, priority):
        allowed_priorities = [0, 4096, 8192, 12288, 16384, 20480, 24576, 28672,
                             32768, 36864, 40960, 45046, 49152, 53248, 57344, 61440]

        if priority in allowed_priorites:
            cmd = 'spanning-tree vlan %s priority %s' %(vlan, priority)
            output = self.iosapi.bcp_send_config_command(self.iosapi.netmiko_session, cmd)
            self.iosapi.bcp_log("info", "(%s) set_stp_vlan_pirority() : Setting VLAN %s priority to %s" %(__name__, vlan, priority))
            return(output)
        else:
            return("%s is not a valid value. \nPriority must be increments of 4096, allowed priorities are: \n%s" %(priority, allowed_priorities))

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