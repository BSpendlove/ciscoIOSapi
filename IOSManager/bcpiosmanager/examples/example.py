from bcpIOSapi import IOSAPI
from bcpIOSapi import InterfaceAPI

from pprint import pprint

devices = ['192.168.64.141', '192.168.64.142']

for device in devices:
    api = IOSAPI('cisco_ios', device, 'cisco', 'cisco', 'cisco', 22)

    if api:
        int_api = InterfaceAPI(api)

        pprint(int_api.get_interfaces_only(), indent=4)