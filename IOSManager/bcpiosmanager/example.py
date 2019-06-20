from bcpIOSapi import IOSAPI
from bcpIOSapi import AclAPI
from bcpIOSapi import CdpAPI
from bcpIOSapi import StpAPI
from bcpIOSapi import SystemAPI
from bcpIOSapi import UsersAPI
from bcpIOSapi import VlanAPI

from pprint import pprint

devices = ['10.10.10.10']

for device in devices:
    api = IOSAPI(device, 'cisco', 'cisco', 'cisco', 22)

    if api:
        cdp_api = CdpAPI(api)

        print(cdp_api.set_cdp_neighbors_description())