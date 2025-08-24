# Use the official V2Ray image as the base
FROM v2fly/v2fly-core:latest

# Install Python 3 (apk is the package manager for Alpine Linux, which the v2fly image is based on)
RUN apk add --no-cache python3

# Copy the V2Ray configuration template
COPY v2ray.config.template.json /etc/v2ray/config.template.json

# Copy the config generation script
COPY generate_config.py /app/generate_config.py

# Copy the VMess link generator script
COPY vmess_link_generator.py /app/vmess_link_generator.py

# Make the scripts executable
RUN chmod +x /app/generate_config.py /app/vmess_link_generator.py

# Expose the V2Ray port
EXPOSE 8080

# Use a shell script as the entrypoint to generate config and start services
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]