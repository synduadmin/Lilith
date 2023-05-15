# CHAT_ASGI APP, consumers.py
import json
import logging
import os
from django.core.asgi import get_asgi_application
from channels.generic.websocket import AsyncWebsocketConsumer
from chatbot.views import chatbot
from chatbot.models import ChatSession
from channels.db import database_sync_to_async
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from django.urls import re_path

logger = logging.getLogger(__name__)
ASGI_APPLICATION = os.environ.get("ASGI_APPLICATION")


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.debug("made it to the chat consumer connect endpoint")

        #logger.debug("ASGI_APPLICATION: %s", ASGI_APPLICATION)
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        self.user = self.scope["user"]

        username = self.user.username #add check that the user has permissions
        self.websocket_id = f"websocket_{self.room_name}"
        await self.get_session()

        #logger.debug("user: %s", self.user)

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        #logger.debug("made it to the chat consumer disconnect endpoint")

        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        #logger.debug("made it to the chat receive endpoint")

        logger.debug("in asgi receive endpoint")
        logger.debug(f"user is {self.user}")

        text_data_json = json.loads(text_data)
        logger.debug(text_data_json)

        message = text_data_json["message"]
        logger.debug(f"receive message: {message}")

        try:
            session = await self.get_session()
            # this is an initial implementation which serializes everything
            # ffu - replace with async io
            message = await self.interact(
                "user", self.user, message, session, text_data
            )
        except ChatSession.DoesNotExist:
            logger.debug("failed to load chat session")

        # Send message to room group
        logger.debug(f"interact completed, trying to send message : {message} back to client")
        logger.debug(f"this is the name of the room in consumer receive {self.room_group_name}")
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    @database_sync_to_async
    def get_session(self):
        #logger.debug("made it to the chat get session endpoint")

        # get or create
        session, created = ChatSession.objects.get_or_create(
            author=self.user, 
            session_name=self.room_name,
            defaults={
        'author': self.user,
        'session_name': self.room_name})
        if created:
            session.save()

        self.session = session
        logger.debug(f"SID : {self.session.session_name}")
        return self.session

    @database_sync_to_async
    def interact(self, role, user, message, session, text_data):
        #logger.debug("made it to the chat interact endpoint")

        logger.debug("in consumers.py interact")
        logger.debug(f"session: {session.id}")
        logger.debug(f"message: {message}")
        logger.debug(f"user: {user}")
        logger.debug(f"text_data: {text_data}")

        try:
            cb = chatbot()
            msg = cb.interact(role, user, message, session, text_data)
            json_content = msg.content.decode("utf-8")
            #logger.debug("JSON object content: %s", json_content)
            return json_content

        except Exception as e:
            logger.debug(f"error: {e}")
            error_message = f"I'm sorry, something in my models went wrong. {e}"
            json_content = json.dumps({"response": error_message})
            return json_content

    # Receive message from room group
    async def chat_message(self, event):
        logger.debug("made it to the chat chat_message endpoint")
        logger.debug(f'this is the event {event["message"]}')

        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
