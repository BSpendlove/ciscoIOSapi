from bcpIOSapi.iosapi import IOSAPI
from ciscoconfparse import CiscoConfParse

class InterfaceAPI(object):
    def __init__(self, iosapi=None):
        if iosapi:
            self.iosapi = iosapi
        else:
            self.iosapi = IOSAPI()
     
    def get_interfaces(self):
        cmd = 'show interfaces'
        output = self.iosapi.bcp_send_command(self.iosapi.netmiko_session, cmd)
        self.iosapi.bcp_log("info", "(%s) get_interfaces() : Attempting to run show interfaces" %(__name__))
        return(self.iosapi.textfsm_extractor('cisco_ios_show_interfaces.template', output))

    def get_interfaces_config(self):
        dict_interfaces = {}
        list_interface_config = []
        

        cmd = 'show running-config'
        running_configuration = self.iosapi.bcp_send_command(self.iosapi.netmiko_session, cmd)
        self.iosapi.bcp_log("info", "(%s) get_interfaces_config() : Attempting to get interface config" %(__name__))

        parser = CiscoConfParse(running_configuration.splitlines())

        interfaces = self.get_interfaces()

        for interface in interfaces:
            interface_config = parser.find_objects(r'interface %s$' %(interface['interface']))

            for interface_object in interface_config:
                list_interface_config = interface_object.ioscfg

            dict_interfaces[interface['interface']] = list_interface_config

        return(dict_interfaces)

    def get_interfaces_description(self):
        cmd = 'show interfaces description'
        output = self.iosapi.bcp_send_command(self.iosapi.netmiko_session, cmd)
        self.iosapi.bcp_log("info", "(%s) get_interfaces_description() : Attempting to get interfaces description" %(__name__))
        return(self.iosapi.textfsm_extractor('cisco_ios_show_interfaces_description.template', output))

    def get_interfaces_status(self):
        cmd = 'show interfaces status'
        output = self.iosapi.bcp_send_command(self.iosapi.netmiko_session, cmd)
        self.iosapi.bcp_log("info", "(%s) get_interfaces_status() : Attempting to get interfaces status" %(__name__))
        return(self.iosapi.textfsm_extractor('cisco_ios_show_interfaces_status.template', output))

    ''' Textfsm template is broke...
    def get_ip_int(self):
        cmd = 'show ip interface'
        output = self.iosapi.bcp_send_command(self.iosapi.netmiko_session, cmd)
        return(self.iosapi.textfsm_extractor('cisco_ios_show_ip_interface.template', output))
    '''

    def get_ip_int_brief(self):
        cmd = 'show ip interface brief'
        output = self.iosapi.bcp_send_command(self.iosapi.netmiko_session, cmd)
        self.iosapi.bcp_log("info", "(%s) get_ip_int_brief() : Attempting to run show ip int brief" %(__name__))
        return(self.iosapi.textfsm_extractor('cisco_ios_show_ip_interface_brief.template', output))