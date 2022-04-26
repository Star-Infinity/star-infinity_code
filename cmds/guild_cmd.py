import discord,json,datetime
from discord.commands import (slash_command,Option)
from discord.ext import commands

class Guild(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
	
        
    @slash_command(description="清除信息")
    async def clear(self,ctx, num: Option(int, "aumount", required=True, default=1)):
        owner = None
        with open('./config.json') as j:
            data = json.load(j)
        try:
        	owner = data["owner"]
        except:
            pass
        if ctx.guild.me.guild_permissions.manage_messages:
            if ctx.author.guild_permissions.manage_messages or ctx.author.id in owner:
                await ctx.channel.purge(limit=num)
                await ctx.respond(f"已經清理{num}個訊息", ephemeral=True)
            else:
                await ctx.respond(f"你沒權限使用此指令")
        else:
            await ctx.respond("無法清理信息\n缺少權限:manage_messages")
    
    @slash_command(description="kick人(只限管理員使用)")
    async def kick(self,ctx,member: Option(discord.Member, "User", required=True),reason: Option(str, "為什麼你要踢他", required=True, default="No reson"),):
        with open('./config.json') as j:
            data = json.load(j)
        owner = None
        with open('./config.json') as j:
            data = json.load(j)
        try:
        	owner = data["owner"]
        except:
            pass
        if ctx.guild.me.guild_permissions.kick_members:
            if ctx.author.guild_permissions.kick_members or (ctx.author.id in owner):
                if int(member.id) not in owner:
                    if member == ctx.guild.owner:
                        await ctx.respond("沒事別kick伺服器owner")
                    else:
                        if str(member.id) == str(ctx.guild.me.id):
                            await ctx.respond("lol, 幹嘛要kick我")
                        else:
                            try:
                                await member.kick()
                                await ctx.respond(f"已踢出{member}\n原因: {reason}")
                                await member.send(f"你在{ctx.guild}被踢出\n因為:{reason}")
                            except:
                                await ctx.respond(f"無法kick此{member}\n可能有以下原因:他的身份組和管理權限大過你、有管理者權限")
                else:
                    await ctx.respond("這個人是神，你不能kick他")
                    
            else:
                await ctx.respond(f"你沒有權限使用此指令")
        else:
            await ctx.respond(f"無法kick此用戶\n缺少權限:kick_members")
    
    @slash_command(description="ban人(只限管理員使用)")
    async def ban(self,ctx,member: Option(discord.Member, "你要踢的人", required=True),reason: Option(str, "為什麼你要踢他", required=True, default="No reson")):
        with open('./config.json') as j:
            data = json.load(j)
        owner = None
        with open('./config.json') as j:
            data = json.load(j)
        try:
        	owner = data["owner"]
        except:
            pass
        if ctx.guild.me.guild_permissions.ban_members:
            if ctx.author.guild_permissions.ban_members or ctx.author.id in owner:
                if int(member.id) not in owner:
                    if member == ctx.guild.owner:
                        await ctx.respond("沒事別ban伺服器owner")
                    else:
                        if str(member.id) == str(ctx.guild.me.id):
                            await ctx.respond("lol, 幹嘛要ban我")
                        else:
                            try:
                                await member.ban()
                                await ctx.respond(f"已ban{member}\n原因: {reason}")
                                await member.send(f"你在{ctx.guild}被封禁\n因為:{reason}")
                            except:
                                await ctx.respond(f"無法ban此{member}\n可能有以下原因:他的身份組和管理權限大過你、該用戶有管理者權限")
                else:
                    await ctx.respond("這個人是神，你不能ban他")         
            else:
                await ctx.respond(f"你沒有權限使用此指令")
        else:
            await ctx.respond(f"無法ban此用戶\n缺少權限:ban_members")
    
    @slash_command(description="查看你所在伺服器的資料")
    async def server_info(self,ctx):
        online = []
        offline = []
        ilde = []
        dnd = []
        for member in ctx.guild.members:
            if str(member.status) == "online":
                online.append(member)
            elif str(member.status) == "offline":
                offline.append(member)
            elif str(member.status) == "idle":
                ilde.append(member)
            else:
                dnd.append(member)
        embed = discord.Embed(title=f"{ctx.guild.name}伺服器資料", color=0x787FDD)
        try:
            embed.set_thumbnail(url=str(ctx.guild.icon_url))
        except:
            pass
        embed.add_field(name="伺服器名稱:", value=ctx.guild.name)
        embed.add_field(name="伺服器擁有者:", value=ctx.guild.owner.name)
        embed.add_field(name="伺服器成員狀態:",value=f"在線:{len(online)}人\n請勿打擾:{len(dnd)}人\n閒置:{len(ilde)}人\n離線:{len(offline)}人",)
        embed.add_field(name="伺服器地區:", value=ctx.guild.region)
        embed.add_field(name="伺服器表情數目:", value=len(ctx.guild.emojis))
        embed.add_field(name="伺服器總人數:", value=ctx.guild.member_count)
        embed.add_field(name="伺服器ID:", value=ctx.guild.id)
        embed.add_field(name="表情:", value=len(ctx.guild.emojis))
        await ctx.respond(embed=embed)
    

    @slash_command(description="禁言~")
    async def timeout(self,ctx, member: Option(discord.Member,'你要禁言的人'), day: Option(int,'禁言的時間',default=0),hour: Option(int,'禁言的時間',default=0,required=True),minutes: Option(int,'禁言的時間',default=0,required=True)):
        with open('./config.json') as j:
            data = json.load(j)
        owner = None
        with open('./config.json') as j:
            data = json.load(j)
        try:
        	owner = data["owner"]
        except:
            pass
        
        if ctx.guild.me.guild_permissions.ban_members:
            if ctx.author.guild_permissions.ban_members or ctx.author.id in owner:
                if int(member.id) not in owner:
                    if member == ctx.guild.owner:
                            await ctx.respond("沒事別ban伺服器owner")
                    else:
                        if str(member.id) == str(ctx.guild.me.id):
                            await ctx.respond("lol, 幹嘛要ban我")
                        else:
                            count_minutes = 0
                                
                            day_min = day * 24 * 60
                            count_minutes += day_min
                            hour_min = hour * 60
                            count_minutes += hour_min
                            if minutes != 0:
                                count_minutes += minutes
                            else:
                                if day == 0 and hour == 0 and minutes == 0:
                                    await ctx.respond("你沒有輸入時間")
                                else:
                                    duration = datetime.timedelta(minutes=count_minutes)
                                    if int(member.id) not in owner:
                                        try:
                                            await member.timeout_for(duration)
                                            await ctx.respond(f"{member.name}已禁言 **{day}**天 **{hour}**小時 **{minutes}** 分鐘")
                                        except:
                                            await ctx.respond(f"無法禁言用戶，可能有以下原因：\n他的身份組和管理權限大過你、用戶有管理權限")
                else:
                    await ctx.respond("這個人是神，你不能禁言他")
            
            else:
                await ctx.respond(f"你沒有權限使用此指令")
        else:
            await ctx.respond(f"無法禁言此用戶\n缺少權限:timeout_members")
    
    
    

def setup(bot):
    bot.add_cog(Guild(bot))
