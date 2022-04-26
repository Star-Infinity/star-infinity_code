import random,json,discord,os
from discord.commands import (slash_command,Option)
from discord.ext import commands
from discord.ui import Button,View,Select,Modal,InputText
from easy_pil import Editor, Canvas, load_image_async, Font

class Lvl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            with open("cmds/level.json", "r") as f:
                data = json.load(f)

            if str(message.guild.id) in data:
                if str(message.author.id) in data[str(message.guild.id)]:
                    xp = data[str(message.guild.id)][str(message.author.id)]['xp']
                    lvl = data[str(message.guild.id)][str(message.author.id)]['level']

                    increased_xp = xp+1
                    new_level = int(increased_xp/100)

                    data[str(message.guild.id)][str(message.author.id)]['xp']=increased_xp
    
                    with open("cmds/level.json", "w") as f:
                        json.dump(data, f)
    
                    if new_level > lvl:
                        await message.channel.send(f"{message.author.mention} 剛剛升級到 Lv.{new_level}!!!!")

                        data[str(message.guild.id)][str(message.author.id)]['level']=new_level
                        data[str(message.guild.id)][str(message.author.id)]['xp']=0

                        with open("cmds/level.json", "w") as f:
                            json.dump(data, f)
                    return

            if str(message.guild.id) in data:
                data[str(message.guild.id)][str(message.author.id)] = {}
                data[str(message.guild.id)][str(message.author.id)]['xp'] = 0
                data[str(message.guild.id)][str(message.author.id)]['level'] = 1
                      
            else:
                data[str(message.guild.id)] = {}
                data[str(message.guild.id)][str(message.author.id)] = {}
                data[str(message.guild.id)][str(message.author.id)]['xp'] = 0
                data[str(message.guild.id)][str(message.author.id)]['level'] = 1    
    
            with open("cmds/level.json", "w") as f:
                json.dump(data, f)
    
            with open("cmds/userdata.json", "r") as f:
                user_data = json.load(f)
    
            if str(message.author.id) in user_data:
                pass
            else:
                user_data[str(message.author.id)] = {}
                user_data[str(message.author.id)]['text_color'] = "#ffffff"
                user_data[str(message.author.id)]['bar_color'] = "#00aeff"
    
            with open("cmds/userdata.json", "w") as f:
                json.dump(user_data, f)

    @slash_command(name="rank",description="查看您的等級")
    async def rank(self, ctx):
        userr = ctx.author

        with open("cmds/level.json", "r") as f:
            data = json.load(f)

        with open("cmds/userdata.json", "r") as f:
            user_data = json.load(f)

        xp = data[str(ctx.guild.id)][str(userr.id)]["xp"]
        lvl = data[str(ctx.guild.id)][str(userr.id)]["level"]

        next_level_xp = (lvl+1) * 100
        xp_need = next_level_xp
        xp_have = data[str(ctx.guild.id)][str(userr.id)]["xp"]

        text_color = str(user_data[str(userr.id)]['text_color'])
        bar_color = str(user_data[str(userr.id)]['bar_color'])

        percentage = int(((xp_have * 100)/ xp_need))

        if percentage < 1:
            percentage = 0

        background = Editor(f"bg.png")
        profile = await load_image_async(str(userr.avatar.url))

        profile = Editor(profile).resize((150, 150)).circle_image()
            
        poppins = Font.poppins(size=40)
        poppins_small = Font.poppins(size=30)

        background.paste(profile.image, (30, 30))

        background.rectangle((30, 220), width=650, height=40, fill="#ffffff", radius=20)
        background.bar(
            (30, 220),
            max_width=650,
            height=40,
            percentage=percentage,
            fill=bar_color,
            radius=20,
        )
        background.text((200, 40), str(userr.name), font=poppins, color=text_color)

        background.rectangle((200, 100), width=350, height=2, fill=bar_color)
        background.text(
            (200, 130),
            f"Level : {lvl}   "
            + f"   XP : {xp} / {(lvl+1) * 100}",
            font=poppins_small,
            color=text_color,
        )

        card = discord.File(fp=background.image_bytes, filename="zCARD.png")
        await ctx.respond(file=card)
    
    

def setup(bot):
    bot.add_cog(Lvl(bot))