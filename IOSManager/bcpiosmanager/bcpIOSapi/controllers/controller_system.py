from bcpIOSapi.iosapi import IOSAPI

class SystemAPI(object):
    def __init__(self, iosapi=None):
        if iosapi:
            self.iosapi = iosapi
        else:
            self.iosapi = IOSAPI()

    #Set functions
    def set_hostname(self, hostname):
        cmd = 'hostname %s' %(hostname)
        output = self.iosapi.bcp_send_config_command(self.iosapi.netmiko_session, cmd)
        self.iosapi.bcp_log("info", "(%s) set_hostname() : Attempting to set hostname" %(__name__))
        return(output)

    def set_ip_domain_name(self, domain):
        cmd = 'ip domain-name %s' %(domain)
        output = self.iosapi.bcp_send_config_command(self.iosapi.netmiko_session, cmd)
        self.iosapi.bcp_log("info", "(%s) set_ip_domain_name() : Attempting to set IP domain name" %(__name__))
        return(output)

    #Banner function needs to be revised - Plan is to provide a range of templates instead of just pasting a template
    def set_banner_motd(self, message):
        if not message:
            message = '''
    UNAUTHORIZED ACCESS TO THIS DEVICE IS PROHIBITED

    You must have explicit, authorized permission to access or configure this device.
    Unauthorized attempts and actions to access or use this system may result in civil and/or criminal penalties.

    All activities performed on this device are logged and monitored.
    '''

    #Get functions
    def get_hostname(self):
        output = self.iosapi.bcp_find_prompt(self.iosapi.netmiko_session)
        self.iosapi.bcp_log("info", "(%s) get_hostname() : Attempting to get hostname" %(__name__))
        return(output[:-1])

    def get_ip_domain_name(self):
        cmd = 'show host'
        output = self.iosapi.bcp_send_command(self.iosapi.netmiko_session, cmd)
        self.iosapi.bcp_log("info", "(%s) get_ip_domain_name() : Attempting to get IP domain name" %(__name__))

        if "Invalid input detected" in output:
            cmd = 'show run | include ip domain-name'
            output = self.iosapi.bcp_send_command(self.iosapi.netmiko_session, cmd)
            return(output)
        else:
            return(self.iosapi.textfsm_extractor('cisco_ios_show_hosts.template', output)[0]['default_domain'])

    def get_running_config(self, backup=False, path=''):
        cmd = 'show running-config'
        output = self.iosapi.bcp_send_command(self.iosapi.netmiko_session, cmd)

        self.iosapi.bcp_log("info", "(%s) get_running_config() : Attempting to get running-config" %(__name__))

        if backup:
            try:
                backup_file = open(path, 'w')
                backup_file.write(output)
                backup_file.close()
                self.iosapi.bcp_log("info", "(%s) get_running_config() : Attempting to save backup in location: %s" %(__name__, path))
            except:
                self.iosapi.bcp_log("info", "(%s) get_running_config() : Unable to save backup in location: %s" %(__name__, path))

        return(output)

    def get_ios_version(self):
        output = self.template_get_ios_version()[0]
        self.iosapi.bcp_log("info", "(%s) get_ios_version() : Attempting to get IOS Version" %(__name__))
        return(output['version'])

    def get_uptime(self):
        output = self.template_get_ios_version()[0]
        self.iosapi.bcp_log("info", "(%s) get_uptime() : Attempting to get uptime" %(__name__))
        return(output['uptime'])

    def get_running_ios_image(self):
        output = self.template_get_ios_version()[0]
        self.iosapi.bcp_log("info", "(%s) get_running_ios_image() : Attempting to get running IOS image" %(__name__))
        return(output['running_image'])

    def get_hardware_model(self):
        output = self.template_get_ios_version()[0]
        self.iosapi.bcp_log("info", "(%s) get_hardware_model() : Attempting to get hardware model" %(__name__))

        if not output['hardware']:
            return(output['hardware'])
        else:
            return(output['hardware'][0])

    def get_serial(self):
        output = self.template_get_ios_version()[0]
        self.iosapi.bcp_log("info", "(%s) get_serial() : Attempting to get serial number" %(__name__))

        if not output['serial']:
            return(output['serial'])
        else:
            return(output['serial'][0])

    def get_config_register(self):
        output = self.template_get_ios_version()[0]
        self.iosapi.bcp_log("info", "(%s) get_config_register() : Attempting to get config register" %(__name__))
        return(output['config_register'])
        
    def template_get_ios_version(self):
        cmd = 'show version'
        output = self.iosapi.bcp_send_command(self.iosapi.netmiko_session, cmd)
        return(self.iosapi.textfsm_extractor('cisco_ios_show_version.template', output))