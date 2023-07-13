import json
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from django.template.loader import get_template
from  .models import Notifications
from profile_app.models import Profile

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        # Join room group
        self.GROUP_NAME = 'user-notifications'
        async_to_sync(self.channel_layer.group_add)(
            self.GROUP_NAME, self.channel_name
        )

        print('userconnect')
        self.accept()
    def user_joined(self , event ):
        #self.send(text_data='من خوبم')
        print('userjoined')
     
        profileNot =Profile.objects.all().filter(user=self.scope["user"])[0]
        notifications = Notifications.objects.all().filter(recivers = profileNot).order_by('-created_at').filter(personalStatus ='pending')
        
        #notifications = Notifications.objects.all().filter(reciver__user__id = self.scope["user"])
        html = get_template('partials/notification2.html').render(
            context = {'notifications' : notifications}
        )
        print(html , '***********')
        self.send(text_data = html)
        
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.GROUP_NAME, self.channel_name
        )
    def receive(self, text_data=None, bytes_data=None):
        # Called with either text_data or bytes_data for each frame
        # You can call:
        self.send(text_data="Hello world!")
        # Or, to send a binary frame:
        self.send(bytes_data="Hello world!")
        # Want to force-close the connection? Call:
        self.close()
        # Or add a custom WebSocket error code!
        self.close(code=4123)