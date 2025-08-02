from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from .models import Message, User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("aagya hero")
        await self.accept()
        self.user = self.scope["user"]
        self.partner_id = self.scope["url_route"]["kwargs"]["partner_id"]
        self.room_name = self.get_room_name(self.user.id, self.partner_id)
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]

        await self.save_message(self.user.id, self.partner_id, message)

        await self.channel_layer.group_send(self.room_group_name, {
            "type": "chat_message",
            "message": message,
            "sender_id": self.user.id
        })    

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender_id": event["sender_id"],
        }))

    def get_room_name(self, user1, user2):
        return f"{min(user1, user2)}_{max(user1, user2)}"
    
    @database_sync_to_async
    def save_message(self, sender_id, receiver_id, content):
        return Message.objects.create(sender_id=sender_id, receiver_id= receiver_id, content=content)
    