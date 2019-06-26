from bcpIOSapi import IOSAPI
from bcpIOSapi import InterfaceAPI

from pprint import pprint

devices = ['bspendlove.ddns.net']

for device in devices:
    api = IOSAPI('cisco_ios', device, 'cisco', '5B7sr00iqH', '5B7sr00iqH', 22)

    if api:
        int_api = InterfaceAPI(api)

        pprint(int_api.get_interfaces_only(), indent=4)