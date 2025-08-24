# Use the official V2Ray image as the base
FROM v2fly/v2fly-core:latest

# Install Python 3 and Nginx (apk is the package manager for Alpine Linux, which the v2fly image is based on)
RUN apk add --no-cache python3 nginx

# Copy the V2Ray configuration template
COPY v2ray.config.template.json /etc/v2ray/config.template.json

# Copy the config generation script
COPY generate_config.py /app/generate_config.py

# Copy the VMess link server script
COPY vmess_link_server.py /app/vmess_link_server.py

# Copy the Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Make the scripts executable
RUN chmod +x /app/generate_config.py /app/vmess_link_server.py

# Expose the V2Ray port (this will be used internally)
EXPOSE 8080

# Use a shell script as the entrypoint to generate config and start services
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]