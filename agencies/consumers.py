import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Agency, Location

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '')

        # Broadcast message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

class LocationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.agency_id = None

    async def disconnect(self, close_code):
        if self.agency_id:
            # Optionally handle disconnect cleanup
            pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        agency_id = data.get('agency_id')
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        if agency_id and latitude and longitude:
            self.agency_id = agency_id
            await self.update_location(agency_id, latitude, longitude)
            # Broadcast updated location to all clients
            await self.channel_layer.group_send(
                "locations",
                {
                    "type": "location_update",
                    "agency_id": agency_id,
                    "latitude": latitude,
                    "longitude": longitude,
                }
            )

    async def location_update(self, event):
        await self.send(text_data=json.dumps({
            "agency_id": event["agency_id"],
            "latitude": event["latitude"],
            "longitude": event["longitude"],
        }))

    @database_sync_to_async
    def update_location(self, agency_id, latitude, longitude):
        try:
            agency = Agency.objects.get(id=agency_id)
            location, created = Location.objects.get_or_create(agency=agency)
            location.latitude = latitude
            location.longitude = longitude
            location.save()
        except Agency.DoesNotExist:
            pass
