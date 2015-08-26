#!/usr/bin/env python
# -*- coding: utf-8 -*-
import yaml
import paramiko
import re
import operator
from netmiko import ConnectHandler

with open("device_settings.yml", 'r') as ymlfile:
    network_device = yaml.load(ymlfile)

net_connect = ConnectHandler(**network_device)

output = net_connect.send_command('show vlan brief')
output = output.splitlines()
output = output[3:]
active_vlans = dict()
for line in output:
	if re.match(r'\S', line):
		vlan = line.split()
		vlan_id = int(vlan[0])
		vlan_name = str(vlan[1])
		if vlan_id == 1002 or vlan_id == 1003 \
			or vlan_id == 1004 or vlan_id == 1005:
			pass
		else:
			active_vlans.update({vlan_id:vlan_name})

print 'Active VLANs'
print '{0:10} {1:20}'.format("VLAN ID", "VLAN NAME")
for keys, values in sorted(active_vlans.iteritems(), key=operator.itemgetter(0)):
	print '{0:10} {1:20}'.format(keys,values)
