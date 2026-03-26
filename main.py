import discord
from discord.ext import commands
import statsapi
from datetime import date, timedelta
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

TOKEN = os.getenv('DISCORD_TOKEN')

@bot.event
async def on_ready():
    print(f"✅ HR Dinger Bot is online as {bot.user}")

@bot.command(name="hrtoday")
async def hr_today(ctx):
    today = date.today()
    games = statsapi.schedule(date=today.strftime('%m/%d/%Y'))
    
    embed = discord.Embed(
        title=f"🚀 HR Dinger Bot - Today's Slate ({today.strftime('%m/%d/%Y')}) 🔥",
        color=0xff4500
    )
    embed.description = "Opening Day HR Watch! Strong candidates for every game."

    for game in games[:12]:
        away = game.get('away_name', 'TBD')
        home = game.get('home_name', 'TBD')
        value = f"**{away} @ {home}**\n" \
                "Away: Power bats to watch\n" \
                "Home: Power bats to watch\n" \
                "Run !hrtoday again closer to first pitch when lineups drop."
        embed.add_field(name="", value=value, inline=False)

    embed.add_field(
        name="Suggested Parlays",
        value=(
            "**Conservative 2-leg:** Tyler O'Neill + Will Smith\n"
            "**3-leg Longshot:** O'Neill + Murakami + Duran\n"
            "**4-leg Super Longshot:** O'Neill + Murakami + Will Smith + Duran"
        ),
        inline=False
    )
    
    embed.set_footer(text="Type !info for help • Run !hrtoday again later!")
    await ctx.send(embed=embed)

@bot.command(name="info")
async def info(ctx):
    embed = discord.Embed(title="HR Dinger Bot Info", color=0xff4500)
    embed.description = "Simple version for now.\nRun !hrtoday to see the slate.\nMore advanced Statcast version coming soon."
    await ctx.send(embed=embed)

@bot.command(name="hrtomorrow")
async def hr_tomorrow(ctx):
    tomorrow = date.today() + timedelta(days=1)
    games = statsapi.schedule(date=tomorrow.strftime('%m/%d/%Y'))
    
    embed = discord.Embed(
        title=f"🚀 HR Dinger Bot - Tomorrow's Slate ({tomorrow.strftime('%m/%d/%Y')})",
        color=0xff4500
    )
    embed.description = "HR candidates loading... Full model coming soon!"
    
    for game in games[:10]:
        away = game.get('away_name', 'TBD')
        home = game.get('home_name', 'TBD')
        embed.add_field(name=f"{away} @ {home}", value="HR watch loading...", inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name="hrslate")
async def hr_slate(ctx):
    await hr_tomorrow(ctx)

bot.run(TOKEN)