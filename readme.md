# WebSocket to Webhook Relay

A Python-based project to fetch paginated data from a WebSocket endpoint and relay each item to a webhook. This project is ideal for real-time data processing and integration tasks.

## Features

- **WebSocket Integration**: Connects to a WebSocket server to fetch data.
- **Pagination Support**: Automatically handles paginated responses.
- **Webhook Relay**: Sends each data item as a POST request to a configured webhook.
- **Asynchronous Execution**: Utilizes Python's `asyncio` and `aiohttp` for efficient operations.
- **Dynamic Headers**: Supports custom HTTP headers for webhook requests.

---

## Requirements

- Docker (recommended)
- Alternatively: Python 3.8+ with required libraries (`websockets`, `aiohttp`)

---

## Installation

### Using Docker (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/websocket-to-webhook.git
   cd websocket-to-webhook
   ```

2. Build the Docker image:
   ```bash
   docker build -t websocket-to-webhook .
   ```

3. Run the Docker container:
   ```bash
   docker run -d --name websocket-webhook-relay websocket-to-webhook
   ```

### Using Python Directly

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/websocket-to-webhook.git
   cd websocket-to-webhook
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the script:
   ```bash
   python main.py
   ```

---

## Configuration

1. **WebSocket URL**: Replace the `WEBSOCKET_URL` value in the script with your WebSocket endpoint.
2. **Webhook URL**: Replace the `WEBHOOK_URL` value in the script with your POST endpoint.
3. **Headers**: Add or modify custom headers in the `HEADERS` dictionary.

Example configuration in `main.py`:
```python
WEBSOCKET_URL = "wss://your-websocket-url"
WEBHOOK_URL = "https://your-webhook-url"

HEADERS = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}
```

---

## Usage

### Docker

1. Make sure the `WEBSOCKET_URL` and `WEBHOOK_URL` in `main.py` are configured.
2. Build and run the Docker container (see Installation steps above).

### Local Python Environment

1. Configure the URLs in `main.py`.
2. Run the script:
   ```bash
   python main.py
   ```

---

## How It Works

1. Connects to the WebSocket endpoint.
2. Sends a request with pagination (`cmd`, `page`).
3. Processes the `cache` array from the WebSocket response.
4. Sends each item in `cache` to the webhook.
5. Automatically fetches the next page until all data is processed.

---

## Example Output

```plaintext
Sent: 24E124707E239183, Status: 200
Sent: 24E124707E239184, Status: 200
Page 1/24, Items received: 100
Sent: 24E124707E239185, Status: 200
...
All pages processed.
```

---

## Dependencies

If not using Docker, ensure the following dependencies are installed:

- `websockets==12.0`
- `aiohttp==3.8.4`

Install them with:
```bash
pip install -r requirements.txt
```

---

## Contribution

Feel free to fork this repository, submit issues, or make pull requests. Contributions are welcome!

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.