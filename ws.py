import asyncio
import websockets
import json

async def chat():
    uri = "ws://localhost:8000/ws/chat/2/"  # Change '2' to receiver user ID

    async with websockets.connect(uri) as websocket:
        print("Connected to server!")

        # Send a message
        message = {
            "message": "Hello from Python tester!"
        }
        await websocket.send(json.dumps(message))
        print(f"Sent: {message['message']}")

        # Wait for a response
        response = await websocket.recv()
        data = json.loads(response)
        print(f"Received: {data}")

        # Optional: Keep the connection open to send/receive more
        while True:
            text = input("Enter message (or type 'exit' to quit): ")
            if text.lower() == "exit":
                break
            await websocket.send(json.dumps({"message": text}))
            response = await websocket.recv()
            print(f"Received: {json.loads(response)}")

asyncio.run(chat())