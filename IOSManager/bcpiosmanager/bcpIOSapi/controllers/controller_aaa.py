from bcpIOSapi.iosapi import IOSAPI

class AaaAPI(object):
    def __init__(self, iosapi=None):
        if iosapi:
            self.iosapi = iosapi
        else:
            self.iosapi = IOSAPI()

    #Add Functions
    def add_aaa_group(self, name='', type='radius', ip='', auth_port='1812', acct_port='1813'):

        """
            Creates AAA Group if the RADIUS/TACACS Server exists in the current configuration
            > name      -   Name of AAA Group
            > type      -   radius or tacacs+
            > ip        -   Old IOS Syntax - IP of current RADIUS or TACACS+ server configured
            > auth_port -   Authentication Port
            > acct_port -   Accounting Port (if RADIUS is used)
        """
        cmds = []

        if not name:
            return("AAA Group needs name to be configured...")

        if type == 'radius':
            cmds.append('aaa group server radius %s' %(name))
            cmds.append('server %s auth-port %s acct-port %s' %(ip, auth_port, acct_port))
        if type == 'tacacs+':
            cmds.append('aaa group server tacacs+ %s' %(name))
            cmds.append('server %s' %(ip))

        output = self.iosapi.bcp_send_config_command(self.iosapi.netmiko_session, cmds)
        self.iosapi.bcp_log("info", "(%s) add_aaa_group() : Attempting to add aaa group %s (%s)" %(__name__, name, type))

        return(output)

    def add_radius_server(self, server, key, auth_port='1812', acct_port='1813'):

        """
            Add RADIUS Server if it doesn't exist (If you would like to update an existing server, use update_radius_server()
            > server    -   Server DNS/IP
            > key       -   RADIUS Secret
            > auth_port -   Authentication Port (Default: UDP 1812)
            > acct_port -   Accounting Port (Default: UDP 1813)

            Example:
            add_radius_server('169.254.1.1', 'myradiussecret')
        """

        radius_servers = self.get_radius_servers()

        for radius_server in radius_servers:
            if radius_server['ip'] == server:
                self.iosapi.bcp_log("info", "(%s) add_radius_server() : RADIUS Server %s already exist" %(__name__, server))
            else:

                cmd = 'radius-server host %s auth-port %s acct-port %s key %s' %(server, auth_port, acct_port, key)
                output = self.iosapi.bcp_send_config_command(self.iosapi.netmiko_session, cmd)

                self.iosapi.bcp_log("info", "(%s) add_radius_server() : Attempting to add radius server %s" %(__name__, server))
                return(server)

    def add_tacacs_server(self, server, key, port='49'):

        """
            Add TACACS+ Server if it doesn't exist (If you would like to update an existing server, use update_tacacs_server()
            > server    -   Server DNS/IP
            > key       -   TACACS+ Secret
            > port      -   TACACS+ port (Default: TCP 49)

            Example:
            add_tacacs_server('169.254.1.1', 'mytacacskey')
        """

        tacacs_servers = self.get_tacacs_servers()

        for tacacs_server in tacacs_servers:
            if tacacs_server['ip'] == server:
                self.iosapi.bcp_log("info", "(%s) add_tacacs_server() : TACACS+ server %s already exist" %(__name__, server))
            else:
                if port:
                    cmd = 'tacacs-server host %s port %s key %s' %(server, port, key)
                else:
                    cmd = 'tacacs-server host %s key %s' %(server, key)

                output = self.iosapi.bcp_send_config_command(self.iosapi.netmiko_session, cmd)
                self.iosapi.bcp_log("info", "(%s) add_tacacs_server() : Attempting to add tacacs server %s" %(__name__, server))
                return(server)

    def add_local_user(self, username, password='', secret='', priv_level=15):

        """
            Adds a new local user. You can define the priv level if need be

            Example:
            add_local_user('cisco', 'disco', 'mySecret')
        """

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

        """
            Enables AAA new-model if not configured

            Example:
            set_aaa_new_model()
        """

        cmd = 'aaa new-model'
        output = self.iosapi.bcp_send_config_command(self.iosapi.netmiko_session, cmd)
        self.iosapi.bcp_log("info", "(%s) set_aaa_new_model : Attempting to send command aaa new-model" %(__name__))
        return(output)

    def set_aaa_authentication_login(self, auth_list='', local=True, group=False, group_name='', local_fallback=False):

        """
            Set AAA Method for either default or specified Group
            > auth_list         -   Authentication List (NOT USED CURRENTLY)
            > local             -   Local authentication only
            > group             -   Set to TRUE if you will be using RADIUS/TACACS+
            > group_name        -   If a group will be used, define the group name (or names eg MYRADIUS MYTACACS)
            > local_fallback    -   Local database authentication fallback if TACACS/RADIUS is unreachable

            Example:
            set_aaa_authentication_login('',False,True,'ISE_GROUP',True)
        """

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

        """
            Create enable password
            > pwd   -   Enable Secret/Password
            > type  -   Can be either secret or password

            Example:
            set_enable('dingdong')
        """

        if type == 'secret':
            cmd = 'enable secret %s' %(pwd)
        else:
            cmd = 'enable password %s' %(pwd)

        output = self.iosapi.bcp_send_config_command(self.iosapi.netmiko_session, cmd)
        self.iosapi.bcp_log("info", "(%s) set_enable : Attempting to set enable" %(__name__))
        return(output)

    #Get Functions
    def get_local_users(self):

        """
            Returns all configured local users in JSON Style Format:

            Example:
            get_local_users()

            {'password': '$1$4Zuj$2E73E0iiL2LQ/bp82Dn2g/',
              'password_level': '5',
              'password_type': 'secret',
              'priv_level': '',
              'username': 'cisco'}
        """

        cmd = 'show run'
        output = self.iosapi.bcp_send_command(self.iosapi.netmiko_session, cmd)
        self.iosapi.bcp_log("info", "(%s) get_local_users() : Attempting to retrieve local users" %(__name__))
        
        local_users = self.iosapi.textfsm_extractor('cisco_ios_local_users.template', output)

        if not local_users:
            return
        else:
            return(local_users)

    def get_radius_servers(self):

        """
            Returns RADIUS Servers in JSON Style Format

            Example:
            get_radius_servers()

            {'acct_port': '1813',
              'auth_port': '1812',
              'id': '2',
              'ip': '192.168.110.226',
              'priority': '1'},
             {'acct_port': '1813',
              'auth_port': '1812',
              'id': '3',
              'ip': '192.168.110.222',
              'priority': '2'}
        """

        cmd = 'show aaa servers'
        output = self.iosapi.bcp_send_command(self.iosapi.netmiko_session, cmd)
        self.iosapi.bcp_log("info", "(%s) get_radius_servers() : Attempting to retrieve RADIUS servers" %(__name__))

        return(self.iosapi.textfsm_extractor('cisco_ios_show_aaa_servers.template', output))

    def get_tacacs_servers(self):

        """
            Returns TACACS Servers in JSON Style Format

            Example:
            get_tacacs_servers()

            {'failed_connections': '0',
             'ip': '192.168.110.241',
             'packet_received': '0',
             'packets_sent': '0',
             'server_port': '49',
             'socket_aborts': '0',
             'socket_closes': '0',
             'socket_errors': '0',
             'socket_opens': '0',
             'socket_timeouts': '0',
             'tacacs_name': 'ISE01'}
        """

        cmd = 'show tacacs'
        output = self.iosapi.bcp_send_command(self.iosapi.netmiko_session, cmd)
        self.iosapi.bcp_log("info", "(%s) get_tacacs_servers() : Attempting to retrieve TACACS+ servers" %(__name__))

        return(self.iosapi.textfsm_extractor('cisco_ios_show_tacacs.template', output))

    # Radius and Tacacs+ Commands
    # radius-server host {hostname | ip-address} [auth-port port-number] [acct-port port-number] [timeout seconds] [retransmit retries] [key string] [alias{hostname | ip-address}]
    # Above command is deprecated in IOS 15.2, use:
    # radius-server {name}
    # 
    # Tacacs Config
    # tacacs-server host host-name [port integer] [timeout integer] [key string] [single-connection] [nat]