from json import JSONDecodeError
import discord
from discord.ext import commands, tasks
from pathlib import Path
from lotus import *
from market import *
from faceit import *
from socialpuller.websitesearch import *
import os
import statistics
import subprocess
import asyncio
import platform
import concurrent.futures 
import aiohttp

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='>', intents=intents)
time_now_disc = lambda: datetime.datetime.now() + datetime.timedelta(hours=4) #gives me the current time
data_folder = Path("botinfo/")
startup = True
token_path = data_folder / "token.txt"
settings_path = data_folder / "settings.txt"
token = open(token_path, "r").read() #discord bot token stored in token.txt 

@bot.event
async def on_ready():
    print("Ready to go!")
    print(bot.user)
    eidolon_day.start()
    vallis_day.start()
    cambion_day.start()
    #update_best_ayatan.start()
    #update_augment_data.start()

@bot.command()
async def debug(ctx, *, args):
    print(args, type(args))
    await ctx.channel.send(args)

@bot.command(aliases=["setup"])
async def settings(ctx, *settings):
    settings_read = open(settings_path, "r")
    settings_json = json.loads(settings_read.read())
    if not ctx.author.guild_permissions.administrator:
        await ctx.channel.send("Not admin")
        return
    if not settings:
        embed = discord.Embed(title="**Settings**", description="!settings day_message <True/False> \n !settings day_channel <channel id>", 
        timestamp=time_now_disc())
        await ctx.channel.send(embed=embed)
        return 
    option = settings[0]
    if option == "day_message":
        if len(settings) == 2:
            value = settings[1]
            with open(settings_path, "w") as day_channel_write:
                settings_json["day_message"] = value.title()
                day_channel_write.write(str(json.dumps(settings_json)))
            await ctx.channel.send("Updated!")
    elif option == "day_channel":
        if len(settings) == 2:
            channel_string = settings[1]
            new_channel_id = channel_string[2:-1]
            with open(settings_path, "w") as day_channel_write:
                settings_json["channel"] = new_channel_id
                day_channel_write.write(str(json.dumps(settings_json)))
            await ctx.channel.send("Updated Channel")

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
async def price(ctx, *, item):
    i = MarketItem(item)
    if i.valid == True:
        embed = discord.Embed(title=f"{item.title()}", description=f"**Platinum:** {str(i.plat)} \n**Volume:** {str(i.volume)}", 
        timestamp=time_now_disc(), color=discord.Color.green())
        embed.set_footer(text="Prices are pulled from warframe.market")
        await ctx.channel.send(embed=embed)
    else:
        embed = discord.Embed(title="Error", description="Item not found", timestamp=time_now_disc(), color=discord.Colour.red())
        await ctx.channel.send(embed=embed)

@price.error
async def price_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Error", description="Please input something \n!price <item>", timestamp=time_now_disc(), color=discord.Color.red())
        await ctx.channel.send(embed=embed)

@bot.command()
async def drops(ctx, *, item):
    i = ItemDrop(item)
    if not i.item_found:
        await ctx.channel.send("Item not found")
        return
    embed = discord.Embed(title=f"Drop locations related to: {item}", timestamp=time_now_disc())
    for x in i.item_drops:
        embed.add_field(name=x["item"], value=f"Place: {x['place']} \n Chance: {str(x['chance'])}% ({x['rarity']})", inline=(False if len(i.item_drops) <= 6 else True))
    await ctx.channel.send(embed=embed)

@bot.command()
async def bestayatan(ctx):
    best_ayatan_read = open(Path("botinfo/warframedata/best_ayatan.txt"), "r")
    best_ayatan = json.load(best_ayatan_read)
    ayatan_data_read = open(Path("botinfo/warframedata/ayatan_data.txt"), "r")
    ayatan_data = json.load(ayatan_data_read)
    description = ""
    for index, x in enumerate(best_ayatan):
        description += f"**{index+1}.** {x} ({ayatan_data[x]} Endo) - {int(best_ayatan[x])} Endo per Plat \n"
    embed = discord.Embed(title="Best Ayatan Treasures for Platinum", description=description, 
    timestamp=time_now_disc())
    await ctx.channel.send(embed=embed)

@bot.command()
async def bestaugments(ctx):
    best_augment_read = open(Path("botinfo/warframedata/augment_data.txt"), "r")
    best_augment = json.load(best_augment_read)
    description = ""
    for index, x in enumerate(best_augment):
        description += f"**{index+1}.** {x} - {int(best_augment[x])} Plat \n"
    embed = discord.Embed(title="Best Augment Mods for Platinum", description=description, timestamp=time_now_disc())
    await ctx.channel.send(embed=embed)

@bot.command()
async def amps(ctx):
    embed = discord.Embed(title=" ")
    embed.set_image(url="https://vignette.wikia.nocookie.net/warframe/images/c/cd/AmpConvention.jpg/revision/latest/scale-to-width-down/700?cb=20190415144538")
    await ctx.channel.send(embed=embed)

