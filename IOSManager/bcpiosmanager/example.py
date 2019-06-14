from bcpIOSapi import IOSAPI
from bcpIOSapi import AclAPI
from bcpIOSapi import CdpAPI
from bcpIOSapi import StpAPI
from bcpIOSapi import SystemAPI
from bcpIOSapi import UsersAPI
from bcpIOSapi import VlanAPI

from pprint import pprint


api = IOSAPI('192.168.64.130', 'cisco', 'cisco', 22, 'cisco', 1)

'''
system_api = SystemAPI(api)
users_api = UsersAPI(api)
stp_api = StpAPI(api)
acl_api = AclAPI(api)
'''
cdp_api = CdpAPI(api)
#vlan_api = VlanAPI(api)

'''
print(system_api.get_hostname())
print(system_api.get_ios_version())
print(system_api.get_uptime())
print(system_api.get_running_ios_image())
print(system_api.get_hardware_model())
print(system_api.get_serial())
print(system_api.get_config_register())
print(system_api.get_ip_domain_name())
print(users_api.get_local_users())
print(users_api.add_local_user(username='MyUsername',secret='MySecret'))
print(stp_api.set_stp_mode('rapid-pvst'))
print(stp_api.get_stp_mode())
pprint(stp_api.get_stp_bridge())
pprint(acl_api.get_all_acls())
pprint(cdp_api.get_cdp_neighbors_detail())
'''
pprint(cdp_api.set_cdp(enabled=False, version=2))
#pprint(vlan_api.get_vlans())
#pprint(vlan_api.get_vlan_id('10d'))