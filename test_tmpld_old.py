#!/usr/bin/env python
# -*- coding: utf-8 -*-
import yaml
from jinja2 import Environment, FileSystemLoader
with open("switch.yml", 'r') as ymlfile:
    switch = yaml.load(ymlfile)
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('test-template')
print template.render(switch)
