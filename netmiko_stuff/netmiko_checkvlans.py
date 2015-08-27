#!/usr/bin/env python
# -*- coding: utf-8 -*-
import yaml
import re
import operator
from netmiko import ConnectHandler


def netmiko_readconfig(ymlfile):
    with open(ymlfile, 'r') as ymlfile:
        network_settings = yaml.load(ymlfile)
    return network_settings


def extract_vlans(input):
    # We dont need headings so we will only iterate over meaningful lines.
    # This could be read as Code Golf but i like it better than nesting
    # regexps inside a for loop.
    important_lines = (line for line in input.splitlines()[3:]
                       if re.match(r'\S', line))
    for line in important_lines:
        vlan = line.split()
        vlan_id, vlan_name = vlan[:2]
        vlan_id = int(vlan_id)
        if vlan_id not in seen_vlans:
            seen_vlans.update({vlan_id: [vlan_name, host]})
        else:
            seen_vlans[vlan_id].append(host)
    return seen_vlans


def print_global_vlans(input):
    print 'VLANs seen on the network'
    print '{0:10} {1:20} {2:20}'.format("VLAN ID",
                                        "VLAN NAME", "Seen on Switches")
    for keys, values in sorted(input.iteritems(), key=operator.itemgetter(0)):
        print '{0:10} {1:20} {2:30}'.format(keys, values[0],
                                            ', '.join(str(switch) for switch
                                                      in values[1:]))


network_settings = netmiko_readconfig("common_settings.yml")
network_hosts = netmiko_readconfig("hosts.yml")
seen_vlans = dict()

for host in network_hosts:
    network_settings['ip'] = host
    netmiko_connect = ConnectHandler(**network_settings)
    netmiko_output = netmiko_connect.send_command('show vlan brief')
    extract_vlans(netmiko_output)

print_global_vlans(seen_vlans)
