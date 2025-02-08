import asyncio
import websockets
import json
import aiohttp
import os
from datetime import datetime

# WebSocket and Webhook details
WEBSOCKET_URL = ""
WEBHOOK_URL = ""

# Custom headers
HEADERS = {"X-Loriot-For": "nAirQua"}

# List of EUIs to monitor
ALLOWED_EUIS = [
    "24E124707E238848",
    # Add more EUIs here
]

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

# Function to write data to a file
async def write_to_file(data, filename=None):
    if filename is None:
        # Generate a default filename with timestamp if none provided
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"loriot_data_{timestamp}.json"
    
    try:
        # Create a data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)
        filepath = os.path.join('data', filename)
        
        # Append the data to the file
        with open(filepath, 'a') as f:
            json.dump(data, f)
            f.write('\n')  # Add newline for better readability
        
        print(f"Written: {data['EUI']} to {filepath}")
    except Exception as e:
        print(f"Error writing data to file: {e}")

# Function to handle WebSocket communication
async def websocket_handler(use_webhook=False, filename=None):
    try:
        async with websockets.connect(WEBSOCKET_URL) as websocket:
            page = 1
            total_pages = float("inf")  # Initialize to an unknown number of pages

            # Initialize HTTP session for webhook if needed
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

                    # Filter items by EUI
                    filtered_cache = [item for item in cache if item.get("EUI") in ALLOWED_EUIS]
                    
                    print(f"Page {page}/{total_pages}, Total items: {len(cache)}, Filtered items: {len(filtered_cache)}")

                    # Process each filtered item
                    for item in filtered_cache:
                        if use_webhook:
                            await send_to_webhook(session, item)
                        else:
                            await write_to_file(item, filename)

                    # Move to the next page
                    page += 1
                    
    except Exception as e:
        print(f"Error in websocket handler: {e}")
        while True:
            pass
            # print("Reconnecting...")
            # try:
            #     await websocket_handler(use_webhook, filename)
            # except Exception as reconnect_error:
            #     print(f"Reconnection failed: {reconnect_error}")
            #     await asyncio.sleep(5)  # Wait 5 seconds before trying again

# Main entry point
if __name__ == "__main__":
    # Example usage:
    # To write to a file:
    asyncio.run(websocket_handler(use_webhook=True, filename="my_data.json"))
    
    # To use webhook:
    # asyncio.run(websocket_handler(use_webhook=True))