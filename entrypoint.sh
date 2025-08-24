#!/bin/sh

# Generate the V2Ray configuration from the template
python3 /app/generate_config.py /etc/v2ray/config.template.json /etc/v2ray/config.json

# Start the V2Ray server in the background
v2ray run -c /etc/v2ray/config.json &

# Start the VMess link server
python3 /app/vmess_link_server.py