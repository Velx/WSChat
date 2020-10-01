import json
import datetime
import time
import asyncio
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('chat', self.channel_name)
        await self.accept()
        message = await self.messages_init()
        await self.send(text_data=json.dumps(
            {
                'message': message,
                'type': 'next'
            },
            default=datetime_handler)
        )

    async def disconnect(self, code):
        await self.channel_layer.group_discard('chat', self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        if data.get('event'):
            messages = await self.get_messages(data['event']['type'], data['event']['id'])
            await self.send(text_data=json.dumps(
                {
                    'message': messages,
                    'type': data['event']['type']
                },
                default=datetime_handler)
            )

        else:
            if data['date']:
                asyncio.create_task(self.postponed_message(data['message'], self.scope["user"], data['date']))
            else:
                mes = await self.post_message(data['message'], self.scope["user"])
                if mes:
                    message = await self.messages_init()
                mes = json.dumps({'message': message, 'type': 'next'}, default=datetime_handler)
                await self.channel_layer.group_send(
                    'chat',
                    {
                        'type': 'chat_message',
                        'message': mes
                    }
                )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=message)

    @database_sync_to_async
    def messages_init(self):
        messages = Message.objects.all().values(
            'id', 'user__username', 'message', 'datetime').order_by('-id')[:20]
        return sorted(messages, key=lambda x: x['id'])

    @database_sync_to_async
    def get_messages(self, message_type, pk):
        if message_type == 'back':
            messages = Message.objects.filter(pk__lt=pk).values(
                'id', 'user__username', 'message', 'datetime').order_by('-id')[:20]
        else:
            messages = Message.objects.filter(pk__gt=pk).values(
                'id', 'user__username', 'message', 'datetime').order_by('id')[:20]
        return sorted(messages, key=lambda x: x['id'])

    @database_sync_to_async
    def post_message(self, text, user):
        if user.is_anonymous:
            user = None
        message = Message.objects.create(message=text, user=user)
        return message

    @database_sync_to_async
    def postponed_message(self, text, user, postponed_to):
        post_in = datetime.datetime.strptime(postponed_to, "%Y-%m-%dT%H:%M")
        time_to_wait = post_in - datetime.datetime.now()
        if time_to_wait.total_seconds() <= 0:
            pass
        else:
            time.sleep(time_to_wait.total_seconds())
            if user.is_anonymous:
                user = None
            message = Message.objects.create(message=text, user=user)
            if message:
                message = async_to_sync(self.messages_init)()
            mes = json.dumps({'message': message, 'type': 'next'}, default=datetime_handler)
            async_to_sync(self.channel_layer.group_send)(
                'chat',
                {
                    'type': 'chat_message',
                    'message': mes
                }
            )



def datetime_handler(obj):
    if isinstance(obj, datetime.datetime):
        return obj.strftime("%Y-%m-%d %H:%M:%S")
