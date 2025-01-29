# Flask Cloudflare Configuration Manager

This project is a Flask-based web application that interacts with the Cloudflare API to manage tunnel configurations. It provides a user-friendly interface to view and update configurations.

## Features

- **View Cloudflare Tunnel Configuration:** Fetch and display configuration details from Cloudflare.
- **Update Configuration:** Add or modify configuration settings using the web interface. Currently, it only supports adding data.
- **Integration with Cloudflare API:** Uses API tokens for secure communication.

## Requirements

- Python 3.x
- Flask
- Flask-CORS
- Requests library

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/mfr17/CF-API.git
    cd CF-API
    ```

2. Configure environment variables in the script:
   - Replace placeholders in the `app.py` script:
     - `account_id`
     - `tunnel_id`
     - `email`
     - `token`

## Usage

1. Start the Flask application:
    ```bash
    python app.py
    ```

2. Open `index.html` in your web browser.

3. Use the interface to fetch and update Cloudflare configurations.

## API Endpoints

- **GET `/get/config`**: Fetches the current Cloudflare tunnel configuration.
- **POST `/update/config`**: Updates the Cloudflare tunnel configuration.

## TODO

- **Modify Existing Data:** Implement functionality to modify existing configurations.
- **Delete Data:** Add an endpoint to delete specific configurations.

## Development

To contribute, fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

### Notes

- Ensure your Cloudflare API token has sufficient permissions to manage tunnel configurations.
- Handle your `account_id`, `tunnel_id`, and `token` securely, as they provide access to your Cloudflare account.
