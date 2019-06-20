from bcpIOSapi.iosapi import IOSAPI

class MacAddressAPI(object):
    def __init__(self, iosapi=None):
        if iosapi:
            self.iosapi = iosapi
        else:
            self.iosapi = IOSAPI()

    def get_mac_address_table(self):
        cmd = 'show mac address-table'
        output = self.iosapi.bcp_send_command(self.iosapi.netmiko_session, cmd)
        self.iosapi.bcp_log("info", "(%s) get_mac_address_table() : Attempting to get MAC address table" %(__name__))
        return (self.iosapi.textfsm_extractor('cisco_ios_show_mac_address-table.template', output))

    def get_mac_address_interface(self, interface):
        cmd = 'show mac address-table interface %s' %(interface)
        output = self.iosapi.bcp_send_command(self.iosapi.netmiko_session, cmd)
        self.iosapi.bcp_log("info", "(%s) get_mac_address_interface() : Attempting to get MAC addresses from interface %s" %(__name__, interface))
        return (self.iosapi.textfsm_extractor('cisco_ios_show_mac_address-table.template', output))

    def get_mac_address_vlan(self, vlan):
        if vlan not in range(0, 4095):
            return
        cmd = 'show mac address-table vlan %s' %(vlan)
        output = self.iosapi.bcp_send_command(self.iosapi.netmiko_session, cmd)
        self.iosapi.bcp_log("info", "(%s) get_mac_address_vlan() : Attempting to get MAC addresses from VLAN %s" %(__name__, vlan))
        return (self.iosapi.textfsm_extractor('cisco_ios_show_mac_address-table.template', output))

    def get_mac_address(self, macaddr):
        cmd = 'show mac address-table address %s' %(macaddr)
        output = self.iosapi.bcp_send_command(self.iosapi.netmiko_session, cmd)
        self.iosapi.bcp_log("info", "(%s) get_mac_address() : Attempting to get MAC address %s" %(__name__, macaddr))
        return (self.iosapi.textfsm_extractor('cisco_ios_show_mac_address-table.template', output))