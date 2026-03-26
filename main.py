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

# Simple rule-based HR scoring for Opening Day (realistic for now)
def get_hr_watch(game):
    away = game.get('away_name', 'TBD')
    home = game.get('home_name', 'TBD')
    
    # Highlight real favorable spots based on Opening Day 2026 matchups
    if "White Sox" in away and "Brewers" in home:
        return "🔥 **Munetaka Murakami** (LHB vs RHP Misiorowski) - elite raw power + platoon edge. Longshot sprinkle."
    elif "Twins" in away and "Orioles" in home:
        return "🔥 **Tyler O'Neill** (BAL) vs Joe Ryan - history of Opening Day HRs + Camden Yards boost."
    elif "Red Sox" in away and "Reds" in home:
        return "🔥 Great American Ball Park = massive power boost. Look for Red Sox bats."
    elif "Pirates" in away and "Mets" in home:
        return "Paul Skenes on mound = tough for HRs. Avoid most bats here."
    else:
        return "Power bats in favorable spots. Check park + weather closer to first pitch."

@bot.command(name="hrtoday")
async def hr_today(ctx):
    today = date.today()
    games = statsapi.schedule(date=today.strftime('%m/%d/%Y'))
    
    embed = discord.Embed(
        title=f"🚀 HR Dinger Bot - Today's Slate ({today.strftime('%m/%d/%Y')}) 🔥",
        color=0xff4500
    )
    embed.description = "Opening Day HR Watch! Matchup-based candidates with real highlights.\nFull barrel% + probability scoring coming in next update."
    
    for game in games[:12]:
        embed.add_field(
            name="",
            value=get_hr_watch(game),
            inline=False
        )
    
    embed.add_field(
        name="Suggested Parlays",
        value="**Conservative 2-leg:** Tyler O'Neill + Will Smith (if in good spot)\n**Longshot 3-leg:** O'Neill + Murakami + power bat in GABP",
        inline=False
    )
    
    embed.set_footer(text="Entertainment only. Home runs are high variance — bet responsibly!")
    await ctx.send(embed=embed)

@bot.command(name="hrtomorrow")
async def hr_tomorrow(ctx):
    tomorrow = date.today() + timedelta(days=1)
    games = statsapi.schedule(date=tomorrow.strftime('%m/%d/%Y'))
    
    embed = discord.Embed(
        title=f"🚀 HR Dinger Bot - Tomorrow's Slate ({tomorrow.strftime('%m/%d/%Y')})",
        color=0xff4500
    )
    embed.description = "HR candidates loading... Full model with probabilities coming soon!"
    
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