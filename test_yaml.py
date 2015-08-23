#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml

with open("switch.yml", 'r') as ymlfile:
    switch = yaml.load(ymlfile)
    for key, value in switch['vlans'].iteritems():
            print key
