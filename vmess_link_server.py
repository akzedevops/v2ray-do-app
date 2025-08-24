import os
import json
import base64
import http.server
import socketserver
import urllib.request
import urllib.parse
import urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler

def get_vmess_config():
    """Generate VMess config dictionary from environment variables."""
    # Get environment variables with defaults
    # For APP_URL, we'll use a placeholder for now and replace it dynamically in the request handler
    app_url = os.environ.get('APP_URL', 'your-app-url-placeholder.ondigitalocean.app')
    uuid = os.environ.get('VMESS_UUID', '34c0808e-ca5e-40c9-8e5d-6bacd84bc564')
    ws_path = os.environ.get('WS_PATH', '/ray')
    
    # Construct the config
    config = {
        "v": "2",
        "ps": f"v2ray-do-app",  # Profile name
        "add": app_url,  # Address (will be replaced dynamically)
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

# HTML template for the web page
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>V2Ray Configuration</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            display: inline-block;
            margin-top: 20px;
            max-width: 600px;
        }}
        h1 {{
            color: #333;
        }}
        .vmess-link {{
            background-color: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            word-wrap: break-word;
            margin: 20px 0;
            text-align: left;
            font-family: monospace;
            font-size: 14px;
            border: 1px solid #ddd;
        }}
        .instructions {{
            text-align: left;
            margin: 20px 0;
        }}
        .copy-button {{
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }}
        .copy-button:hover {{
            background-color: #45a049;
        }}
        .footer {{
            margin-top: 20px;
            color: #777;
            font-size: 14px;
        }}
        .note {{
            background-color: #e7f3ff;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
            text-align: left;
            border-left: 5px solid #1a73e8;
        }}
    </style>
</head>
<body>
    <h1>Your V2Ray Server is Ready</h1>
    <div class="container">
        <p>Copy the VMess link below and use it in your V2Ray client.</p>
        
        <div class="vmess-link" id="vmess-link">
            {vmess_link}
        </div>
        
        <button class="copy-button" onclick="copyToClipboard()">Copy VMess Link</button>
        
        <div class="note">
            <strong>Note:</strong> This configuration is specific to your deployment. Keep it secure and do not share it publicly.
        </div>
        
        <div class="instructions">
            <h3>Client Setup Instructions:</h3>
            <ul>
                <li><strong>v2rayNG (Android):</strong> Tap the "+" button, select "Import Config from Clipboard".</li>
                <li><strong>V2RayN (Windows):</strong> Right-click the tray icon, select "Import VMess Link from Clipboard".</li>
                <li><strong>Other clients:</strong> Look for an option to import from clipboard or manually enter the details.</li>
            </ul>
        </div>
    </div>
    
    <script>
        function copyToClipboard() {{
            const vmessLink = document.getElementById('vmess-link').innerText;
            navigator.clipboard.writeText(vmessLink).then(() => {{
                alert('VMess link copied to clipboard!');
            }}).catch(err => {{
                console.error('Failed to copy: ', err);
                // Fallback for older browsers
                const textArea = document.createElement('textarea');
                textArea.value = vmessLink;
                document.body.appendChild(textArea);
                textArea.select();
                try {{
                    const successful = document.execCommand('copy');
                    if (successful) {{
                        alert('VMess link copied to clipboard!');
                    }} else {{
                        alert('Failed to copy VMess link.');
                    }}
                }} catch (err) {{
                    console.error('Fallback: Oops, unable to copy', err);
                    alert('Failed to copy VMess link. Please copy it manually.');
                }}
                document.body.removeChild(textArea);
            }});
        }}
    </script>
</body>
</html>
"""

class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Handle requests for the VMess link
        if self.path == '/' or self.path == '/config':
            # For the root path, we'll try to get the actual app URL from the request
            # If that's not available, we'll fall back to the environment variable
            host_header = self.headers.get('Host')
            if host_header:
                app_url = host_header
            else:
                app_url = os.environ.get('APP_URL', 'your-app-url-placeholder.ondigitalocean.app')
            
            # Temporarily update the config with the actual app URL for this request
            config = get_vmess_config()
            config["add"] = app_url
            config["ps"] = f"v2ray-do-app ({app_url})"
            
            # Serve the HTML page with the VMess link
            vmess_link = generate_vmess_link(config)
            html_content = HTML_TEMPLATE.format(vmess_link=vmess_link)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
        elif self.path == '/vmess':
            # Serve the VMess link as plain text
            host_header = self.headers.get('Host')
            if host_header:
                app_url = host_header
            else:
                app_url = os.environ.get('APP_URL', 'your-app-url-placeholder.ondigitalocean.app')
            
            config = get_vmess_config()
            config["add"] = app_url
            config["ps"] = f"v2ray-do-app ({app_url})"
            
            vmess_link = generate_vmess_link(config)
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(vmess_link.encode('utf-8'))
        else:
            # Proxy all other requests to V2Ray
            self.proxy_request()
    
    def do_POST(self):
        # Proxy POST requests to V2Ray
        self.proxy_request()
    
    def do_PUT(self):
        # Proxy PUT requests to V2Ray
        self.proxy_request()
    
    def do_DELETE(self):
        # Proxy DELETE requests to V2Ray
        self.proxy_request()
    
    def do_HEAD(self):
        # Proxy HEAD requests to V2Ray
        self.proxy_request()
    
    def do_OPTIONS(self):
        # Proxy OPTIONS requests to V2Ray
        self.proxy_request()
    
    def do_PATCH(self):
        # Proxy PATCH requests to V2Ray
        self.proxy_request()
    
    def proxy_request(self):
        # Proxy the request to V2Ray
        try:
            # Construct the URL for V2Ray
            v2ray_url = f"http://127.0.0.1:8080{self.path}"
            
            # Create a request to V2Ray
            if self.command == 'GET':
                req = urllib.request.Request(v2ray_url)
            else:
                # For POST, PUT, etc., we need to read the request body
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length) if content_length > 0 else None
                req = urllib.request.Request(v2ray_url, data=post_data, method=self.command)
            
            # Copy headers from the original request
            for header in ['User-Agent', 'Accept', 'Accept-Language', 'Accept-Encoding', 'Connection', 'Upgrade', 'Content-Type', 'Content-Length']:
                if header in self.headers:
                    req.add_header(header, self.headers[header])
            
            # Send the request to V2Ray
            with urllib.request.urlopen(req) as response:
                # Send the response back to the client
                self.send_response(response.getcode())
                # Copy headers from V2Ray's response
                for header, value in response.getheaders():
                    if header.lower() != 'transfer-encoding':  # Skip transfer-encoding header
                        self.send_header(header, value)
                self.end_headers()
                # Copy the response body
                self.wfile.write(response.read())
        except urllib.error.HTTPError as e:
            # Handle HTTP errors from V2Ray
            self.send_response(e.code)
            # Copy headers from the error response
            for header, value in e.headers.items():
                if header.lower() != 'transfer-encoding':
                    self.send_header(header, value)
            self.end_headers()
            # Copy the error response body
            self.wfile.write(e.read())
        except Exception as e:
            # Handle other errors
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Proxy error: {str(e)}".encode('utf-8'))

def run_server(port):
    server_address = ('', port)
    httpd = HTTPServer(server_address, ProxyHandler)
    print(f"VMess link server and proxy running on port {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    # Get the port from the environment variable, default to 8080 if not set
    port = int(os.environ.get('PORT', 8080))
    run_server(port)