from channels.generic.websocket import AsyncJsonWebsocketConsumer


class DashboardSocket(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.session_name = "ui_%s" % str(self.user.pk)

        await self.channel_layer.group_add(self.session_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.session_name, self.channel_name)

    async def send_event(self, event, content):
        await self.send_json({"event": event, "data": content})

    # async def receive_json(self, content, **kwargs):
    #     await self.send_json(
    #         await self.send_notification("alert_success", "Test", "Test success")
    #     )

    async def send_notification(self, content):
        data = content["data"]

        await self.send_json(
            {
                "type": "notification",
                "data": {
                    "type": data["type"],
                    "title": data["title"] if "title" in data else None,
                    "content": data["content"],
                },
            }
        )
