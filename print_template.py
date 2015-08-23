#!/usr/bin/env python
# -*- coding: utf-8 -*-
import yaml
from jinja2 import Environment, FileSystemLoader
with open("switch.yml", 'r') as ymlfile:
    switch = yaml.load(ymlfile)
env = Environment(loader=FileSystemLoader('.'), trim_blocks=True,
                  lstrip_blocks=True)
template = env.get_template('ios_switch.j2')
print template.render(switch)
