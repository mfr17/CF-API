from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

# Input your accountId and tunnelId 
account_id = ""  # Your Account ID 
tunnel_id = ""  # Your Tunnel ID

# Input your Credentials
email = ""  # Your Email registered on Cloudlared
token = ""  # Your API Token

# Initialize Flask application and enable CORS
app = Flask(__name__)
CORS(app)

# Define base URLs for API requests
BASE_URL = "https://api.cloudflare.com/client/v4/accounts/{}/cfd_tunnel/{}"
ZONE_URL = "https://api.cloudflare.com/client/v4/zones"

def get_headers():
    # Return headers required for API requests
    return {
        "X-Auth-Email": email, 
        "X-Auth-Key": token, 
        "Content-Type": "application/json"
    }

@app.route('/get/config', methods=['GET'])
def get_config():
    # Fetch the configuration for the specified tunnel
    url = BASE_URL.format(account_id, tunnel_id) + "/configurations"
    headers = get_headers()

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to fetch data", "status_code": response.status_code})

@app.route('/update/config', methods=['POST'])
def update_config():
    # Update the configuration and DNS record for the specified tunnel
    data = request.get_json()
    updated_config = data.get('config')
    hostname = data.get('hostname')
    
    tunnel_url = BASE_URL.format(account_id, tunnel_id) + "/configurations"
    headers = get_headers()

    # Retrieve zones to find the correct domain
    get_zones = requests.get(ZONE_URL, headers=headers)
    if get_zones.status_code != 200:
        return jsonify({"error": "Failed to retrieve zones", "status_code": get_zones.status_code})

    data = get_zones.json()
    parts = [part for part in hostname.split('.') if part]

    # Determine domain and subdomain from hostname
    if len(parts) > 2:
        domain = '.'.join(parts[1:])
        subdomain = parts[0]
    else:
        domain = hostname
        subdomain = ""

    # Filter zones to find the matching domain
    domain_zones = [
        {"id": zone['id'], "name": zone['name']} 
        for zone in data.get('result', []) 
        if zone['name'] == domain
    ]

    # Prepare DNS data for the new record
    dns_data = {
        "type": "CNAME",
        "name": subdomain if subdomain else hostname,
        "content": f"{tunnel_id}.cfargotunnel.com",
        "ttl": 1,
        "proxied": True
    }

    # Update the tunnel configuration
    tunnel = requests.put(tunnel_url, headers=headers, json=updated_config)
    if tunnel.status_code != 200:
        return jsonify({"error": "Failed to update tunnel", "status_code": tunnel.status_code})

    # Add the DNS record for the specified domain
    dns_url = f"https://api.cloudflare.com/client/v4/zones/{domain_zones[0]['id']}/dns_records"
    dns = requests.post(dns_url, headers=headers, json=dns_data)
    if dns.status_code != 200:
        return jsonify({"error": "Failed to add DNS record", "status_code": dns.status_code})

    return jsonify({"success": True, "message": "Configuration updated and DNS record added successfully."}), 200

if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=False)