from bcpIOSapi import IOSAPI

from bcpIOSapi import AaaAPI
from bcpIOSapi import CdpAPI
from bcpIOSapi import InterfaceAPI
from bcpIOSapi import MacAddressAPI
from bcpIOSapi import StpAPI
from bcpIOSapi import SystemAPI
from bcpIOSapi import VlanAPI

from pprint import pprint

devices = ['10.198.224.110','10.198.224.111','10.198.224.112','10.198.224.113','10.198.224.114','10.198.224.115']

for device in devices:
    api = IOSAPI('cisco_ios', device, 'cisco', 'cisco', 'cisco', 22)

    if api:
        aaa_api = AaaAPI(api)
        cdp_api = CdpAPI(api)
        int_api = InterfaceAPI(api)
        macaddr_api = MacAddressAPI(api)
        stp_api = StpAPI(api)
        system_api = SystemAPI(api)
        vlan_api = VlanAPI(api)

        print(device)
        print(system_api.get_running_config())
        pprint(system_api.get_fqdn_name())
        pprint(int_api.get_interfaces_only())
        print("\n\n")