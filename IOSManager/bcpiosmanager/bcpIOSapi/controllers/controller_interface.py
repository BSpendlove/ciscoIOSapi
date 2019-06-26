from bcpIOSapi.iosapi import IOSAPI
from ciscoconfparse import CiscoConfParse

class InterfaceAPI(object):
    def __init__(self, iosapi=None):
        if iosapi:
            self.iosapi = iosapi
        else:
            self.iosapi = IOSAPI()
     
    #Set Commands
    def set_interface_ip(self, interface, ip, mask):
        cmds = ['interface %s' %(interface), 'ip address %s %s' %(ip, mask)]

        output = self.iosapi.bcp_send_config_command(self.iosapi.netmiko_session, cmds)
        self.iosapi.bcp_log("info", "(%s) set_interface_ip() : Attempting to set interface %s IP" %(__name__, interface))
        return(output)

    def set_l2_interface_mode(self, interface, mode):
        modes = ['access', 'trunk']

        if mode not in modes:
            print("%s is an Invalid mode... Valid modes are: %s" %(mode, modes))
            self.iosapi.bcp_log("info", "(%s) set_l2_interface_mode() : Invalid mode %s for interface %s" %(__name__, mode, interface))

        cmds = ['interface %s' %(interface), 'switchport mode %s' %(mode)]

        output = self.iosapi.bcp_send_config_command(self.iosapi.netmiko_session, cmds)
        self.iosapi.bcp_log("info", "(%s) set_l2_interface_mode() : Attempting to set interface %s to %s" %(__name__, interface, mode))

        if 'encapsulation is "Auto"' in output:
            self.iosapi.bcp_log("info", "(%s) set_l2_interface_mode() : Interface with encapsulation set to Auto can not be configured to Trunk mode" %(__name__))
            return(output)
        else:
            return(output)

    def set_l2_stp_portfast(self, interface, enabled=True, mode='access'):
        cmds = ['interface %s' %(interface)]

        if mode == 'access':
            cmds.append('spanning-tree portfast')
        else:
            cmds.append('spanning-tree portfast trunk')

        output = self.iosapi.bcp_send_config_command(self.iosapi.netmiko_session, cmds)
        self.iosapi.bcp_log("info", "(%s) set_l2_stp_portfast() : Attempting to set interface %s portfast state: Enabled = %s, Mode = %s" %(__name__, interface, enabled, mode))

        return(output)

    #Get Commands
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

    def get_interfaces_only(self):
        interfaces = {}
        interface_list = []

        output = self.get_interfaces()

        for interface in output:
            interface_list.append(interface['interface'])

        interfaces['interfaces'] = interface_list

        return(interfaces)

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