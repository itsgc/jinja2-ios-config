#!/usr/bin/env python
# -*- coding: utf-8 -*-
import yaml
import paramiko
import re
import operator
from netmiko import ConnectHandler

def netmiko_readconfig(ymlfile):
	with open(ymlfile, 'r') as ymlfile:
		network_device = yaml.load(ymlfile)
		return network_device

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
	return active_vlans

def print_vlans(input):
	print 'Active VLANs'
	print '{0:10} {1:20}'.format("VLAN ID", "VLAN NAME")
	for keys, values in sorted(input.iteritems(), key=operator.itemgetter(0)):
		print '{0:10} {1:20}'.format(keys,values)

active_vlans = dict()
network_device = netmiko_readconfig("device_settings.yml")
netmiko_connect = ConnectHandler(**network_device)
netmiko_output = netmiko_connect.send_command('show vlan brief')

extract_vlans(netmiko_output)
print_vlans(active_vlans)
