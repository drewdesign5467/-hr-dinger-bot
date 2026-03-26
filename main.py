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

def get_slate(target_date, is_today=False):
    games = statsapi.schedule(date=target_date.strftime('%m/%d/%Y'))
    title = f"🚀 HR Dinger Bot - {'Today' if is_today else 'Tomorrow'}'s Slate ({target_date.strftime('%m/%d/%Y')}) 🔥"
    
    embed = discord.Embed(title=title, color=0xff4500)
    embed.description = "Matchup-based HR watch. Full model with barrel%, park factors, weather, and probabilities coming very soon!"
    
    for game in games[:10]:
        away = game.get('away_name', 'TBD')
        home = game.get('home_name', 'TBD')
        embed.add_field(
            name=f"{away} @ {home}",
            value="🔥 Top HR candidates loading soon...\nFavorable parks & matchups highlighted in next update.",
            inline=False
        )
    
    embed.set_footer(text="For entertainment only. Home runs are high variance!")
    return embed

@bot.command(name="hrtoday")
async def hr_today(ctx):
    today = date.today()
    embed = get_slate(today, is_today=True)
    await ctx.send(embed=embed)

@bot.command(name="hrtomorrow")
async def hr_tomorrow(ctx):
    tomorrow = date.today() + timedelta(days=1)
    embed = get_slate(tomorrow)
    await ctx.send(embed=embed)

@bot.command(name="hrslate")
async def hr_slate(ctx):
    await hr_tomorrow(ctx)

bot.run(TOKEN)