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

# Helper function to get games for a specific date
def get_slate(target_date):
    games = statsapi.schedule(date=target_date.strftime('%m/%d/%Y'))
    embed = discord.Embed(
        title=f"🚀 HR Dinger Bot - Slate for {target_date.strftime('%m/%d/%Y')} 🔥",
        color=0xff4500
    )
    embed.description = "Basic slate for now. Full HR predictions (barrel%, park, weather, top candidates) coming soon!"
    
    for game in games[:12]:  # Show up to 12 games
        away = game.get('away_name', 'TBD')
        home = game.get('home_name', 'TBD')
        embed.add_field(
            name=f"{away} @ {home}",
            value="HR candidates loading soon...",
            inline=False
        )
    
    embed.set_footer(text="Entertainment only. Baseball is high variance!")
    return embed

@bot.command(name="hrtoday")
async def hr_today(ctx):
    today = date.today()
    embed = get_slate(today)
    await ctx.send(embed=embed)

@bot.command(name="hrtomorrow")
async def hr_tomorrow(ctx):
    tomorrow = date.today() + timedelta(days=1)
    embed = get_slate(tomorrow)
    await ctx.send(embed=embed)

# Optional: keep !hrslate as alias for tomorrow
@bot.command(name="hrslate")
async def hr_slate(ctx):
    await hr_tomorrow(ctx)

bot.run(TOKEN)
