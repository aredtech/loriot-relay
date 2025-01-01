import asyncio
import websockets
import json
import aiohttp

# WebSocket and Webhook details
WEBSOCKET_URL = "wss://me1pro.loriot.io/app?token=vgEAPAAAABBtZTFwcm8ubG9yaW90LmlvsaDEGT-LkIyknvOTQKFknA=="
WEBHOOK_URL = "http://host.docker.internal:8000/api/webhooks/"  # Replace with your POST endpoint URL

# Custom headers
HEADERS = {"Example-Header": "Example-Header-Value"}


# Function to send data to the webhook
async def send_to_webhook(session, data):
    print(data)
    try:
        async with session.post(WEBHOOK_URL, json=data, headers=HEADERS) as response:
            if response.status == 200:
                print(f"Sent: {data['EUI']}, Status: {response.status}")
            else:
                print(response)
                print(f"Failed to send: {data['EUI']}, Status: {response.status}")
    except Exception as e:
        print(f"Error sending data to webhook: {e}")


# Function to handle WebSocket communication
async def websocket_handler():
    async with websockets.connect(WEBSOCKET_URL) as websocket:
        page = 1
        total_pages = float("inf")  # Initialize to an unknown number of pages

        # Initialize HTTP session for webhook
        async with aiohttp.ClientSession() as session:
            while page <= total_pages:
                # Send a message to request data
                message = {"cmd": "cq", "page": page}
                await websocket.send(json.dumps(message))
                print(f"Sent: {message}")

                # Receive response
                response = await websocket.recv()
                data = json.loads(response)

                # Extract total and cache
                cache = data.get("cache", [])
                total = data.get("total", 0)
                per_page = len(cache)
                total_pages = (total // per_page) + (1 if total % per_page != 0 else 0)

                print(f"Page {page}/{total_pages}, Items received: {len(cache)}")

                # Send each item in cache to the webhook
                for item in cache:
                    await send_to_webhook(session, item)

                # Move to the next page
                page += 1

        print("All pages processed.")


# Main entry point
if __name__ == "__main__":
    asyncio.run(websocket_handler())
