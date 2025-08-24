import os
import sys

def generate_v2ray_config(template_path, output_path):
    """Generate V2Ray config from template using environment variables."""
    # Read the template
    with open(template_path, 'r') as f:
        template = f.read()
    
    # Get environment variables with defaults
    uuid = os.environ.get('VMESS_UUID', '34c0808e-ca5e-40c9-8e5d-6bacd84bc564')
    ws_path = os.environ.get('WS_PATH', '/ray')
    
    print(f"Generating V2Ray config with UUID: {uuid} and WS_PATH: {ws_path}")
    
    # Replace placeholders in the template
    config = template.replace('${VMESS_UUID}', uuid).replace('${WS_PATH}', ws_path)
    
    # Write the final config
    with open(output_path, 'w') as f:
        f.write(config)
    
    print("V2Ray config generated successfully.")
    print(f"Generated config:\n{config}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate_config.py <template_path> <output_path>")
        sys.exit(1)
    
    template_path = sys.argv[1]
    output_path = sys.argv[2]
    
    print(f"Template path: {template_path}")
    print(f"Output path: {output_path}")
    
    generate_v2ray_config(template_path, output_path)