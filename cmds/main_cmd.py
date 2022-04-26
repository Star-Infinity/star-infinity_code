import discord,datetime
from discord.commands import (slash_command,Option)
from discord.ext import commands
import random,json,time
from discord.ui import Button,View,Select,Modal,InputText

class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # activity command

    class VoiceChannel:
        pass

    @slash_command(description="語音活動，僅限電腦版")
    async def discord_activity(self, ctx, channel: Option(VoiceChannel, "頻道", required=True),game: Option(str,"選擇遊戲",choices=["youtube",
            "youtube(dev)",
            "西洋棋",
            "西洋棋(dev)",
            "Betrayal.io",
            "撲克之夜",
            "Fishington.io",
            "lettertile",
            "wordsnack",
            "你猜我畫",
            "awkword",
            "spellcast",
            "checkers",
            "puttparty"],),):
        discord_games={
            "youtube": "880218394199220334",
            "youtube(dev)": "880218832743055411",
            "撲克之夜": "755827207812677713",
            "Betrayal.io":"773336526917861400",
            "Fishington.io":"814288819477020702",
            "西洋棋": "832012774040141894",
            "西洋棋(dev)": "832012586023256104",
            "lettertile": "879863686565621790",
            "wordsnack": "879863976006127627",
            "你猜我畫": "878067389634314250",
            "awkword": "879863881349087252",
            "spellcast": "852509694341283871",
            "checkers": "832013003968348200",
            "puttparty": "763133495793942528"}
        invite = await channel.create_activity_invite(int(discord_games[game]), max_age=3600, max_uses=20)
        embed = discord.Embed(title="Discord Activity", description=f"由{ctx.author.name}創建此活動", color=discord.Color.random())
        embed.add_field(name="活動名稱",value=game,inline=False)
        embed.add_field(name="活動連接",value=f"[點擊連接加入活動]({invite})",inline=False)
        await ctx.respond(embed = embed)
    
    # about command
    @slash_command(description="關於我的資訊")
    async def about(self, ctx):
        guild_number = 0
        for guild in self.bot.guilds:
            guild_number += 1
        embed = discord.Embed(title="【關於我】",description="[更新意見調查](https://forms.gle/fJt9tni2TsUT896y7)",color=discord.Color.random())
        embed.add_field(name="伺服器數量",value=f"正在為{guild_number}個伺服器服務")
        embed.add_field(name="python版本", value="3.10.2")
        embed.add_field(name="開發成員",value="Dyēus(.w..w.)")
        embed.add_field(name="Update Log - 1.0.8",value="-fix bug\n-rpg remake")
        embed.add_field(name="邀請我",value="[點我來邀請star-infinity](https://discord.com/api/oauth2/authorize?client_id=897671739457282089&permissions=0&scope=bot%20applications.commands)")
        embed.add_field(name="支援伺服器",value="[點我去支援伺服器](https://discord.gg/ukhmac4xYw)")
        await ctx.respond(embed = embed)
    
    # ticket event
    @commands.Cog.listener()
    async def on_interaction(self,interaction):
        if interaction.is_component() and interaction.message.author.id == self.bot.user.id:
            if interaction.data["custom_id"] == "delete-ticket":
                try:
                    await interaction.channel.send("ticket將會在幾秒之後關閉")
                    await interaction.channel.delete()
                except:
                    await interaction.channel.send("ticket無法關閉，可能是沒有權限哦~")
            else:
                pass


    @slash_command(name="8ball")
    async def ball(self,ctx,ques:Option(str,"問題", required=True)):
        response_list = ['在我看來是對的',
                      '這絕對是對的',
                      '我不確定這是不是對的',
                      f'我不知道這是不是對的\n但是我知道在其他伺服器加Star-Infinity是最好的方法',
                      '有可能是對的',
                      '這根本不對',
                      "我有點累了，你下次再找我回答吧",
                      'lol, 我不知道耶',
                      '我知道這個是不對的，別去做了',
                      "這肯定的是對的",
                      '千萬不要']
        embed = discord.Embed(title="神奇的水晶球🔮",color=discord.Color.random())
        embed.add_field(name="問題:",value=ques,inline=False)
        embed.add_field(name="回答:",value=random.choice(response_list),inline=False)
        await ctx.respond(embed=embed)
  
    # ticket command
    @slash_command(description="創建ticket")
    async def ticket(self,ctx):
        add_button = Button(label="create ticket",style=discord.ButtonStyle.green,custom_id="create-ticket",emoji="☄",)
        async def button_callback(interaction):
            perms = discord.Permissions()
            try:
                channel = await interaction.guild.create_text_channel(f"ticket-{random.randint(1,9999)}")
                await channel.set_permissions(interaction.guild.default_role, view_channel=False)
                await interaction.response.send_message(f"ticket create {channel.mention}", ephemeral=True)
                del_button = Button(label="delete ticket",style=discord.ButtonStyle.danger,custom_id="delete-ticket")
                v = View()
                v.add_item(del_button)
                embed = discord.Embed(title="點擊按鈕刪除此ticket",color=0x787FDD,description=f"{interaction.user.mention} 開啟了此ticket",)
                await channel.send(embed=embed, view=v)
            except:
                await interaction.response.send_message(f"無法創建ticket，可能沒有權限哦~", ephemeral=True)    
            
        embed = discord.Embed(title="創建ticket",description="點擊按鈕創建ticket",color=discord.Color.random())
        v = View()
        v.add_item(add_button)
        add_button.callback=button_callback
        await ctx.respond(embed=embed,view=v)


    #dm command
    @slash_command(description="Dm一些人.w.")
    async def dm(self,ctx,user: Option(discord.Member, "User", required=True, default=None),message: Option(str, "Message", required=True, default=None),):
        with open("./config.json",encoding='utf-8') as f:
                data = json.load(f)
        if user.id == self.bot.user.id:
            return await ctx.respond(f"你不能用Star-Infinity跟Star-Infinity講話哦", ephemeral=True)
        elif int(user.id) in data["owner"] and int(ctx.author.id) not in data["owner"]:
            
            await ctx.respond(f"您無法將此消息發送給creater", ephemeral=True)

        else:
            embed = discord.Embed(title=f"{ctx.author.name}給你發了一個訊息", description=message)
            try:
                await user.send(embed=embed)
            except:
                await ctx.respond(f"我無法發送信息給{user.name}", ephemeral=True)
            else:
                await ctx.respond("成功發送", ephemeral=True)
    
    #say command
    @slash_command(description="使用機器人來跟人講話哦.w.")
    async def say(self,ctx, message: Option(str, "message you want to say", ephemeral=True)):
        await ctx.respond("信息成功發出", ephemeral=True)
        await ctx.channel.send(message)
    
    #dice command
    @slash_command(description="擲骰子")
    async def dice(self,ctx):
        x = random.randint(1, 6)
        await ctx.respond(f"你擲到 **{x}**")
    
    @slash_command(description="用戶資訊")
    async def userinfo(self,ctx,user: Option(discord.Member, "User", default=None)):
        roles_name = []
        if user == None:
            user = ctx.author
        for role in user.roles:
            roles_name.append(role.mention)
        joined_at = user.joined_at
        created_at = user.created_at
        embed = discord.Embed(title=f"{user.name}的資訊", color=discord.Color.random())
        embed.add_field(name="用戶名稱", value=user.mention)
        embed.add_field(name="用戶ID", value=user.id)
        embed.add_field(name="在此服加入於", value=joined_at.strftime("%Y/%m/%d %H:%M %Z"))
        embed.add_field(name="創建此賬號於", value=created_at.strftime("%Y/%m/%d %H:%M %Z"))
        embed.add_field(name="身份組["+str(len(user.roles))+"個]", value="**|**".join(roles_name))
        await ctx.respond(embed=embed)
        
    @slash_command(description="Help-查看指令")
    async def help(self,ctx):
        message_embed = discord.Embed(title="Help指令",color=discord.Color.random())
        message_embed.add_field(name="功能性指令:",value="`/help` `/ping` `/dice` `/say` `/dm` `/userinfo` `/8ball`")
        message_embed.add_field(name="等級系統:",value="`/rank`")
        message_embed.add_field(name="伺服器管理:",value="`/kick` `/ban` `/timeout` `/server_info` `/ticket`")
        message_embed.add_field(name="RPG:",value="`/rpg_start` `/rpg_profile` `/rpg_wild` `rpg_shop` `rpg_heal` `/rpg_equip` `/rpg_unequip` `/rpg_inv`")
        await ctx.respond(embed=message_embed)
   

	

def setup(bot):
    bot.add_cog(Main(bot))