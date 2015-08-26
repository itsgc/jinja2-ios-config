#!/usr/bin/env python
# -*- coding: utf-8 -*-
import yaml
#import paramiko
#import netmiko

with open("device_settings.yml", 'r') as ymlfile:
    network_device = yaml.load(ymlfile)

print network_device
