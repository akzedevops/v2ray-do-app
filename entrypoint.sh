#!/bin/sh

echo "Starting entrypoint script..."

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

# Start the VMess link server in the background on port 8000
echo "Starting VMess link server..."
python3 /app/vmess_link_server.py &
SERVER_PID=$!

# Wait a moment for the server to start
sleep 2

# Replace the placeholder in the Nginx configuration with the actual port
# If PORT is not set, default to 8080
NGINX_PORT=${PORT:-8080}
echo "Configuring Nginx to listen on port $NGINX_PORT"
sed -i "s/{{PORT}}/$NGINX_PORT/g" /etc/nginx/nginx.conf

# Verify the Nginx config
echo "Nginx config:"
cat /etc/nginx/nginx.conf

# Start Nginx in the foreground
echo "Starting Nginx..."
nginx -g "daemon off;"