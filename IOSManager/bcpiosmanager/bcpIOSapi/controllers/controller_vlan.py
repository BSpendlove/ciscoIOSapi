from bcpIOSapi.iosapi import IOSAPI

class VlanAPI(object):
    def __init__(self, iosapi=None):
        if iosapi:
            self.iosapi = iosapi
        else:
            self.iosapi = IOSAPI()

    #Get Functions
    def get_vlans(self):
        cmd = 'show vlan brief'
        output = self.iosapi.bcp_send_command(self.iosapi.netmiko_session, cmd)
        self.iosapi.bcp_log("info", "(%s) get_vlans() : Attempting to retreive all VLANs" %(__name__))
        return(self.iosapi.textfsm_extractor('cisco_ios_show_vlan.template', output))

    def get_vlan_id(self, vlanid):
        cmd = 'show vlan id %s' %(vlanid)
        output = self.iosapi.bcp_send_command(self.iosapi.netmiko_session, cmd)
        self.iosapi.bcp_log("info", "(%s) get_vlan_id() : Attempting to retreive VLAN ID %s" %(__name__, vlanid))
        return(self.iosapi.textfsm_extractor('cisco_ios_show_vlan.template', output))