from bcpIOSapi.iosapi import IOSAPI

class VlanAPI(object):
    def __init__(self, iosapi=None):
        if iosapi:
            self.iosapi = iosapi
        else:
            self.iosapi = IOSAPI()

    #Add Functions
    def add_vlan(self, vlanid, name=''):

        """
            Creates VLAN and returns the SSH output of the results
            > vlanid    -   VLAN number to add
            > name      -   VLAN name to assign the VLAN ID

            Example:
            add_vlan(10, 'CORP_USERS')
        """

        cmds = []

        if vlanid:
            if isinstance(vlanid, int):
                cmds.append('vlan %s' % vlanid)
            if name:
                cmds.append('name %s' %name)

        if self.check_vlan_exist(vlanid):
            self.iosapi.bcp_log("info", "(%s) add_vlan() : VLAN already exist - Renaming VLAN %s to %s" %(__name__, vlanid, name))
        else:
            self.iosapi.bcp_log("info", "(%s) add_vlans() : Attempting to create VLAN %s" %(__name__, vlanid))

        return(self.iosapi.bcp_send_config_command(self.iosapi.netmiko_session, cmds))

    #Check Functions

    def check_vlan_exist(self, vlanid):

        """
            Returns Boolean
            IOS typically returns something like: 'VLAN id 23 not found in current VLAN database'
            > vlanid    -   VLAN number to check

            Example:
            check_vlan_exist(10)

            True
        """

        cmd = 'show vlan id %s' %(vlanid)

        output = self.iosapi.bcp_send_command(self.iosapi.netmiko_session, cmd)
        self.iosapi.bcp_log("info", "(%s) get_vlans() : Attempting to retreive all VLANs" %(__name__))

        if 'VLAN id {} not found'.format(vlanid) in output:
            return(False)
        else:
            return(True)

    #Get Functions
    def get_vlans(self):

        """
            Returns all VLANs in the database in JSON type format

            Example:
            get_vlans()

            {
                'interfaces': ['Gi0/1',
                               'Gi0/2',
                               'Gi0/3'],
                'name': 'default',
                'status': 'active',
                'vlan_id': '1'
            },
            {
                'interfaces': ['Gi1/0'],
                'name': 'CORP_USERS',
                'status': 'active',
                'vlan_id' : '10'
            }
        """

        cmd = 'show vlan brief'
        output = self.iosapi.bcp_send_command(self.iosapi.netmiko_session, cmd)
        self.iosapi.bcp_log("info", "(%s) get_vlans() : Attempting to retreive all VLANs" %(__name__))
        return(self.iosapi.textfsm_extractor('cisco_ios_show_vlan.template', output))

    def get_vlan_id(self, vlanid):

        """
            Returns JSON type format for specific VLAN
            > vlanid    -   VLAN ID to check

            Example:
            get_vlan_id(10)

            {
                'interfaces': ['Gi1/0'],
                'name': 'CORP_USERS',
                'status': 'active',
                'vlan_id' : '10'
            }
        """

        cmd = 'show vlan id %s' %(vlanid)
        output = self.iosapi.bcp_send_command(self.iosapi.netmiko_session, cmd)
        self.iosapi.bcp_log("info", "(%s) get_vlan_id() : Attempting to retreive VLAN ID %s" %(__name__, vlanid))
        return(self.iosapi.textfsm_extractor('cisco_ios_show_vlan.template', output))