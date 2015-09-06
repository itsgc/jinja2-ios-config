## ABOUT
This is a Jinja2 template for classic IOS switches including some common best practices configuration.

It's inspired by [Mierdin/jinja2-nxos-config](https://github.com/Mierdin/jinja2-nxos-config)

Additionally, i added a Vlan "Census" tool. It's meant as a utility to have a quick overview of which vlan is present on which switch. Given a list of hosts and some common settings from YaML files, it will trawl a network and present a table of each vlan and the switches it's configured on.

## HOW
It uses YaML files for device-specific configuration. One file per device, containing details for management and for data plane operation (which vlans, where etc.)

## REQUIREMENTS

It needs Python2 (obviously) with Jinja2 and YAML support.

## TODO

I need to put a TODO list to writing because the task at hand feels a bit overwhelming to me.

* Move everything to ansible
* Automatic configuration push not important right now, having config generated and placed in a local directory fine too. Evaluate [ktbyers/scp_sidecar](https://github.com/ktbyers/scp_sidecar) and [supertylerc/ansible-netmiko-stdlib](https://github.com/supertylerc/ansible-netmiko-stdlib)
* Vanilla template with common settings
* Create configuration snippets for the following components:
    - Authentication (defaults + radius yes/no and ip address + psk in vars file)
    - L2
        - VLAN creation
        - Trunk and access port configuration (define a range of ports with property "access" in inventory file, a range with propery "trunk" and what should go into each, access and voice vlan for access ports and allowed vlans for trunk ports)
        - MSTP yes/no and if yes, make a list of vlans and put first half in instance 1 and second half in instance 2 -- OPTIONAL
    - L3/L4
        - Site to Site IKEv2 VPN (define a bunch of variables such as psk, target host, etc. in inventory file and derive every necessary field from it including interesting traffic acl, nat exempt statement etc.) 
        - Internet Access NAT (with IPSla and Route-Map per-interface natting)
        - Port Forwarding NAT
        - HSRP
        - OSPF Routing -- OPTIONAL
