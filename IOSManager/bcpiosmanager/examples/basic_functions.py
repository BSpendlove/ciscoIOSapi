from bcpIOSapi import IOSAPI

from bcpIOSapi import AaaAPI
from bcpIOSapi import CdpAPI
from bcpIOSapi import InterfaceAPI
from bcpIOSapi import MacAddressAPI
from bcpIOSapi import StpAPI
from bcpIOSapi import SystemAPI
from bcpIOSapi import VlanAPI

from pprint import pprint

#Credentials and IP addresses used in this example script are purely for showcases examples with GNS3 IOSv and IOSvL2 images

devices = ['192.168.110.80']

for device in devices:
    api = IOSAPI('cisco_ios', device, 'cisco', 'cisco', 'cisco', 22, debug_mode=True)

    if api:
        int_api = InterfaceAPI(api)
        vlan_api = VlanAPI(api)

        pprint(int_api.replace_interfaces_access_vlan(100,110))
        pprint(int_api.replace_interfaces_voice_vlan(50,120))