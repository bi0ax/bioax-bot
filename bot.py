import discord
from discord.ext import commands, tasks
from lotus import *
from market import *
from faceit import *
import asyncio
bot = commands.Bot(command_prefix='!')
time_now_disc = lambda: datetime.datetime.now() + datetime.timedelta(hours=4)
channel_id = 591342601961996290 #channel you want your automated messages to be in

@bot.event
async def on_ready():
    print("Ready to go!")
    print(bot.user.name)
    eidolon_day.start()
    vallis_day.start()
    cambion_day.start()

@bot.command(aliases=["nw"])
async def nightwave(ctx):
    nw = Nightwave()
    embed = discord.Embed(title="Nightwave Challenges", timestamp=time_now_disc())
    for x,y,z,a in zip(nw.get_challenge_names(), nw.get_challenge_descs(), nw.get_challenge_standings(), nw.get_time_left()):
        embed.add_field(name=x, value=f"{y} ({z} standing) - {a}", inline=False)
    await ctx.channel.send(embed=embed)

@bot.command()
async def sortie(ctx):
    sortie = Sortie()
    total_time_left = time_left(sortie.current_sortie["expiry"][:-1])
    hours = total_time_left.seconds//3600
    minutes = (total_time_left.seconds//60)%60
    embed = discord.Embed(title=f"Sortie ({sortie.get_boss()})", description=f"{hours}h {minutes}m remaining", timestamp=time_now_disc())
    for x,y,z in zip(sortie.get_mission_types(), sortie.get_nodes(), sortie.get_modifiers()):
        embed.add_field(name=f"{x} - {y}", value=z, inline=False)
    await ctx.channel.send(embed=embed)

@bot.command(aliases=["plains", "cetus", "eidolon"])
async def earth(ctx):
    e = Eidolon()
    embed = discord.Embed(title="Plains of Eidolon", description=f"**State**: {e.get_day().capitalize()}\n**Time Left**: {e.eidolon['timeLeft']}", timestamp=time_now_disc())
    await ctx.channel.send(embed=embed)

@bot.command(aliases=["orbvallis", "fortuna"])
async def venus(ctx):
    o = OrbVallis()
    embed = discord.Embed(title="Orb Vallis", description=f"**State**: {o.get_day().capitalize()}\n**Time Left**: {o.orb_vallis['timeLeft']}", timestamp=time_now_disc())
    await ctx.channel.send(embed=embed)

@bot.command(aliases=["cambion", "necralisk", "cambiondrift"])
async def deimos(ctx):
    c = CambionDrift()
    embed = discord.Embed(title="Cambion Drift", description=f"**State**: {c.get_day().capitalize()}\n**Time Left**: {c.cambion_drift['timeLeft']}", timestamp=time_now_disc())
    await ctx.channel.send(embed=embed)

@bot.command()
async def price(ctx, *, arg):
    i = Item(arg)
    if i.valid == True:
        embed = discord.Embed(title=f"{arg.title()}", description=f"Platinum: {str(i.get_plat())}", 
        timestamp=time_now_disc(), color=discord.Color.green())
        embed.set_footer(text="Prices are pulled from warframe.market")
        await ctx.channel.send(embed=embed)
    else:
        embed = discord.Embed(title="Error", description="Item not found", timestamp=time_now_disc(), color=discord.Colour.red())
        await ctx.channel.send(embed=embed)
        

@bot.command(aliases=["faceit"])
async def stats(ctx, arg):
    username = arg.split("/")[-1]
    player = FaceitUser(username)
    if player.valid == True:
        player_lifetime = player.get_lifetime_overall()
        elo = player.player_json["games"]["csgo"]["faceit_elo"]
        level = player.player_json["games"]["csgo"]["skill_level"]
        avatar = player.player_json["avatar"]
        kdr = player_lifetime["Average K/D Ratio"]
        matches = player_lifetime["Matches"]
        winrate = player_lifetime["Win Rate %"]
        embed = discord.Embed(title=f"Stats for {username}", url=f"https://www.faceit.com/en/players/{username}/stats/csgo", color=discord.Color.from_rgb(255,85,0), timestamp=time_now_disc())
        embed.set_thumbnail(url=avatar)
        embed.add_field(name="Elo", value=f"{elo} (Level {level})", inline=False)
        embed.add_field(name="K/D", value=kdr, inline=False)
        embed.add_field(name="Matches", value=matches, inline=False)
        embed.add_field(name="Win Rate", value=f"{winrate}%", inline=False)
        embed.set_footer(text="Data is from FACEIT.com")
        await ctx.channel.send(embed=embed)
    else:
        embed = discord.Embed(title="Error", description="User not found. If you entered a username, it must be case sensitive.", timestamp=time_now_disc(), color=discord.Colour.red())
        await ctx.channel.send(embed=embed)


#The @tasks.loop are automated messages of the time of day on the open worlds
@tasks.loop(seconds=53.0)
async def eidolon_day():
    await asyncio.sleep(7)
    e = Eidolon()
    eidolon_day_read = open("world_days\\eidolon_day.txt", "r")
    if eidolon_day_read.read() == e.get_day():
        print("same earth")
    else:
        edw = open("world_days\\eidolon_day.txt", "w")
        edw.write(e.get_day())
        edw.close()
        print("updated earth")
        embed = discord.Embed(title="Plains of Eidolon", description=f"**State**: {e.get_day().capitalize()}\n**Time Left**: {e.eidolon['timeLeft']}", timestamp=time_now_disc())
        channel = bot.get_channel(591342601961996290)
        await channel.send(embed=embed)

@tasks.loop(seconds=55.0)
async def vallis_day():
    await asyncio.sleep(5)
    o = OrbVallis()
    vallis_day_read = open("world_days\\orb_vallis_day.txt", "r")
    if vallis_day_read.read() == o.get_day():
        print("same venus")
    else:
        odw = open("world_days\\orb_vallis_day.txt", "w")
        odw.write(o.get_day())
        odw.close()
        print("updated venus")
        embed = discord.Embed(title="Orb Vallis", description=f"**State**: {o.get_day().capitalize()}\n**Time Left**: {o.orb_vallis['timeLeft']}", timestamp=time_now_disc())
        channel = bot.get_channel(channel_id)
        await channel.send(embed=embed)

@tasks.loop(seconds=54.0)
async def cambion_day():
    await asyncio.sleep(6)
    c = CambionDrift()
    cambion_day_read = open("world_days\\cambion_drift_day.txt", "r")
    if cambion_day_read.read() == c.get_day():
        print("same deimos")
    else:
        cdw = open("world_days\\cambion_drift_day.txt", "w")
        cdw.write(c.get_day())
        cdw.close()
        print("updated deimos")
        embed = discord.Embed(title="Cambion Drift", description=f"**State**: {c.get_day().capitalize()}\n**Time Left**: {c.cambion_drift['timeLeft']}", timestamp=time_now_disc())
        channel = bot.get_channel(channel_id)
        await channel.send(embed=embed)


bot.run("MTAwMjU3NjUyMDA2NzQzNjYzNA.GJ4JbB.ZqyIDOnn_vVdDTO7_3_RM8bTaqySqwvDdpI5Y8")
