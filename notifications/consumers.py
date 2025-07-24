import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed

from notifications.settings import get_config


class NotificationConsumer(WebsocketConsumer):
    def authenticate(self):
        headers = dict(self.scope["headers"])
        token = headers.get(b"token")
        if token:
            auth = JWTAuthentication()
            try:
                validated_token = auth.get_validated_token(token)
                return auth.get_user(validated_token), validated_token
            except (InvalidToken, AuthenticationFailed) as e:
                print(f"Socket Authentication Error: {e.args[0]}")
                return None
        else:
            print("Token missing.")
            return None

    def connect(self):
        user, validated_token = self.authenticate()
        if user is None:
            self.close()
            return

        self.user_key = f"user_{user.id}"

        for key in get_config()["SOCKET_EXTRA_KEYS"]:
            if value := validated_token.get(key):
                self.user_key += f"_{value}"

        async_to_sync(self.channel_layer.group_add)(
            self.user_key,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        if hasattr(self, 'user_key'):
            self.channel_layer.group_discard(
                self.user_key,
                self.channel_name
            )

    def notify(self, event):
        self.send(text_data=event['message'])

    # Receive message from WebSocket
    # def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json['message']
    #
    #     # Send message to room group
    #     async_to_sync(self.channel_layer.group_send)(
    #         self.room_group_name,
    #         {
    #             'type': 'chat_message',  # This maps to a method named chat_message
    #             'message': message
    #         }
    #     )
