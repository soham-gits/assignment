from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Handles new WebSocket connections."""
        self.room_group_name = "private_chat"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        print("WebSocket Connected")

    async def disconnect(self, close_code):
        """Handles WebSocket disconnections."""
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        print("WebSocket Disconnected")

    async def receive(self, text_data):
        """Receives and broadcasts messages to the chat group."""
        try:
            data = json.loads(text_data)
            message = data.get("message", "")
            sender = data.get("sender", "")

            if message and sender:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "chat_message",
                        "message": message,
                        "sender": sender,
                    }
                )
                print(f"Received & Broadcasting: {message} from {sender}")
            else:
                print("Empty message or sender")
        except json.JSONDecodeError:
            print("Invalid JSON received")

    async def chat_message(self, event):
        """Sends messages to WebSocket clients."""
        message = event["message"]
        sender = event["sender"]
        await self.send(text_data=json.dumps({"sender": sender, "message": message}))
        print(f"Sent: {message} from {sender}")
