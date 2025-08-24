# Use the official V2Ray image
FROM v2fly/v2fly-core:v5.17.1

# Copy the V2Ray configuration file
COPY v2ray.config.json /etc/v2ray/config.json

# Expose the port (will be overridden by DigitalOcean's PORT env var)
EXPOSE 8080

# Run V2Ray when the container starts
ENTRYPOINT ["v2ray", "run", "-c", "/etc/v2ray/config.json"]