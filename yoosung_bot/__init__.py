import discord
import os
from random import randint
import dotenv
from yoosung_bot.quote_create import create_image

intents = discord.Intents.default()
intents.members = True  # Enable member intents for username access

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')

@client.event
async def on_message(message):
    if message.author == client.user:  # Ignore bot's own messages
        return

    if not message.reference:  # Check if message is a reply
        return

    if message.content.lower().startswith('!'):  # Check if reply starts with command prefix
        return

    if client.user in message.mentions:  # Check if bot is mentioned
        # Fetch the original message manually
        original_message = await message.channel.fetch_message(message.reference.message_id)
        author = original_message.author

        if author != client.user:  # Avoid self-targeting
            # Get avatar URL (different formats based on presence)
            if author.avatar:
                avatar_url = author.avatar.url
            elif author.default_avatar:
                avatar_url = author.default_avatar.url
            else:
                avatar_url = f"https://cdn.discordapp.com/embed/avatars/{randint(0,5)}.png"  # Use default image if no avatar

            # Send embed with username and avatar
            # embed = discord.Embed(title=f"{author.name}'s Info", color=discord.Color.blue())
            # embed.set_thumbnail(url=avatar_url)
            # embed.add_field(name="Username", value=author.name, inline=False)
            # embed.add_field(name="Discriminator", value=author.discriminator, inline=False)
            # embed.add_field(name="Message", value=original_message.content, inline=False)
            # print(f"Original message: {original_message.content}")
            # await message.channel.send(embed=embed)
            quote_image = create_image(avatar_url, author.name, original_message.content)
            await message.channel.send(file=discord.File(quote_image, "quote.jpg"))

dotenv.load_dotenv()
client.run(os.getenv('DISCORD_TOKEN'))
