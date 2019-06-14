from bcpIOSapi.iosapi import IOSAPI

class UsersAPI(object):
    def __init__(self, iosapi=None):
        if iosapi:
            self.iosapi = iosapi
        else:
            self.iosapi = IOSAPI()

    #Add Functions
    def add_local_user(self, username, password='', secret='', priv_level=15):
        priv_valid_range = '<0-15>'
        if priv_level not in range (0, 16):
            print("Invalid priv-level, valid range is %s" %(priv_valid_range))
            return
        if password and secret:
            print("Password and Secret can not be both configured")
            return
        if password and not secret:
            cmd = "username %s priv %s password %s" %(username, priv_level, password)
        if secret and not password:
            cmd = "username %s priv %s secret %s" %(username, priv_level, secret)

        output = self.iosapi.bcp_send_config_command(self.iosapi.netmiko_session, cmd)
        self.iosapi.bcp_log("info", "(%s) add_local_user() : Attempting to add local user %s" %(__name__, username))
        
        return(output)

    #Set Functions

    #Get Functions
    def get_local_users(self):
        cmd = 'show run'
        output = self.iosapi.bcp_send_command(self.iosapi.netmiko_session, cmd)
        self.iosapi.bcp_log("info", "(%s) get_local_users() : Attempting to retrieve local users" %(__name__))
        
        local_users = self.iosapi.textfsm_extractor('cisco_ios_local_users.template', output)

        if not local_users:
            return
        else:
            return(local_users)