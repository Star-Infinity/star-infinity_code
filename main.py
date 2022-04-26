import discord,os,json,datetime,requests,asyncio,random,time,aiohttp
from discord.ext import commands
from discord.commands import Option
from discord.ui import Button,View,Select,Modal,InputText
from datetime import datetime, timedelta, timezone

bot = discord.Bot(intents=discord.Intents().all())

async def status_task():
    while True:
        await bot.change_presence(activity=discord.Game(name="/about"))
        await asyncio.sleep(10)
        await bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.guilds)}個伺服器"))
        await asyncio.sleep(10)
@bot.event
async def on_ready():
    print('online')
    print(f"name : {bot.user.name} , id : {bot.user.id}")
    for i in bot.guilds:
        print(i.name)
    print("=============================================================")
    bot.loop.create_task(status_task())
    

            
# @bot.event
# async def on_ready():
    # while True:
    #     command = input("<Star-Infinity>> ")
    #     if command == "exit":
    #         exit()
    #     elif command == "say":
    #         channel = input("輸入頻道ID: ")
    #         content = input("輸入內容: ")
    #         await bot.get_channel(int(channel)).send(content)

@bot.event
async def on_message(message):
    if message.author.id != bot.user.id:
        if message.content == "<@897671739457282089>":
            embed = discord.Embed(title="幹嘛ping我啦www",description=f"你不會用我嗎? 使用指令`/help`查看所有指令\n想了解我的話就用`/about`哦~\n下次別再ping我了",color=discord.Color.random())
            embed.set_author(name=f"Star-Infinity",icon_url=bot.user.avatar.url)
            await message.reply(embed=embed)


            
            
@bot.slash_command()
async def ping(ctx):
    ping = round(bot.latency*1000)
    if ping>100:
        await ctx.respond(f'{ping}ms Σ(ﾟﾛﾟ;)')  
    elif ping>85:
        await ctx.respond(f'{ping}ms (；·∀·) ')
    else:
        await ctx.respond(f'{ping}ms (～￣▽￣)～')

@bot.slash_command(description="建議")
async def suggest(ctx):
    model = Modal(title="給我們留下的建議")
    model.add_item(InputText(label="建議", placeholder="輸入你的建議",style=discord.InputTextStyle.paragraph))
    async def callback(interaction):
        message = model.children[0].value
        await ctx.respond("已經收到您的建議,感謝你的支持", ephemeral=True)
        async with aiohttp.ClientSession() as session:
            await session.post(
                "https://discord.com/api/webhooks/952492467830263909/XM4nZWvapbCeGnwjLuW0CZbrLIZ_NmKjAs5iXNEerO_cyHCl2Ug0IorbydgkWMAApZ88",
                json={
                    "content": message,
                    "username": f"{ctx.author.name} 的建議",
                    "avatar_url": ctx.author.avatar.url,
                }
            )
    model.callback = callback
    await ctx.interaction.response.send_modal(model)

with open('config.json',encoding='utf-8') as f:
    config = json.load(f)

for filename in os.listdir('./cmds'):
    if filename.endswith('.py'):   
        bot.load_extension(f'cmds.{filename[:-3]}')
for filename in os.listdir('./rpg'):
    if filename.endswith('.py'):   
        bot.load_extension(f'rpg.{filename[:-3]}')

if __name__ == '__main__':
    bot.run(config["token"])