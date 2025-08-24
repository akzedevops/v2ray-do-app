import os
import json
import base64
from http.server import HTTPServer, BaseHTTPRequestHandler

# V2Ray VMess configuration details
# These should match the settings in your v2ray.config.json and the DigitalOcean app URL
VMessConfig = {
    "v": "2",
    "ps": "v2ray-do-app",  # Profile name
    "add": "oyster-app-34tkd.ondigitalocean.app",  # Address (DigitalOcean App URL)
    "port": "443",  # Port (443 for HTTPS, which DigitalOcean App Platform uses)
    "id": "34c0808e-ca5e-40c9-8e5d-6bacd84bc564",  # UUID
    "aid": "0",  # AlterId
    "scy": "auto",  # Security
    "net": "ws",  # Network (WebSocket)
    "type": "none",  # Type (for WebSocket, usually 'none')
    "host": "",  # Host (can be left empty for WebSocket)
    "path": "/ray",  # Path (WebSocket path)
    "tls": "tls",  # TLS (enable for HTTPS)
    "sni": "",  # SNI (can be left empty)
    "alpn": "",  # ALPN (can be left empty)
    "fp": ""  # Fingerprint (can be left empty)
}

def generate_vmess_link(config):
    """Generate a VMess link from the configuration."""
    json_str = json.dumps(config, separators=(',', ':'))
    encoded_str = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
    return f"vmess://{encoded_str}"

class ConfigHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Serve the VMess link as plain text
            vmess_link = generate_vmess_link(VMessConfig)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            
            # Send the VMess link
            self.wfile.write(vmess_link.encode('utf-8'))
        else:
            # Serve a 404 page for other paths
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Page not found')

def run_server(port):
    server_address = ('', port)
    httpd = HTTPServer(server_address, ConfigHandler)
    print(f"Config server running on port {port}")
    print(f"VMess link: {generate_vmess_link(VMessConfig)}") # Also print to console/logs
    httpd.serve_forever()

if __name__ == '__main__':
    # Get the port from the environment variable, default to 8000 if not set
    # DigitalOcean App Platform sets the PORT environment variable
    port = int(os.environ.get('PORT', 8000))
    run_server(port)