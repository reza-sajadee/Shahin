from django.db.models.signals import post_save
from django.dispatch import receiver
from  .models import Messages
# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer
# @receiver(post_save , sender = Messages)
# def send_messages(sender , instance ,created , **kwargs):
#     if(created):
#         channel_layer = get_channel_layer()
#         group_name = 'user-messages'
#         event = {
#             'type' : 'user_joined',
#             'text' :instance.title
#         }
#         async_to_sync(channel_layer.group_send)(group_name , event)
      
