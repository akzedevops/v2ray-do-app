#!/bin/sh

echo "Starting entrypoint script..."

# Debug: Print environment variables
echo "PORT environment variable: '$PORT'"
echo "All environment variables:"
env

# Generate the V2Ray configuration from the template
echo "Generating V2Ray configuration..."
python3 /app/generate_config.py /etc/v2ray/config.template.json /etc/v2ray/config.json

# Verify the generated config
echo "Generated V2Ray config:"
cat /etc/v2ray/config.json

# Start the V2Ray server in the background on port 8080
echo "Starting V2Ray server..."
v2ray run -c /etc/v2ray/config.json &
V2RAY_PID=$!

# Wait a moment for V2Ray to start
sleep 2

# Check if V2Ray is running
if kill -0 $V2RAY_PID 2>/dev/null; then
    echo "V2Ray started successfully with PID $V2RAY_PID"
else
    echo "Failed to start V2Ray"
    exit 1
fi

# Start the VMess link server (which will also act as a proxy)
echo "Starting VMess link server..."
python3 /app/vmess_link_server.py