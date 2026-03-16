import discord
from discord.ext import commands
import re
import os

TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# 監視するチャンネルIDとメッセージの設定
CHANNELS_CONFIG = {
    1464945429706702878: "yuniteの使い方がわかる方は、いつも通りにボットからキーを受け取ってください。わからない方は下の動画を参考にしてください。なにかわからない場合はサポートからお問い合わせください。",
    1452239800223404064: "ルール違反者がいた場合ここにその人をメンションして、証拠を同時に提出してください。 【証拠がない場合対処できないことがありますので、ご協力お願いします。】",
    1482921292725354627: "division申請になります。ここのスクリムではdivision別にスクリムを開催しております。なので、divisionが上がった場合はここに証拠と、「division〇に昇格しましたので、ロール付与をお願いします。」これ以外のメッセージは警告、またはBANになります。"
}

# 付与するロールID（あなたの設定に合わせて変更してください）
ROLE_ID_TO_GIVE =1464909615316861032

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
        self.last_messages = {}

    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.channel.id in CHANNELS_CONFIG:
            # 【改良版】XやTwitterのリンクをより柔軟に検知するようにしました
            if "x.com/" in message.content.lower() or "twitter.com/" in message.content.lower():
                try:
                    await message.add_reaction('✅')
                    role = message.guild.get_role(ROLE_ID_TO_GIVE)
                    if role:
                        await message.author.add_roles(role)
                        print(f"Role added to {message.author}")
                except Exception as e:
                    print(f"Error: {e}")

            # メッセージ追従機能
            last_msg = self.last_messages.get(message.channel.id)
            if last_msg:
                try:
                    await last_msg.delete()
                except:
                    pass

            content = CHANNELS_CONFIG[message.channel.id]
            try:
                self.last_messages[message.channel.id] = await message.channel.send(content)
            except:
                pass

bot = MyBot()
bot.run(TOKEN)
