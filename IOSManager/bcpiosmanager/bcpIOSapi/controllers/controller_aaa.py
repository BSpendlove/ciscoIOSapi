from bcpIOSapi.iosapi import IOSAPI

class AaaAPI(object):
    def __init__(self, iosapi=None):
        if iosapi:
            self.iosapi = iosapi
        else:
            self.iosapi = IOSAPI()

    #Add Functions
    #add_aaa_group is best used with with add_radius_server or add_tacacs_server
    #like:  myRadiusServer = add_radius_server('10.10.10.10','mykey','1812','1813')
    #       add_aaa_group('MyRadiusGroup', myRadiusServer)
    def add_aaa_group(self, name='', type='radius', ip=''):
        cmds = []

        if not name:
            return("AAA Group needs name to be configured...")

        if type == 'radius':
            cmds.append('aaa group server radius %s' %(name))
        else:
            cmds.append('aaa group server tacacs+ %s' %(name))

        cmds.append('server %s' %(ip))

        output = self.iosapi.bcp_send_config_command(self.iosapi.netmiko_session, cmds)
        self.iosapi.bcp_log("info", "(%s) add_aaa_group() : Attempting to add aaa group %s (%s)" %(__name__, name, type))

        return(output)

    def add_radius_server(self, server, key, auth_port, acct_port):
        cmd = 'radius-server host %s auth-port %s acct-port %s key %s' %(server, auth_port, acct_port, key)
        output = self.iosapi.bcp_send_config_command(self.iosapi.netmiko_session, cmd)
        self.iosapi.bcp_log("info", "(%s) add_radius_server() : Attempting to add radius server %s" %(__name__, server))
        return(server)

    def add_tacacs_server(self, server, key, port=''):
        if port:
            cmd = 'tacacs-server host %s port %s key %s' %(server, port, key)
        else:
            cmd = 'tacacs-server host %s key %s' %(server, key)

        output = self.iosapi.bcp_send_config_command(self.iosapi.netmiko_session, cmd)
        self.iosapi.bcp_log("info", "(%s) add_tacacs_server() : Attempting to add tacacs server %s" %(__name__, server))
        return(server)

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
    def set_aaa_new_model(self):
        cmd = 'aaa new-model'
        output = self.iosapi.bcp_send_config_command(self.iosapi.netmiko_session, cmd)
        self.iosapi.bcp_log("info", "(%s) set_aaa_new_model : Attempting to send command aaa new-model" %(__name__))
        return(output)

    def set_aaa_authentication_login(self, auth_list='', local=True, group=False, group_name='', local_fallback=False):
        if auth_list:
            if local:
                cmd = 'aaa authentication login %s local' %(auth_list)
            else:
                if group:
                    if not group_name:
                        return("Group name needs to be configured...")
                    else:
                        cmd = 'aaa authentication login %s group %s' %(auth_list, group_name)
                    if local_fallback:
                        cmd = 'aaa authentication login %s group %s local' %(auth_list, group_name)
        else:
            if local:
                cmd = 'aaa authentication login %s local' %(auth_list)
            else:
                if group:
                    if not group_name:
                        return("Group name needs to be configured...")
                    else:
                        cmd = 'aaa authentication login default group %s' %(group_name)
                    if local_fallback:
                        cmd = 'aaa authentication login default group %s local' %(group_name)

        output = self.iosapi.bcp_send_command(self.iosapi.netmiko_session, cmd)
        self.iosapi.bcp_log("info", "(%s) set_aaa_authentication_login : Attempting to send command %s" %(__name__, command))
        return(output)


    def set_enable(self, pwd, type='secret'):
        if type == 'secret':
            cmd = 'enable secret %s' %(pwd)
        else:
            cmd = 'enable password %s' %(pwd)

        output = self.iosapi.bcp_send_config_command(self.iosapi.netmiko_session, cmd)
        self.iosapi.bcp_log("info", "(%s) set_enable : Attempting to set enable" %(__name__))
        return(output)

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