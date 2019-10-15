from bcpIOSapi.iosapi import IOSAPI
from ciscoconfparse import CiscoConfParse
import json

class InterfaceAPI(object):
    def __init__(self, iosapi=None):
        if iosapi:
            self.iosapi = iosapi
        else:
            self.iosapi = IOSAPI()
     
    #Replace commands
    def replace_interfaces_access_vlan(self, current_vlan, new_vlan, backup=True):

        """
            Replaces all interfaces in a specified VLAN that are set as an administrative mode Access, to a different VLAN.
            > current_vlan  -   VLAN to match access ports currently configured in this vlan
            > new_vlan      -   VLAN to assign ports
            > backup        -   Previous configuration will be saved for every interface in the script directory for the device (Default: True)

            Example:
            replace_interfaces_access_vlan(10,20)
        """

        all_interfaces = self.get_interfaces_switchport()

        current_interface_config = self.get_interfaces_config()
        interface_backup = []
        
        config_set = []

        for interface in all_interfaces:
            if interface['access_vlan'] == 'none':
                pass

            elif interface['administrative_mode'] == 'static access' and int(interface['access_vlan']) == current_vlan:

                interface_backup.append(current_interface_config[interface['interface']])
                print("Will change port: %s from ACCESS VLAN %s to ACCESS VLAN %s" %(interface['interface'], current_vlan, new_vlan))

                config_set.append('interface %s' %(interface['interface']))
                config_set.append(' switchport access vlan %s' %(new_vlan))

                self.iosapi.bcp_log("info", "(%s) replace_interfaces_access_vlan() : Attempting to replace interface %s access VLAN from %s to %s" %(__name__, interface['interface'], current_vlan, new_vlan))

        if backup:
            config_format = {
                'old_configuration' : interface_backup,
                'new_configuration' : config_set }

            self.iosapi.create_backup('replace_interfaces_access_vlan', json.dumps(config_format, indent=4, sort_keys=True))

        return(self.iosapi.bcp_send_config_command(self.iosapi.netmiko_session, config_set))

    def replace_interfaces_voice_vlan(self, current_vlan, new_vlan, backup=True):
        
        """
            Replaces the voice VLAN for all interfaces configured with the specified current voice vlan
            > current_vlan  -   Current VOICE Vlan to Match
            > new_vlan      -   VLAN to assign ports
            > backup        -   Previous configuration will be saved for every interface in the script directory for the device (Default: True)

            Example:
            replace_interfaces_voice_vlan(101, 201)
        """

        all_interfaces = self.get_interfaces_switchport()

        current_interface_config = self.get_interfaces_config()
        interface_backup = []

        config_set = []

        for interface in all_interfaces:
            if interface['voice_vlan'] == 'none':
                pass

            elif interface['administrative_mode'] == 'static access' and int(interface['voice_vlan']) == current_vlan:

                interface_backup.append(current_interface_config[interface['interface']])
                print("Will change port: %s from VOICE VLAN %s to VOICE VLAN %s" %(interface['interface'], current_vlan, new_vlan))

                config_set.append('interface %s' %(interface['interface']))
                config_set.append(' switchport voice vlan %s' %(new_vlan))

                self.iosapi.bcp_log("info", "(%s) replace_interfaces_voice_vlan() : Attempting to replace interface %s voice VLAN from %s to %s" %(__name__, interface['interface'], current_vlan, new_vlan))

        if backup:
            config_format = {
                'old_configuration' : interface_backup,
                'new_configuration' : config_set }

            self.iosapi.create_backup('replace_interfaces_voice_vlan', json.dumps(config_format, indent=4, sort_keys=True))

        return(self.iosapi.bcp_send_config_command(self.iosapi.netmiko_session, config_set))

    #Set Commands
    def set_interface_ip(self, interface, ip, mask):

        """
            Configure IP Address on interface - Need to improve this function for checking etc..
            > interface     -   Interface syntax
            > ip            -   IP Address
            > mask          -   Subnet Mask

            Example:
            set_interface_ip('vlan100', '169.254.100.254', '255.255.255.0')
        """

        cmds = ['interface %s' %(interface), 'ip address %s %s' %(ip, mask)]

        output = self.iosapi.bcp_send_config_command(self.iosapi.netmiko_session, cmds)
        self.iosapi.bcp_log("info", "(%s) set_interface_ip() : Attempting to set interface %s IP" %(__name__, interface))
        return(output)

    def set_l2_interface_mode(self, interface, mode):

        """
            Set interface mode to either Access or Trunk
            > interface     -   Interface Syntax
            > mode          -   access or trunk

            Example:
            set_l2_interface_mode('g1/0/3', 'access')
        """

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

        """
            Set Portfast on either Access port or Trunk port (Need to improve this function for additional checking)
            > interface     -   Interface Syntax
            > enabled       -   Enable Portfast
            > mode          -   access or trunk (Default: access)

            Example:
            set_l2_stp_portfast('g1/0/2', True, 'access')
        """

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

        """
            Returns JSON type format for interfaces

            Example:
            get_interfaces()

            { 
                'address': '0cd6.448e.780f',
                'bandwidth': '1000000 Kbit',
                'bia': '0cd6.448e.780f',
                'delay': '10 usec',
                'description': '',
                'duplex': 'Full-duplex',
                'encapsulation': 'ARPA',
                'hardware_type': 'iGbE',
                'input_errors': '0',
                'input_packets': '0',
                'input_rate': '0',
                'interface': 'GigabitEthernet3/3',
                'ip_address': '',
                'last_input': 'never',
                'last_output': '00:00:00',
                'last_output_hang': 'never',
                'link_status': 'up',
                'mtu': '1500',
                'output_errors': '0',
                'output_packets': '4530',
                'output_rate': '0',
                'protocol_status': 'up (connected)',
                'queue_strategy': 'fifo',
                'speed': 'Auto-speed'
            }
        """

        cmd = 'show interfaces'

        output = self.iosapi.bcp_send_command(self.iosapi.netmiko_session, cmd)
        self.iosapi.bcp_log("info", "(%s) get_interfaces() : Attempting to run show interfaces" %(__name__))
        return(self.iosapi.textfsm_extractor('cisco_ios_show_interfaces.template', output))


    def get_interfaces_config(self):

        """
            Returns Dictionary with List of child configuration for every port (using CiscoConfParse)

            Example:
            get_interfaces_config()

            {
                'GigabitEthernet1/1': ['interface GigabitEthernet1/1',
                                        ' media-type rj45',
                                        ' negotiation auto',
                                        ' switchport mode access'],
                 'GigabitEthernet1/2': ['interface GigabitEthernet1/2',
                                        ' description ** Link to API Server **',
                                        ' switchport trunk allowed vlan 101-104,200',
                                        ' switchport trunk encapsulation dot1q',
                                        ' switchport trunk native vlan 101',
                                        ' switchport mode trunk',
                                        ' media-type rj45',
                                        ' negotiation auto',
                                        ' ip dhcp snooping trust'],
                'Tunnel10': ['interface Tunnel10',
                                        ' ip address 169.254.10.1 255.255.255.252',
                                        ' tunnel source GigabitEthernet0/0',
                                        ' tunnel key 100',
                                        ' tunnel protection ipsec profile vpn_s03'],
                }
        """

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

        """
            Returns JSON type format for interface descriptions and protocol/status

            Example:
            get_interfaces_description()

            {
                'descrip': '', 
                'port': 'Gi0/0', 
                'protocol': 'up', 
                'status': 'up'
            },
            {
                'descrip': '',
                'port': 'Gi0/1',
                'protocol': 'up',
                'status': 'up'
            },
            {
                'descrip': '** Link to API Server **',
                'port': 'Gi1/2',
                'protocol': 'up',
                'status': 'up'
            }
        """

        cmd = 'show interfaces description'

        output = self.iosapi.bcp_send_command(self.iosapi.netmiko_session, cmd)
        self.iosapi.bcp_log("info", "(%s) get_interfaces_description() : Attempting to get interfaces description" %(__name__))
        return(self.iosapi.textfsm_extractor('cisco_ios_show_interfaces_description.template', output))

    def get_interfaces_only(self):

        """
            Returns List of interfaces that exist on the device (Physical and Virtual)

            Example:
            get_interfaces_only()

            {['GigabitEthernet3/0',
                'GigabitEthernet3/1',
                'GigabitEthernet3/2',
                'GigabitEthernet3/3',
                'Loopback0',
                'Loopback1',
                'Tunnel10',
                'Vlan100',
                'Vlan101']}
        """

        interfaces = {}
        interface_list = []

        output = self.get_interfaces()

        for interface in output:
            interface_list.append(interface['interface'])

        interfaces['interfaces'] = interface_list

        return(interfaces)

    def get_interfaces_status(self):

        """
            Returns JSON type format for interface status

            Example:
            get_interfaces_status()

            {
                 'duplex': 'a-full',
                 'name': '',
                 'port': 'Gi0/0',
                 'speed': 'auto',
                 'status': 'connected',
                 'type': 'RJ45',
                 'vlan': 'routed'
             },
             {
                 'duplex': 'a-full',
                 'name': '',
                 'port': 'Gi0/1',
                 'speed': 'auto',
                 'status': 'connected',
                 'type': 'RJ45',
                 'vlan': '1'
              }
        """

        cmd = 'show interfaces status'

        output = self.iosapi.bcp_send_command(self.iosapi.netmiko_session, cmd)
        self.iosapi.bcp_log("info", "(%s) get_interfaces_status() : Attempting to get interfaces status" %(__name__))
        return(self.iosapi.textfsm_extractor('cisco_ios_show_interfaces_status.template', output))

    def get_interfaces_switchport(self):

        """
            Returns JSON type format for interface switchports

            Example:
            get_interfaces_switchport()

                {
                     'access_vlan': '1',
                     'access_vlan_name': 'default',
                     'administrative_mode': 'dynamic auto',
                     'interface': 'GigabitEthernet1/1',
                     'operational_mode': 'static access',
                     'switchport_status': 'Enabled',
                     'voice_vlan': 'none'
                  },
                 {
                     'access_vlan': '1',
                     'access_vlan_name': 'default',
                     'administrative_mode': 'trunk',
                     'interface': 'GigabitEthernet1/2',
                     'operational_mode': 'trunk',
                     'switchport_status': 'Enabled',
                     'voice_vlan': 'none'
                }
        """

        cmd = 'show interfaces switchport'

        interface_mapper = {
            'Gi' : 'GigabitEthernet',
            'Fa' : 'FastEthernet',
            'TenGi' : 'TenGigabitEthernet'
            }

        output = self.iosapi.bcp_send_command(self.iosapi.netmiko_session, cmd)
        self.iosapi.bcp_log("info", "(%s) get_interfaces_switchport() : Attempting to get interfaces switchport" %(__name__))

        returned_output = self.iosapi.textfsm_extractor('cisco_ios_show_interfaces_switchport.template', output)
        new_output = []

        for interface in returned_output:
            for item, value in interface_mapper.items():
                interface['interface'] = interface['interface'].replace(item, value)
            new_output.append(interface)

        return(new_output)

    def get_ip_int_brief(self):

        """
            Returns JSON type format for show ip int brief

            Example:
            get_ip_int_brief()

            {
                'intf': 'GigabitEthernet0/0',
                'ipaddr': '169.254.10.254',
                'proto': 'up',
                'status': 'up'
            },
            {
                'intf': 'GigabitEthernet0/1',
                'ipaddr': 'unassigned',
                'proto': 'up',
                'status': 'up'
            }

        """

        cmd = 'show ip interface brief'
        output = self.iosapi.bcp_send_command(self.iosapi.netmiko_session, cmd)
        self.iosapi.bcp_log("info", "(%s) get_ip_int_brief() : Attempting to run show ip int brief" %(__name__))

        return(self.iosapi.textfsm_extractor('cisco_ios_show_ip_interface_brief.template', output))