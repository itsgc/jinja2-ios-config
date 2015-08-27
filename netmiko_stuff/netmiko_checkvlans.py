#!/usr/bin/env python
# -*- coding: utf-8 -*-
import yaml
import paramiko
import re
import operator
from netmiko import ConnectHandler

def netmiko_readconfig(ymlfile):
	with open(ymlfile, 'r') as ymlfile:
		network_settings = yaml.load(ymlfile)
		return network_settings

def extract_vlans(input,exceptions=(1002,1003,1004,1005)):
	input = input.splitlines()
	input = input[3:]
	for line in input:
		if re.match(r'\S', line):
			vlan = line.split()
			vlan_id = int(vlan[0])
			vlan_name = str(vlan[1])
			if vlan_id not in exceptions:
				active_vlans.update({vlan_id:vlan_name})
				if vlan_id not in seen_vlans:
					seen_vlans.update({vlan_id:vlan_name})
					seen_vlans[vlan_id] = []
					seen_vlans[vlan_id] = [vlan_name, ]
					seen_vlans[vlan_id].append(host)
				else:
					seen_vlans[vlan_id].append(host)
	return active_vlans
	return seen_vlans
def print_vlans(input):
	print 'Active VLANs for {0}'.format(host)
	print '{0:10} {1:20}'.format("VLAN ID", "VLAN NAME")
	for keys, values in sorted(input.iteritems(), key=operator.itemgetter(0)):
		print '{0:10} {1:20}'.format(keys,values)
def print_global_vlans(input):
	print 'VLANs seen on the network'
	print '{0:10} {1:20} {2:20}'.format("VLAN ID", "VLAN NAME", "Seen on Switches")
	for keys, values in sorted(input.iteritems(), key=operator.itemgetter(0)):
		print '{0:10} {1:20} {2:30}'.format(keys,values[0],values[1:])
network_settings = netmiko_readconfig("common_settings.yml")
network_hosts = netmiko_readconfig("hosts.yml")
seen_vlans = dict()
for host in network_hosts:
	active_vlans = dict()
	network_settings['ip'] = host
	netmiko_connect = ConnectHandler(**network_settings)
	netmiko_output = netmiko_connect.send_command('show vlan brief')
	extract_vlans(netmiko_output)
	#print_vlans(active_vlans)
print_global_vlans(seen_vlans)
