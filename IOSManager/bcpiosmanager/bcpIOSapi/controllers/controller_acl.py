from bcpIOSapi.iosapi import IOSAPI

class AclAPI(object):
    def __init__(self, iosapi=None):
        if iosapi:
            self.iosapi = iosapi
        else:
            self.iosapi = IOSAPI()

    def get_all_acls(self):
        cmd = 'show ip access-list'
        output = self.iosapi.bcp_send_command(self.iosapi.netmiko_session, cmd)
        self.iosapi.bcp_log("info", "(%s) get_all_acls() : Attempting to retreive all ACLs" %(__name__))
        return(self.iosapi.textfsm_extractor('cisco_ios_show_access_lists.template', output)[0])