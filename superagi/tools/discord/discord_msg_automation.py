import discord
from superagi.helper.discord_msg_automation import handle_response
from superagi.config.config import get_config
from typing import Type, List
from pydantic import BaseModel, Field
from superagi.tools.base_tool import BaseTool
# scopes
intents = discord.Intents.default()
intents.message_content = True
intents.presences = False

class DiscordMsgSchema(BaseModel):
    pass

class DiscordMsgTool(BaseTool):
    name = "Discord Message Tool"
    description = (
        "A tool for performing a message automation for a specific Discord channel."
        "Input should be a commend query for chat bot, it will be retrived from dicord channel."
    )
    args_schema: Type[DiscordMsgSchema] = DiscordMsgSchema
# Send messages
    async def send_message(self,message, user_message, is_private):
        try:
            response = handle_response(user_message)
            await message.author.send(response) if is_private else await message.channel.send(response)

        except Exception as e:
            print(e)
            print("is private--->"+str(is_private))


    def run_discord_bot(self):
        TOKEN =  get_config("DISCORD_TOKEN")
        client = discord.Client(intents=intents)

        @client.event
        async def on_ready():
            print(f'{client.user} is now running!')

            channel = client.get_channel(
                get_config("DISCORD_CHANNEL_ID"))
            await channel.send("I'm online now!")
            await channel.send('Type ask/''Yourqueries'' The bot will answer')


        @client.event
        async def on_message(self,message):
            # Make sure bot doesn't get stuck in an infinite loop
            if message.author == client.user:
                return

            # Get data about the user
            username = str(message.author)
            user_message = str(message.content)
            channel = str(message.channel)

            # Debug printing
            print(f"{username} said: '{user_message}' ({channel})")

            # If the user message contains a '?' in front of the text, it becomes a private message
            if user_message[0] == '?':
                user_message = user_message[1:]  # [1:] Removes the '?'
                await send_message(message, user_message, is_private=True)
            else:
                await send_message(message, user_message, is_private=False)

        client.run(TOKEN)