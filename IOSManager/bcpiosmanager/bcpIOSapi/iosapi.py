import os
import re
import logging
import time
import textfsm
from datetime import datetime
from netmiko import ConnectHandler
from netmiko import NetMikoAuthenticationException, NetMikoTimeoutException

class IOSAPI(object):
    def __init__(self, device_driver='cisco_ios', ip='', username='', password='', secret='',port=22, debug_mode=False):
        self.device_driver = device_driver
        self.ip = ip
        self.username = username
        self.password = password
        self.port = port
        self.debug_mode = debug_mode

        details = {
            'device_type' : device_driver,
            'ip' : ip,
            'username' : username,
            'password' : password,
            'port' : port
            }

        if port == 23:
            details.update({'device_type' : 'cisco_ios_telnet'})

        if not secret:
            print("Secret has not been configured for the specified device, some commands may not work...")
        else:
            details['secret'] = secret

        try:
            self.netmiko_session = self.create_session(details)

            if self.netmiko_session:
                self.bcp_enable(self.netmiko_session)
        except:

            return

    def bcp_log(self, type='warning', Logmessage=''):
        with open('bcp.log','a') as file:
            now = datetime.now()
            file.write("{0} : {1: <8} --- {2: <10}\n".format(now.strftime('%m-%d-%Y %H:%M:%S'), type, Logmessage))

    def create_session(self, netmiko_dict):
        try:
            session = ConnectHandler(**netmiko_dict)
            self.bcp_log("info", "(%s) create_session() : Successful connection to device %s on port: %s" %(__name__, netmiko_dict['ip'], netmiko_dict['port']))
            return(session)

        except (NetMikoAuthenticationException, NetMikoTimeoutException) as error:
            self.bcp_log("info", "(%s) create_session() : Failed connection to device %s on port: %s - Reason: %s" %(__name__, netmiko_dict['ip'], netmiko_dict['port'], error))
            print("Netmiko Error: %s" %(error))
            return

    def bcp_enable(self, session):
        try:
            output = session.enable()
            self.bcp_log("info", "(%s) bcp_enable() : Successfully entered enable mode" %(__name__))
        except:
            self.bcp_log("info", "(%s) bcp_enable() : Error entering enable mode" %(__name__))
            return

    def bcp_find_prompt(self, session):
        return(session.find_prompt())

    def bcp_send_command(self, session, command):
        if session:
            output = session.send_command(command)

            if self.debug_mode:
                self.bcp_log("debug", "(%s) bcp_send_command() : Command sent - %s" %(__name__, command))

            if "Invalid input detected" in output:
                self.bcp_log("info", "(%s) bcp_send_command() : Invalid input detected" %(__name__))
                return("Invalid input detected...")

            if "Command rejected:" in output:
                self.bcp_log("info", "(%s) bcp_send_command() : Command rejected" %(__name__))
                return("Invalid input detected...")

            return(output)
        else:
            self.bcp_log("info", "(%s) bcp_send_command() : Unable to send command" %(__name__))

    def bcp_send_config_command(self, session, command):
        output = session.send_config_set(command)

        if self.debug_mode:
            self.bcp_log("debug", "(%s) .bcp_send_config_command() : Command sent - %s" %(__name__, command))

        if "Invalid input detected" in output:
            self.bcp_log("info", "(%s) bcp_config_command() : Invalid input detected" %(__name__))
            return
        else:
            return(output)

    def textfsm_extractor(self, template_name, raw_text):
        textfsm_data = list()
        fsm_handler = None

        template_directory = os.path.abspath(os.path.join(os.path.dirname(__file__),'templates'))
        template_path = '{0}/{1}'.format(template_directory, template_name)

        with open(template_path) as f:
            fsm_handler = textfsm.TextFSM(f)

            for obj in fsm_handler.ParseText(raw_text):
                entry = {}

                for index, entry_value in enumerate(obj):
                    entry[fsm_handler.header[index].lower()] = entry_value

                textfsm_data.append(entry)

            return(textfsm_data)