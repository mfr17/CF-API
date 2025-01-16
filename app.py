from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

# Input your accountId and tunnelId
account_id = ""  # Your Cloudflare Account ID
tunnel_id = ""  # Your Tunnel ID

# Input your credentials
email = ""  # Your Cloudflare email
token = ""  # Your Cloudflare API Token

# Initialize the Flask application
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) for this app
CORS(app)

# Route to fetch the current configuration from Cloudflare
@app.route('/get/config', methods=['GET'])
def get_config():
    # URL to get configuration for a specific tunnel
    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/cfd_tunnel/{tunnel_id}/configurations"

    # Set up headers with authentication and content type
    headers = {
        "X-Auth-Email": email,  # Auth email header
        "X-Auth-Key": token,    # API token for authentication
        "Content-Type": "application/json"
    }

    # Make a GET request to Cloudflare API
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()  # Parse JSON response
        return jsonify(data)    # Return the data as JSON
    else:
        # Return an error response if the request failed
        return jsonify({"error": "Failed to fetch data", "status_code": response.status_code})

# Route to update the configuration in Cloudflare
@app.route('/update/config', methods=['POST'])
def update_config():
    # Get the updated configuration from the request body
    updated_config = request.get_json()

    # URL to update configuration for a specific tunnel
    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/cfd_tunnel/{tunnel_id}/configurations"

    # Set up headers with authentication and content type
    headers = {
        "X-Auth-Email": email,  # Auth email header
        "X-Auth-Key": token,    # API token for authentication
        "Content-Type": "application/json"
    }

    # Make a PUT request to Cloudflare API with the updated configuration
    requests.put(url, headers=headers, json=updated_config)

    # Return a success response
    return jsonify({"success": True, "message": "Configuration updated successfully."}), 200

# Entry point for the Flask application
if __name__ == '__main__':
    # Run the Flask app in debug mode
    app.run(debug=True)
