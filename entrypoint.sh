#!/bin/sh

echo "Starting entrypoint script..."

# Generate the V2Ray configuration from the template
echo "Generating V2Ray configuration..."
python3 /app/generate_config.py /etc/v2ray/config.template.json /etc/v2ray/config.json

# Verify the generated config
echo "Generated V2Ray config:"
cat /etc/v2ray/config.json

# Generate and print the VMess link
echo ""
echo "Generating VMess link..."
python3 /app/vmess_link_generator.py

# Start the V2Ray server
echo ""
echo "Starting V2Ray server..."
v2ray run -c /etc/v2ray/config.json