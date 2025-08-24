# V2Ray Server on DigitalOcean App Platform

This project provides a template for deploying a V2Ray server using the DigitalOcean App Platform.

## Components

- `Dockerfile`: Defines the container image using the official V2Ray image.
- `v2ray.config.json`: The V2Ray configuration file.
  - Listens on the port defined by the `PORT` environment variable (set by DigitalOcean).
  - Uses VMess protocol with WebSocket transport on path `/ray`.
  - The user ID (UUID) is hardcoded in the config. You should change this for security.

## Deployment Instructions

### Prerequisites

1. A DigitalOcean account.
2. This project code hosted in a Git repository (e.g., GitHub, GitLab).

### Steps

1. **Fork or Clone this Repository**: If you haven't already, get this code into your own Git repository.
2. **Update UUID (Recommended for Security)**:
   - Generate a new UUID (you can use `python -c "import uuid; print(uuid.uuid4())"`).
   - Replace the `id` value in `v2ray.config.json` with your new UUID.
3. **Create an App on DigitalOcean**:
   - Go to the [DigitalOcean Control Panel](https://cloud.digitalocean.com/).
   - Navigate to `Apps` (under the 'Manage' section).
   - Click `Create App`.
4. **Configure Source**:
   - Choose your Git repository provider and select this repository.
   - Select the branch you want to deploy (e.g., `main`).
5. **Configure App**:
   - DigitalOcean should automatically detect the `Dockerfile`.
   - Ensure the `Source directory` is set correctly (usually `/` for this project).
   - No specific build command is needed as it's a Dockerfile deployment.
6. **Set Environment Variables (Not strictly needed for basic setup, but good to know)**:
   - The `PORT` environment variable is automatically set by DigitalOcean App Platform. Our config uses `{{.PORT}}` to reference it.
7. **Finalize and Deploy**:
   - Review the plan.
   - Choose your region.
   - Decide on the plan (the free tier might suffice for light personal use, but check DigitalOcean's current offerings).
   - Click `Launch App`.

### Client Configuration

To connect to your V2Ray server, you'll need a client that supports VMess.

- **Address**: The URL of your deployed DigitalOcean app (e.g., `https://your-app-name.ondigitalocean.app`).
- **Port**: 443 (if using HTTPS, which is typical for App Platform apps).
- **ID**: The UUID you used in `v2ray.config.json`.
- **AlterId**: 0 (as configured).
- **Security**: auto (or aes-128-gcm if your client requires it explicitly).
- **Network**: ws (WebSocket).
- **Path**: `/ray`.
- **TLS**: tls (enable).

**Note**: DigitalOcean App Platform typically provides HTTPS endpoints automatically. Make sure your client is configured to use `wss` (WebSocket Secure) if connecting via HTTPS.

Enjoy your V2Ray server!