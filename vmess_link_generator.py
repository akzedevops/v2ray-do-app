import os
import json
import base64

def get_vmess_config():
    """Generate VMess config dictionary from environment variables."""
    # Get environment variables with defaults
    app_url = os.environ.get('APP_URL', 'your-app-url-placeholder.ondigitalocean.app')
    uuid = os.environ.get('VMESS_UUID', '34c0808e-ca5e-40c9-8e5d-6bacd84bc564')
    ws_path = os.environ.get('WS_PATH', '/ray')
    
    # Construct the config
    config = {
        "v": "2",
        "ps": f"v2ray-do-app ({app_url})",  # Profile name
        "add": app_url,  # Address
        "port": "443",  # Port (443 for HTTPS)
        "id": uuid,  # UUID
        "aid": "0",  # AlterId
        "scy": "auto",  # Security
        "net": "ws",  # Network (WebSocket)
        "type": "none",  # Type
        "host": "",  # Host
        "path": ws_path,  # Path
        "tls": "tls",  # TLS
        "sni": "",  # SNI
        "alpn": "",  # ALPN
        "fp": ""  # Fingerprint
    }
    
    return config

def generate_vmess_link(config):
    """Generate a VMess link from the configuration."""
    json_str = json.dumps(config, separators=(',', ':'))
    encoded_str = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
    return f"vmess://{encoded_str}"

if __name__ == "__main__":
    # Get the app URL from the APP_URL environment variable
    # For local testing or if APP_URL is not set, we'll use a placeholder
    app_url = os.environ.get('APP_URL', 'your-app-url-placeholder.ondigitalocean.app')
    
    # Update the config with the app URL
    config = get_vmess_config()
    config["add"] = app_url
    config["ps"] = f"v2ray-do-app ({app_url})"
    
    # Generate and print the VMess link
    vmess_link = generate_vmess_link(config)
    print("VMess link for your V2Ray client:")
    print(vmess_link)
    print("")
    print("IMPORTANT: If you see 'your-app-url-placeholder.ondigitalocean.app' in the link above,")
    print("you need to set the APP_URL environment variable to your actual app URL.")
    print("In the DigitalOcean App Platform, this is automatically set.")
    print("For local testing, you can set it like this:")
    print("  export APP_URL=your-app-name.ondigitalocean.app")
    print("")
    print("To use this configuration in a V2Ray client:")
    print("- Copy the entire VMess link above")
    print("- In v2rayNG (Android): Tap the '+' button, select 'Import Config from Clipboard'")
    print("- In V2RayN (Windows): Right-click the tray icon, select 'Import VMess Link from Clipboard'")
    print("- In other clients: Look for an option to import from clipboard")