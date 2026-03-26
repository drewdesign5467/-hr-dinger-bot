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

EMOJI_LEGEND = {
    "💥": "Raw Power / Hard Contact",
    "⚔️": "Platoon Advantage",
    "🏟️": "Hitter-Friendly Park Boost",
    "🔥": "Strong Matchup / History",
    "🎲": "Longshot / High Variance",
    "❄️": "Tough Pitcher"
}

@bot.command(name="info")
async def info(ctx):
    embed = discord.Embed(title="HR Dinger Bot Emoji Legend", color=0xff4500)
    embed.description = "Emoji guide:"
    for emoji, meaning in EMOJI_LEGEND.items():
        embed.add_field(name=emoji, value=meaning, inline=False)
    await ctx.send(embed=embed)

def get_hr_candidates(game):
    away = game.get('away_name', 'TBD')
    home = game.get('home_name', 'TBD')
    lines = [f"**{away} @ {home}**"]

    # Strong highlighted matchups
    if "White Sox" in away and "Brewers" in home:
        lines.append("💥⚔️ Munetaka Murakami (LHB vs RHP) - elite raw power + platoon edge")
        lines.append("💥 Luis Robert Jr. - speed + power combo")
        lines.append("🔥 Andrew Benintendi - contact + pop")
    elif "Twins" in away and "Orioles" in home:
        lines.append("🔥🏟️ Tyler O'Neill (BAL) - Opening Day history + Camden Yards boost")
        lines.append("💥 Gunnar Henderson - young power bat vs righty")
        lines.append("⚔️ Adley Rutschman - switch-hitter with pull power")
    elif "Red Sox" in away and "Reds" in home:
        lines.append("🏟️💥 Jarren Duran - speed + pop in GABP")
        lines.append("🏟️ Willson Contreras - power in hitter-friendly park")
        lines.append("💥 Roman Anthony - rising young power threat")
    elif "Dodgers" in home:
        lines.append("💥 Will Smith - strong vs righties + warm Dodger Stadium")
        lines.append("💥 Shohei Ohtani - elite power (if in lineup)")
        lines.append("🔥 Freddie Freeman - veteran consistency")
    elif "Pirates" in away and "Mets" in home:
        lines.append("❄️ Paul Skenes pitching = tough for HRs")
        lines.append("Avoid most bats - focus on strikeouts instead")
    else:
        # Generic but useful for every other game
        lines.append("Power bats to watch in this matchup. Check park factors and weather closer to first pitch.")

    return "\n".join(lines)

@bot.command(name="hrtoday")
async def hr_today(ctx):
    today = date.today()
    games = statsapi.schedule(date=today.strftime('%m/%d/%Y'))
    
    embed = discord.Embed(
        title=f"🚀 HR Dinger Bot - Today's Slate ({today.strftime('%m/%d/%Y')}) 🔥",
        color=0xff4500
    )
    embed.description = "Opening Day HR Watch! Matchup-based candidates with emoji stats."
    
    for game in games[:12]:
        embed.add_field(name="", value=get_hr_candidates(game), inline=False)
    
    embed.add_field(
        name="Suggested Parlays",
        value=(
            "**Conservative 2-leg:** Tyler O'Neill + Will Smith\n"
            "**3-leg Longshot:** O'Neill + Murakami + Duran (GABP)\n"
            "**4-leg Super Longshot:** O'Neill + Murakami + Will Smith + Duran"
        ),
        inline=False
    )
    
    embed.set_footer(text="Type !info for emoji legend • Entertainment only — bet responsibly!")
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
    
    embed.set_footer(text="Type !info for emoji legend • Entertainment only.")
    await ctx.send(embed=embed)

@bot.command(name="hrslate")
async def hr_slate(ctx):
    await hr_tomorrow(ctx)

bot.run(TOKEN)