import json
from channels.generic.websocket import AsyncWebsocketConsumer

class UpdateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def send_update(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
