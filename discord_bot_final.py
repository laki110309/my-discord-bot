import discord
from discord.ext import commands
from discord import app_commands
import re
import os

TOKEN = os.getenv('DISCORD_BOT_TOKEN')

CHANNELS_CONFIG = {
    1464945429706702878: "yuniteの使い方がわかる方は、いつも通りにボットからキーを受け取ってください。わからない方は下の動画を参考にしてください。なにかわからない場合はサポートからお問い合わせください。",
    1452239800223404064: "ルール違反者がいた場合ここにその人をメンションして、証拠を同時に提出してください。 【証拠がない場合対処できないことがありますので、ご協力お願いします。】",
    1482921292725354627: "division申請になります。ここのスクリムではdivision別にスクリムを開催しております。なので、divisionが上がった場合はここに証拠と、「division〇に昇格しましたので、ロール付与をお願いします。」これ以外のメッセージは警告、またはBANになります。"
}

ROLE_ID_TO_GIVE = 1464909615316861032


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
        self.last_messages = {}

    async def setup_hook(self):
        await self.tree.sync()
        print(f"Synced slash commands for {self.user}")

bot = MyBot()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.id in CHANNELS_CONFIG:
        x_pattern = r'https?://(twitter\.com|x\.com )/\w+/status/\d+'
        if re.search(x_pattern, message.content):
            await message.add_reaction('✅')
            role = message.guild.get_role(ROLE_ID_TO_GIVE)
            if role:
                try:
                    await message.author.add_roles(role)
                except:
                    pass

        last_msg = bot.last_messages.get(message.channel.id)
        if last_msg:
            try:
                await last_msg.delete()
            except:
                pass

        content = CHANNELS_CONFIG[message.channel.id]
        try:
            bot.last_messages[message.channel.id] = await message.channel.send(content)
        except:
            pass

    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(TOKEN)
