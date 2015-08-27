## ABOUT
This is a Jinja2 template for classic IOS switches including some common best practices configuration.

It's inspired by [Mierdin/jinja2-nxos-config](https://github.com/Mierdin/jinja2-nxos-config)

Additionally, i added a Vlan "Census" tool. It's meant as a utility to have a quick overview of which vlan is present on which switch. Given a list of hosts and some common settings from YaML files, it will trawl a network and present a table of each vlan and the switch it's configured on.

## HOW
It uses a yaml files for device-specific configuration. One file per device, containing details for management and for data plane operation (which vlans, where etc.)

## REQUIREMENTS

It needs Python2 (obviously) with Jinja2 and YAML support.

