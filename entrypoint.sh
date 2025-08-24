#!/bin/sh

echo "Starting entrypoint script..."

# Generate the V2Ray configuration from the template
echo "Generating V2Ray configuration..."
python3 /app/generate_config.py /etc/v2ray/config.template.json /etc/v2ray/config.json

# Verify the generated config
echo "Generated V2Ray config:"
cat /etc/v2ray/config.json

# Start the V2Ray server in the background
echo "Starting V2Ray server..."
v2ray run -c /etc/v2ray/config.json &
V2RAY_PID=$!

# Start the VMess link server
echo "Starting VMess link server..."
python3 /app/vmess_link_server.py &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?