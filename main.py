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
    embed.description = "Opening Day HR Watch! Matchup-based candidates.\nFull barrel% + probability model coming soon!"
    
    for game in games[:12]:
        away = game.get('away_name', 'TBD')
        home = game.get('home_name', 'TBD')
        embed.add_field(
            name=f"{away} @ {home}",
            value="🔥 HR candidates loading soon...\nFavorable matchups highlighted in next update.",
            inline=False
        )
    
    embed.set_footer(text="Entertainment only. Home runs are high variance!")
    await ctx.send(embed=embed)

@bot.command(name="hrtomorrow")
async def hr_tomorrow(ctx):
    tomorrow = date.today() + timedelta(days=1)
    games = statsapi.schedule(date=tomorrow.strftime('%m/%d/%Y'))
    
    embed = discord.Embed(
        title=f"🚀 HR Dinger Bot - Tomorrow's Slate ({tomorrow.strftime('%m/%d/%Y')})",
        color=0xff4500
    )
    embed.description = "HR candidates loading soon..."
    
    for game in games[:10]:
        away = game.get('away_name', 'TBD')
        home = game.get('home_name', 'TBD')
        embed.add_field(name=f"{away} @ {home}", value="HR watch loading...", inline=False)
    
    embed.set_footer(text="Entertainment only.")
    await ctx.send(embed=embed)

@bot.command(name="hrslate")
async def hr_slate(ctx):
    await hr_tomorrow(ctx)

bot.run(TOKEN)