@bot.command(aliases=["faceit", "lifetime"])
async def stats(ctx, user):
    username = user.split("/")[-1]
    player = FaceitUser(username)
    if player.valid == True:
        player_lifetime = player.get_lifetime_overall()
        elo = player.player_json["games"]["csgo"]["faceit_elo"]
        level = player.player_json["games"]["csgo"]["skill_level"]
        avatar = player.player_json["avatar"]
        kdr = player_lifetime["Average K/D Ratio"]
        matches = player_lifetime["Matches"]
        winrate = player_lifetime["Win Rate %"]
        embed = discord.Embed(title=f"Lifetime Stats for {username}", url=f"https://www.faceit.com/en/players/{username}/stats/csgo", color=discord.Color.from_rgb(255,85,0), timestamp=time_now_disc())
        embed.set_thumbnail(url=avatar)
        embed.add_field(name="Elo", value=f"{elo} (Level {level})", inline=False)
        embed.add_field(name="K/D", value=kdr, inline=False)
        embed.add_field(name="Matches", value=matches, inline=False)
        embed.add_field(name="Win Rate", value=f"{winrate}%", inline=False)
        embed.set_footer(text="Data is from FACEIT.com")
        await ctx.channel.send(embed=embed)
    else:
        embed = discord.Embed(title="Error", description="User not found. If you entered a username, it must be case sensitive.", 
        timestamp=time_now_disc(), color=discord.Colour.red())
        await ctx.channel.send(embed=embed)

@stats.error
async def stats_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Error", description="Please input something \n!stats/faceit/lifetime <nickname/url>", 
        timestamp=time_now_disc(), color=discord.Color.red())
        await ctx.channel.send(embed=embed)

@bot.command(aliases=["statspast"])
async def faceitpast(ctx, *args):
    username = args[0].split("/")[-1]
    player = FaceitUser(username)
    matches = int(args[1]) if len(args) == 2 else 20
    if player.valid == True:
        elo = player.player_json["games"]["csgo"]["faceit_elo"]
        avatar = player.player_json["avatar"]
        stats = player.get_stats(matches)
        average_kd = statistics.mean([float(x[0]) for x in stats])
        average_kd = str(round(average_kd, 2))
        average_kr = statistics.mean([float(x[1]) for x in stats])
        average_kr = str(round(average_kr, 2))
        average_kills = statistics.mean([int(x[2]) for x in stats])
        average_kills = str(int(average_kills))
        average_hs = statistics.mean([int(x[3]) for x in stats])
        average_hs = str(int(average_hs))
        embed = discord.Embed(title=f"Stats for {username} Over the Past {str(matches)} Matches", description=f"[Profile](https://www.faceit.com/en/players/{username}/stats/csgo)",
        color=discord.Color.from_rgb(255,85,0), timestamp=time_now_disc())
        embed.set_thumbnail(url=avatar)
        embed.add_field(name="Elo", value=elo, inline=False)
        embed.add_field(name="K/D", value=average_kd, inline=False)
        embed.add_field(name="K/R", value=average_kr, inline=False)
        embed.add_field(name="Average Kills", value=average_kills, inline=False)
        embed.add_field(name="Average HS%", value=average_hs, inline=False)
        embed.set_footer(text="Data is from FACEIT.com")
        await ctx.channel.send(embed=embed)
    else:
        embed = discord.Embed(title="Error", description="User not found. If you entered a username, it must be case sensitive.",
        timestamp=time_now_disc(), color=discord.Color.red())
        await ctx.channel.send(embed=embed)

@faceitpast.error
async def faceitpast_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Error", description="Please input something \n!faceitpast/statspast <nickname/url> [matches (20 is default)]", 
        timestamp=time_now_disc(), color=discord.Color.red())
        await ctx.channel.send(embed=embed)

@bot.command(aliases=["fetch", "dox", "doxx"])
async def pull(ctx, *, username):
    dox_path = Path(f"socialpuller/downloads/{username}.txt")
    if not dox_path.exists():
        search_all(username)
    print("Done searching " + username)
    await ctx.channel.send(file=discord.File(dox_path))

@pull.error
async def pull_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Error", description="Please input something \n!pull/doxx/dox/fetch <username>", 
        timestamp=time_now_disc(), color=discord.Color.red())

@bot.command(aliases=["geolocate"])
async def locate(ctx, ip):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://ip-api.com/json/{ip}") as response:
            if response.status != 200:
                return
            ip_data = await response.json()
            del ip_data["status"]
            del ip_data["query"]
            del ip_data["region"]
            del ip_data["countryCode"]
            desc = ""
            for key, value in ip_data.items():
                desc += f"**{key.title()}:** {str(value)}\n"
            embed = discord.Embed(title=f"Geolocation Data for {ip}", description=desc,
            timestamp=time_now_disc(), color=discord.Color.green())
            await ctx.channel.send(embed=embed)

@bot.command()
async def dm(ctx, *, username):
    mention_string = username.split()[0]
    user_id = int(mention_string[2:-1])
    user = await bot.fetch_user(user_id)
    if len(username.split()) > 1:
        message = username.split(" ", 1)[1]
        await user.send(message)
    else:
        await ctx.channel.send("There must be a message")

