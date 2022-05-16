import asyncio
from cgitb import text
from distutils.command.config import config
from pyexpat.errors import messages
from helper import Credential
from helper import Message
from helper.messages import Messages
from helper.settings import SettingHelper
from telethon import TelegramClient, events

credential: Credential = Credential.getTelegramCredential()

entities = {}
async def main():
    client = TelegramClient('session_name', credential.appId , credential.apiHash)
    await client.start()

    @client.on(events.NewMessage())
    async def handler(event):
        message = event.message
        wrapper = Message(text = message.message.lower(), isMedia = event.media != None)
        wrappers = Messages(channelId = str(message.peer_id.channel_id), messages = [wrapper])
        forward_setting, filteredMessages = SettingHelper.filterMessages(wrappers)
        if filteredMessages and len(filteredMessages.messages) > 0:
            destId = forward_setting.desination.id
            entity = None
            if destId not in entities:
                entity = await client.get_entity(int(destId))
                entities[destId] = entity
            else:
                entity = entities[destId]
            await client.forward_messages(entity=entity, messages=message)


    await client.run_until_disconnected()

        
asyncio.run(main())