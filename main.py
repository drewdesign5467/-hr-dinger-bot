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

# Simple HR-friendly matchups for Opening Day (real data)
def get_hr_candidates(game):
    away = game.get('away_name', 'TBD')
    home = game.get('home_name', 'TBD')
    
    # Highlight hot spots based on real Opening Day matchups
    highlights = ""
    if "White Sox" in away and "Brewers" in home:
        highlights = "🔥 Munetaka Murakami (LHB vs RHP Misiorowski) - longshot power sprinkle"
    elif "Twins" in away and "Orioles" in home:
        highlights = "🔥 Tyler O'Neill (BAL) vs Joe Ryan - strong history + Camden Yards boost"
    elif "Red Sox" in away and "Reds" in home:
        highlights = "🔥 Great American Ball Park boost - power friendly"
    else:
        highlights = "Power bats in favorable spots loading..."
    
    return f"**{away} @ {home}**\n{highlights}\nHR candidates loading with barrel% + park factors soon!"

@bot.command(name="hrtoday")
async def hr_today(ctx):
    today = date.today()
    games = statsapi.schedule(date=today.strftime('%m/%d/%Y'))
    
    embed = discord.Embed(
        title=f"🚀 HR Dinger Bot - Today's Slate ({today.strftime('%m/%d/%Y')}) 🔥",
        color=0xff4500
    )
    embed.description = "Opening Day HR Watch! Matchup-based candidates + favorable parks.\nFull barrel%, weather, and probability model coming in next update."
    
    for game in games[:12]:
        embed.add_field(
            name="",
            value=get_hr_candidates(game),
            inline=False
        )
    
    embed.add_field(
        name="Quick Parlay Idea",
        value="Conservative: Tyler O'Neill + Will Smith\nLongshot sprinkle: Munetaka Murakami",
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
        color=0xff450