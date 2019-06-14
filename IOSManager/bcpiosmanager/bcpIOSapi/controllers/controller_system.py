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
        self.iosapi.bcp_log("info", "(IOSAPI_log) SystemAPI.set_hostname() : Attempting to set hostname")
        return(output)

    def set_ip_domain_name(self, domain):
        cmd = 'ip domain-name %s' %(domain)
        output = self.iosapi.bcp_send_config_command(self.iosapi.netmiko_session, cmd)
        self.iosapi.bcp_log("info", "(IOSAPI_log) SystemAPI.set_ip_domain_name() : Attempting to set ip domain name")
        return(output)

    #Get functions
    def get_hostname(self):
        output = self.iosapi.bcp_find_prompt(self.iosapi.netmiko_session)
        self.iosapi.bcp_log("info", "(IOSAPI_log) SystemAPI.get_hostname() : Attempting to retrieve hostname")
        return(output[:-1])

    def get_ip_domain_name(self):
        cmd = 'show host'
        output = self.iosapi.bcp_send_command(self.iosapi.netmiko_session, cmd)
        self.iosapi.bcp_log("info", "(IOSAPI_log) SystemAPI.get_ip_domain_name() : Attempting to retrieve ip domain name")

        if "Invalid input detected" in output:
            cmd = 'show run | include ip domain-name'
            output = self.iosapi.bcp_send_command(self.iosapi.netmiko_session, cmd)
            return(output)
        else:
            return(self.iosapi.textfsm_extractor('cisco_ios_show_hosts.template', output)[0]['default_domain'])

    def get_ios_version(self):
        output = self.template_get_ios_version()[0]
        self.iosapi.bcp_log("info", "(IOSAPI_log) SystemAPI.get_ios_version() : Attempting to retrieve IOS version")
        return(output['version'])

    def get_uptime(self):
        output = self.template_get_ios_version()[0]
        self.iosapi.bcp_log("info", "(IOSAPI_log) SystemAPI.get_uptime() : Attempting to retrieve device uptime")
        return(output['uptime'])

    def get_running_ios_image(self):
        output = self.template_get_ios_version()[0]
        self.iosapi.bcp_log("info", "(IOSAPI_log) SystemAPI.get_running_ios_image() : Attempting to retrieve running IOS image")
        return(output['running_image'])

    def get_hardware_model(self):
        output = self.template_get_ios_version()[0]
        self.iosapi.bcp_log("info", "(IOSAPI_log) SystemAPI.get_hardware_model() : Attempting to retrieve hardware model")

        if not output['hardware']:
            return(output['hardware'])
        else:
            return(output['hardware'][0])

    def get_serial(self):
        output = self.template_get_ios_version()[0]
        self.iosapi.bcp_log("info", "(IOSAPI_log) SystemAPI.get_serial() : Attempting to retrieve device serial number")

        if not output['serial']:
            return(output['serial'])
        else:
            return(output['serial'][0])

    def get_config_register(self):
        output = self.template_get_ios_version()[0]
        self.iosapi.bcp_log("info", "(IOSAPI_log) SystemAPI.get_config_register() : Attempting to retrieve config register")
        return(output['config_register'])
        
    def template_get_ios_version(self):
        cmd = 'show version'
        output = self.iosapi.bcp_send_command(self.iosapi.netmiko_session, cmd)
        return(self.iosapi.textfsm_extractor('cisco_ios_show_version.template', output))