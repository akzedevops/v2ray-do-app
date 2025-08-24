# V2Ray Server on DigitalOcean App Platform

This project provides a template for deploying a V2Ray server using the DigitalOcean App Platform.

## Components

- `Dockerfile`: Defines the container image using the official V2Ray image.
- `v2ray.config.template.json`: A template for the V2Ray configuration file.
- `generate_config.py`: A Python script to generate the V2Ray configuration from the template using environment variables.
- `vmess_link_generator.py`: A Python script to generate the VMess link.
- `entrypoint.sh`: A shell script that generates the V2Ray configuration and starts the V2Ray server.

## Environment Variables

The following environment variables can be set to configure the V2Ray server:

- `VMESS_UUID`: The UUID for the VMess inbound. Default: `34c0808e-ca5e-40c9-8e5d-6bacd84bc564`.
- `WS_PATH`: The WebSocket path. Default: `/ray`.

## Deployment Instructions

### Prerequisites

1. A DigitalOcean account.
2. This project code hosted in a Git repository (e.g., GitHub, GitLab).

### Steps

1. **Fork or Clone this Repository**: If you haven't already, get this code into your own Git repository.
2. **(Optional) Update UUID**:
   - Generate a new UUID (you can use `python -c "import uuid; print(uuid.uuid4())"`).
   - You can either set the `VMESS_UUID` environment variable in the DigitalOcean App Platform settings or modify the default value in `generate_config.py`.
3. **Create an App on DigitalOcean**:
   - Go to the [DigitalOcean Control Panel](https://cloud.digitalocean.com/).
   - Navigate to `Apps` (under the 'Manage' section).
   - Click `Create App`.
4. **Configure Source**:
   - Choose your Git repository provider and select this repository.
   - Select the branch you want to deploy (e.g., `main` or `vmess-link-generator`).
5. **Configure App**:
   - DigitalOcean should automatically detect the `Dockerfile`.
   - Ensure the `Source directory` is set correctly (usually `/` for this project).
   - No specific build command is needed as it's a Dockerfile deployment.
6. **Set Environment Variables (Optional but Recommended)**:
   - In the DigitalOcean App Platform settings, you can set environment variables.
   - Set `VMESS_UUID` to your desired UUID.
   - Set `WS_PATH` if you want to use a different WebSocket path.
   - The `PORT` environment variable is automatically set by DigitalOcean App Platform.
7. **Finalize and Deploy**:
   - Review the plan.
   - Choose your region.
   - Decide on the plan (the free tier might suffice for light personal use, but check DigitalOcean's current offerings).
   - Click `Launch App`.

### Accessing the VMess Link

After deployment, the app will print the VMess link to the console logs during startup. You can find this link in the app's logs in the DigitalOcean Control Panel.

Alternatively, you can generate the VMess link locally by running the `vmess_link_generator.py` script with the correct environment variables:

```bash
# Set the environment variables
export APP_URL=your-app-name.ondigitalocean.app
export VMESS_UUID=your-uuid
export WS_PATH=/ray

# Run the script
python vmess_link_generator.py
```

Replace `your-app-name.ondigitalocean.app` with the actual URL of your deployed app.

### Client Configuration

To connect to your V2Ray server, you'll need a client that supports VMess.

- **Address**: The URL of your deployed DigitalOcean app (e.g., `your-app-name.ondigitalocean.app`).
- **Port**: 443 (if using HTTPS, which is typical for App Platform apps).
- **ID**: The UUID you used (either the default or the one set via `VMESS_UUID`).
- **AlterId**: 0 (as configured).
- **Security**: auto (or aes-128-gcm if your client requires it explicitly).
- **Network**: ws (WebSocket).
- **Path**: `/ray` (or the value of `WS_PATH` if you changed it).
- **TLS**: tls (enable).

**Note**: DigitalOcean App Platform typically provides HTTPS endpoints automatically. Make sure your client is configured to use `wss` (WebSocket Secure) if connecting via HTTPS.

Enjoy your V2Ray server!