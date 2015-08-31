#!/usr/bin/env python
# -*- coding: utf-8 -*-
import yaml
import re
import operator
import socket
from netmiko import ConnectHandler


class VlanCensus(object):

    def __init__(self, hosts='', settings=''):
        if hosts and settings:
            self.hosts = self.read_config(hosts)
            self.settings = self.read_config(settings)
        self.seenVlans = dict()
        self.errors = []
        self.vlanDict = self.gather_vlans()

    def show_errors(self):
        if len(self.errors) > 0:
            output = "I encountered these errors while processing:\n"
            for error in self.errors:
                output += "{}\n".format(error)
            return output
        else:
            output = "There were no errors during processing"
            return output

    def read_config(self, input):
        with open(input, 'r') as ymlfile:
            output = yaml.load(ymlfile)
        return output

    def is_valid_ipv4_address(self, address):
        try:
            socket.inet_pton(socket.AF_INET, address)
        except AttributeError:  # no inet_pton here, sorry
            try:
                socket.inet_aton(address)
            except socket.error:
                return False
            return address.count('.') == 3
        except socket.error:  # not a valid address
            return False
        return True

    def is_valid_ipv6_address(self, address):
        try:
            socket.inet_pton(socket.AF_INET6, address)
        except socket.error:  # not a valid address
            return False
        return True

    def gather_vlans(self):
        for host in self.hosts:
            if self.is_valid_ipv4_address(host):
                try:
                    self.settings['ip'] = host
                    netmiko_connect = ConnectHandler(**self.settings)
                    netmiko_output = netmiko_connect.\
                        send_command('show vlan brief')
                    output = self.parse_vlans(netmiko_output,
                                              self.seenVlans, host)
                except:
                    self.errors.append("Connection to {0} didn't go so well".format(host))
            else:
                self.errors.append("{0} is not a valid IPv4 address.".format(host))
        return output

    def parse_vlans(self, raw_data, dictionary, host):
        # We dont need headings so we will only iterate over meaningful lines.
        # This could be read as Code Golf but i like it better than nesting
        # regexps inside a for loop.
        important_lines = (line for line in raw_data.splitlines()[3:]
                           if re.match(r'\S', line))
        for line in important_lines:
            vlan = line.split()
            vlan_id, vlan_name = vlan[:2]
            vlan_id = int(vlan_id)
            if vlan_id not in self.seenVlans:
                dictionary.update({vlan_id: [vlan_name, host]})
            else:
                dictionary[vlan_id].append(host)
        return dictionary

    def vlan_table(self):
        output = 'VLANs seen on the network\n'
        output += '{0:10} {1:20} {2:20}\n'.format("VLAN ID",
                                                  "VLAN NAME",
                                                  "Seen on Switches")
        for keys, values in sorted(self.vlanDict.iteritems(),
                                   key=operator.itemgetter(0)):
            output += '{0:10} {1:20} {2:30}\n'.format(keys,
                                                      values[0],
                                                      ', '.join(str(switch)
                                                                for switch
                                                                in values[1:]))
        return output
