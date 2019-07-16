from bcpIOSapi import IOSAPI

from bcpIOSapi import AaaAPI
from bcpIOSapi import CdpAPI
from bcpIOSapi import InterfaceAPI
from bcpIOSapi import MacAddressAPI
from bcpIOSapi import StpAPI
from bcpIOSapi import SystemAPI
from bcpIOSapi import VlanAPI

from pprint import pprint

devices = ['10.10.10.10','10.10.10.11','10.10.10.12']

for device in devices:
    api = IOSAPI('cisco_ios', device, 'cisco', 'disco', 'bisco', 22)

    if api:
        aaa_api = AaaAPI(api)
        cdp_api = CdpAPI(api)
        int_api = InterfaceAPI(api)
        macaddr_api = MacAddressAPI(api)
        stp_api = StpAPI(api)
        system_api = SystemAPI(api)
        vlan_api = VlanAPI(api)

        print(device)
        pprint(aaa_api.get_local_users())
        pprint(vlan_api.get_vlans())
        pprint(system_api.get_fqdn_name())
        pprint(int_api.get_interfaces_only())
        pprint(stp_api.set_stp_mode('rapid-pvst'))