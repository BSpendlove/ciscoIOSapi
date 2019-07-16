# ciscoIOSapi
### ps. It's not really an API... Just a project for fun to see how much/what I can do with pure interaction between Python and Cisco IOS (not developed for ASA/IOS-XE/XR/NXOS etc..)

## Examples what can be achieved:

Show all local users configured on IOS device:
```
api = IOSAPI('cisco_ios', device, 'cisco', 'disco', 'bisco', 22)
aaa_api = AaaAPI(api)
pprint(aaa_api.get_local_users())

[{'password': '$1$p.QC$1VpdpBufSwjA3F.CzaQws/',
  'password_level': '5',
  'password_type': 'secret',
  'priv_level': '',
  'username': 'cisco'},
 {'password': '$1$o2iI$chX6MLmL0gzd2uZEhnyNT0',
  'password_level': '5',
  'password_type': 'secret',
  'priv_level': '',
  'username': 'pythonuser'}]
```

Find FQDN Name:
```
system_api = SystemAPI(api)

pprint(system_api.get_fqdn_name())

'rtr01.ldn.mydomain.com'
```

Configure STP Mode:
```
stp_api = StpAPI(api)
  
print(stp_api.set_stp_mode('nonstpmode'))
"Mode nonstpmode is not valid, valid modes are: pvst, mst or rapid-pvst"
```

Other examples:
- Many output commands returned in JSON type format via TextFSM such as:
--Interface Status
-- Show IP interface brief
-- Show spanning-tree bridge
-- Returning MAC address table
-- Show VLAN database and interface VLAN membership 'show vlan brief'
-- Display ACLs
- Configure range of settings via Python like hostname, ip domain-name, interfaces, STP mode, VLANs, AAA Groups
- Set Interface description for CDP neighbors

## Concepts

If I work on this more in the future, I wanted to separate the specific functions according to controllers.

Eg. controller_stp has all the functions related to STP. Retrieving and configuring.
You will need to pass in the base class (ciscoIOSapi) into the relevant controller class and go from there...

```
from bcpIOSapi import IOSAPI

from bcpIOSapi import SystemAPI
from bcpIOSapi import VlanAPI

devices = ['10.198.208.254']

for device in devices:
    api = IOSAPI('cisco_ios', device, 'cisco', 'disco', 'bisco', 22)

    if api:
        system_api = SystemAPI(api)
        vlan_api = VlanAPI(api)

        print(vlan_api.get_vlans())
        print(system_api.get_fqdn_name())
```

### Current Controllers

- AaaAPI
- AclAPI
- CdpAPI
- InterfaceAPI
- MacAddressAPI
- StpAPI
- SystemAPI
- VlanAPI

Obviously, not all are complete and fully functional but I'm slowly creating functions to be used in this python tool. My goal is to actually create more useful functions such as the CDP function to set interface descriptions instead of just using TextFSM to return data...

Not sure if I should update the readme with the actual functions for each class, or just comment more on the relevant controller files...
I currently test this in a python virtual enviornment, just simply go to the root and run `pip -install -e ./` for testing...

I'm always open for suggestions and always willing to improve my code. 

A few of the TextFSM templates I wrote myself, but the majority of them are via networktocode. I've included the license file, I don't think it's bad to include some of the templates that I'm using because I just wrote my own TextFSM function instead of using Netmiko's use_textfsm=True when sending commands...