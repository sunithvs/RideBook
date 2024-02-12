import json

from channels.generic.websocket import AsyncWebsocketConsumer


class RideConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Retrieve the user ID from the scope
        user_id = self.scope["user"].id

        # Create a unique channel name for the driver
        driver_channel_name = f"driver_{user_id}"

        # Add the driver to the group with the unique channel name
        await self.channel_layer.group_add(
            driver_channel_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Clean up: Remove the user from the group when they disconnect
        user_id = self.scope["user"].id
        driver_channel_name = f"driver_{user_id}"
        await self.channel_layer.group_discard(
            driver_channel_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            # Send the received data back to the client
            await self.send(text_data=json.dumps({'message': text_data}))
        elif bytes_data:
            # Handle bytes_data if needed
            pass
