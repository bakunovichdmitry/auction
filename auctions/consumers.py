from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer


class AuctionConsumer(JsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_name = None

    def connect(self):
        auction_uuid = self.scope['url_route']['kwargs']['unique_id']
        self.group_name = 'auction_%s' % auction_uuid
        print(self.group_name)

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )
        self.close()

    def send_changed_data(self, event):
        self.send_json(
            {
                'data': event['data']
            }
        )
