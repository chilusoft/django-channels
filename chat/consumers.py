# chat/consumers.py
import json
import random
import time
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChannelName
from channels.consumer import SyncConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        # async_to_sync(ChannelName.objects.create(channel_name=self.channel_name, channel_description=self.room_name))
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

class DataWidgetConsumer(SyncConsumer):

    def websocket_connect(self, event):
        self.send({
            "type": "websocket.accept",
        })
        print(event)

    def websocket_receive(self, event):
        for i in range(20):

            time.sleep(1)
            self.send({
                "type": "websocket.send",
                "text": f'{random.randint(1, 10)}',
            })
        # print(event)
    def websocket_disconnect(self, event):
        # print(event)
        pass