@bot.command()
async def dmall(ctx, *, message):
    if not ctx.author.guild_permissions.administrator:
        await ctx.channel.send("Not admin")
        return
    all_members = ctx.guild.members
    for member in all_members:
        user = await bot.fetch_user(member.id)
        try:
            await user.send(message)
        except:
            pass


#The @tasks.loop are automated messages of the time of day on the open worlds
@tasks.loop(seconds=60)
async def eidolon_day():
    e = Eidolon()
    settings_read = open(settings_path, "r")
    settings_json = json.loads(settings_read.read())
    channel_ready = True
    if settings_json["channel"]:   
        channel_id = int(settings_json["channel"]) #channel you want your automated messages to be in
    else:
        channel_ready = False
    eidolon_path = data_folder / "worlddays/eidolon_day.txt"
    eidolon_day_read = open(eidolon_path, "r")
    if eidolon_day_read.read() == e.get_day() and settings_json["day_message"] == "True":
        print("same earth")
    elif channel_ready and settings_json["day_message"] == "True":
        with open(eidolon_path, "w") as edw:
            edw.write(e.get_day())
        print("updated earth")
        embed = discord.Embed(title="Plains of Eidolon", description=f"**State**: {e.get_day().capitalize()}\n**Time Left**: {e.eidolon['timeLeft']}", timestamp=time_now_disc())
        channel = bot.get_channel(channel_id)
        await channel.send(embed=embed)

@tasks.loop(seconds=60.0)
async def vallis_day():
    o = OrbVallis()
    settings_read = open(settings_path, "r")
    settings_json = json.loads(settings_read.read())
    channel_ready = True
    if settings_json["channel"]:   
        channel_id = int(settings_json["channel"]) #channel you want your automated messages to be in
    else:
        channel_ready = False
    orb_vallis_path = data_folder / "worlddays/orb_vallis_day.txt"
    vallis_day_read = open(orb_vallis_path, "r")
    if vallis_day_read.read() == o.get_day() and settings_json["day_message"] == "True":
        print("same venus")
    elif channel_ready and settings_json["day_message"] == "True":
        with open(orb_vallis_path, "w") as odw:
            odw.write(o.get_day())
        print("updated venus")
        embed = discord.Embed(title="Orb Vallis", description=f"**State**: {o.get_day().capitalize()}\n**Time Left**: {o.orb_vallis['timeLeft']}", timestamp=time_now_disc())
        channel = bot.get_channel(channel_id)
        await channel.send(embed=embed)

@tasks.loop(seconds=60)
async def cambion_day():
    c = CambionDrift()
    settings_read = open(settings_path, "r")
    settings_json = json.loads(settings_read.read())
    channel_ready = True
    if settings_json["channel"]:   
        channel_id = int(settings_json["channel"]) #channel you want your automated messages to be in
    else:
        channel_ready = False
    cambion_drift_path = data_folder / "worlddays/cambion_drift_day.txt"
    cambion_day_read = open(cambion_drift_path, "r")
    if cambion_day_read.read() == c.get_day() and settings_json["day_message"] == "True":
        print("same deimos")
    elif channel_ready and settings_json["day_message"] == "True":
        with open(cambion_drift_path, "w") as cdw:
            cdw.write(c.get_day())
        print("updated deimos")
        embed = discord.Embed(title="Cambion Drift", description=f"**State**: {c.get_day().capitalize()}\n**Time Left**: {c.cambion_drift['timeLeft']}", timestamp=time_now_disc())
        channel = bot.get_channel(channel_id)
        await channel.send(embed=embed)

@tasks.loop(seconds=1800)
async def update_best_ayatan():
    items = Items()
    ayatan_prices = items.ayatan_prices
    ratios = {}
    def add_ratio(ayatan, endo):
        plat = MarketItem(ayatan).get_plat()
        ratios[ayatan] = endo/plat
    for ayatan, endo in ayatan_prices.items():
        add_ratio(ayatan, endo)
    ratios = {ayatan_name: endo for ayatan_name, endo in sorted(ratios.items(), key=lambda x: x[1], reverse=True)}
    with open(Path("botinfo/warframedata/best_ayatan.txt"), "w") as ratio_write:
        ratio_write.write(json.dumps(ratios))
        print("done writing ayatan ratios")

@tasks.loop(seconds=43200)
async def update_augment_data():
    mods = Mods()
    all_augments = mods.all_augments
    prices = {}
    for augment in all_augments:
        mi = MarketItem(augment["name"])
        plat = mi.plat
        if mi.volume >= 10:
            prices[augment["name"]] = plat
            print(augment["name"] + " added")
        else:
            print(augment["name"] + " not enough")
        await asyncio.sleep(0.34)
    prices = {mod_name: price for mod_name, price in sorted(prices.items(), key=lambda x: x[1], reverse=True)}
    with open(Path("botinfo/warframedata/augment_data.txt"), "w") as price_write:
        price_write.write(json.dumps(prices))
        print("done writing augment prices")

if __name__ == "__main__":
    bot.run(token)
    
