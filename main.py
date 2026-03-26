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

def get_hr_candidates(game):
    away = game.get('away_name', 'TBD')
    home = game.get('home_name', 'TBD')
    
    if "White Sox" in away and "Brewers" in home:
        return "🔥 **Munetaka Murakami** (LHB vs RHP Misiorowski) - elite raw power + platoon edge. Strong longshot."
    elif "Twins" in away and "Orioles" in home:
        return "🔥 **Tyler O'Neill** (BAL) vs Joe Ryan - Opening Day history + Camden Yards boost. Solid play."
    elif "Red Sox" in away and "Reds" in home:
        return "🔥 **Great American Ball Park** = massive power boost. Look for Red Sox power bats (e.g. Devers, O'Neill types)."
    elif "Pirates" in away and "Mets" in home:
        return "Paul Skenes pitching = tough for HRs. Avoid most bats here."
    elif "Dodgers" in home:
        return "🔥 **Will Smith** (LAD) - strong vs righties + warm Dodger Stadium. Good candidate."
    else:
        return f"Power bats to watch in {home} or {away}."

@bot.command(name="hrtoday")
async def hr_today(ctx):
    today = date.today()
    games = statsapi.schedule(date=today.strftime('%m/%d/%Y'))
    
    embed = discord.Embed(
        title=f"🚀 HR Dinger Bot - Today's Slate ({today.strftime('%m/%d/%Y')}) 🔥",
        color=0xff4500
    )
    embed.description = "Opening Day HR Watch! Real matchup-based candidates with reasoning.\nFull barrel% + probability model in next update."
    
    for game in games[:12]:
        embed.add_field(
            name="",
            value=get_hr_candidates(game),
            inline=False
        )
    
    embed.add_field(
        name="Suggested Parlays",
        value=(
            "**Conservative 2-leg:** Tyler O'Neill + Will Smith\n"
            "**3-leg Longshot:** O'Neill + Murakami + Red Sox bat in GABP\n"
            "**4-leg Super Longshot:** O'Neill + Murakami + Will Smith + GABP power bat"
        ),
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
    embed.description = "HR candidates loading... Full model coming soon!"
    
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