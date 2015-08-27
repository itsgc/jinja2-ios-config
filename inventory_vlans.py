#!/usr/bin/env python
# -*- coding: utf-8 -*-
from vlantools import VlanCensus

hosts = 'config/hosts.yml'
settings = 'config/common_settings.yml'

x = VlanCensus(hosts, settings)
print x.vlan_table()
