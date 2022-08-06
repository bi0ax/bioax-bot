import discord
from discord.ext import commands, tasks
from lotus import *
from market import *
import asyncio
bot = commands.Bot(command_prefix='!')
time_now_disc = lambda: datetime.datetime.now() + datetime.timedelta(hours=4)
days_directory = "C:\\Users\\justin\\OneDrive\\Desktop\\projects\\bioax-bot\\world_days"
channel = bot.get_channel(591342601961996290)

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
        embed.add_field(name=x, value="{} ({} standing) - {}".format(y, z, a),inline=False)
    await ctx.channel.send(embed=embed)

@bot.command()
async def sortie(ctx):
    sortie = Sortie()
    total_time_left = time_left(sortie.current_sortie["expiry"][:-1])
    embed = discord.Embed(title="Sortie ({})".format(sortie.get_boss()), description="{}h {}m remaining".format(total_time_left.seconds//3600, (total_time_left.seconds//60)%60), timestamp=time_now_disc())
    for x,y,z in zip(sortie.get_mission_types(), sortie.get_nodes(), sortie.get_modifiers()):
        embed.add_field(name="{} - {}".format(x,y), value=z, inline=False)
    await ctx.channel.send(embed=embed)

@bot.command(aliases=["plains", "cetus", "eidolon"])
async def earth(ctx):
    embed = discord.Embed(title="Plains of Eidolon", description="**State**: {}\n**Time Left**: {}".format(Eidolon().get_day().capitalize(), Eidolon().eidolon["timeLeft"]), timestamp=time_now_disc())
    await ctx.channel.send(embed=embed)

@bot.command(aliases=["orbvallis", "fortuna"])
async def venus(ctx):
    embed = discord.Embed(title="Orb Vallis", description="**State**: {}\n**Time Left**: {}".format(OrbVallis().get_day().capitalize(), OrbVallis().orb_vallis["timeLeft"]), timestamp=time_now_disc())
    await ctx.channel.send(embed=embed)

@bot.command(aliases=["cambion", "necralisk", "cambiondrift"])
async def deimos(ctx):
    embed = discord.Embed(title="Cambion Drift", description="**State**: {}\n**Time Left**: {}".format(CambionDrift().get_day().capitalize(), CambionDrift().cambion_drift["timeLeft"]), timestamp=time_now_disc())
    await ctx.channel.send(embed=embed)

@bot.command()
async def price(ctx, *, arg):
    i = Item(arg)
    if i.get_plat() == "Error":
        embed = discord.Embed(title="Error", description="Item not found", timestamp=time_now_disc(), color=discord.Colour.red())
        await ctx.channel.send(embed=embed)
    else:
        embed = discord.Embed(title="{}".format(arg.title()), description="Platinum: {}".format(str(i.get_plat())), 
        timestamp=time_now_disc(), color=discord.Color.green())
        embed.set_footer(text="Prices are pulled from warframe.market")
        await ctx.channel.send(embed=embed)


@tasks.loop(seconds=53.0)
async def eidolon_day():
    await asyncio.sleep(7)
    eidolon_day_read = open("{}\\eidolon_day.txt".format(days_directory), "r")
    if eidolon_day_read.read() == Eidolon().get_day():
        print("same earth")
    else:
        edw = open("{}\\eidolon_day.txt".format(days_directory), "w")
        edw.write(Eidolon().get_day())
        edw.close()
        print("updated earth")
        embed = discord.Embed(title="Plains of Eidolon", description="**State**: {}\n**Time Left**: {}".format(Eidolon().get_day().capitalize(), Eidolon().eidolon["timeLeft"]), timestamp=time_now_disc())
        channel = bot.get_channel(591342601961996290)
        await channel.send(embed=embed)

@tasks.loop(seconds=55.0)
async def vallis_day():
    await asyncio.sleep(5)
    vallis_day_read = open("{}\\orb_vallis_day.txt".format(days_directory), "r")
    if vallis_day_read.read() == OrbVallis().get_day():
        print("same venus")
    else:
        odw = open("{}\\orb_vallis_day.txt".format(days_directory), "w")
        odw.write(OrbVallis().get_day())
        odw.close()
        print("updated venus")
        embed = discord.Embed(title="Orb Vallis", description="**State**: {}\n**Time Left**: {}".format(OrbVallis().get_day().capitalize(), OrbVallis().orb_vallis["timeLeft"]), timestamp=time_now_disc())
        channel = bot.get_channel(591342601961996290)
        await channel.send(embed=embed)

@tasks.loop(seconds=54.0)
async def cambion_day():
    await asyncio.sleep(6)
    cambion_day_read = open("{}\\cambion_drift_day.txt".format(days_directory), "r")
    if cambion_day_read.read() == CambionDrift().get_day():
        print("same deimos")
    else:
        cdw = open("{}\\cambion_drift_day.txt".format(days_directory), "w")
        cdw.write(CambionDrift().get_day())
        cdw.close()
        print("updated deimos")
        embed = discord.Embed(title="Cambion Drift", description="**State**: {}\n**Time Left**: {}".format(CambionDrift().get_day().capitalize(), CambionDrift().cambion_drift["timeLeft"]), timestamp=time_now_disc())
        channel = bot.get_channel(591342601961996290)
        await channel.send(embed=embed)


bot.run("MTAwMjU3NjUyMDA2NzQzNjYzNA.GJ4JbB.ZqyIDOnn_vVdDTO7_3_RM8bTaqySqwvDdpI5Y8")
