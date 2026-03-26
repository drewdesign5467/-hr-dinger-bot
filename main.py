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
    "❄️": "Tough Pitcher (suppresses HRs)"
}

@bot.command(name="info")
async def info(ctx):
    embed = discord.Embed(title="HR Dinger Bot Emoji Legend", color=0xff4500)
    embed.description = "Here's what each emoji means:"
    for emoji, meaning in EMOJI_LEGEND.items():
        embed.add_field(name=emoji, value=meaning, inline=False)
    embed.add_field(
        name="📌 Lineup Note",
        value="Early predictions use probable starters and known favorable matchups.\n\nRun `!hrtoday` again closer to first pitch for updated candidates when lineups drop. Confirmed lineups will show better/more accurate HR spots.",
        inline=False
    )
    await ctx.send(embed=embed)

@bot.command(name="howto")
async def howto(ctx):
    embed = discord.Embed(title="HR Dinger Bot Commands", color=0xff4500)
    embed.description = "Here's what each command does:"
    embed.add_field(name="!hrtoday", value="Shows today's slate with current HR candidates (best when run multiple times as lineups drop)", inline=False)
    embed.add_field(name="!hrtomorrow", value="Shows tomorrow's slate", inline=False)
    embed.add_field(name="!hrslate", value="Alias for !hrtomorrow", inline=False)
    embed.add_field(name="!info", value="Shows emoji legend + lineup timing note", inline=False)
    embed.add_field(name="!howto", value="Shows this help message", inline=False)
    await ctx.send(embed=embed)

def get_hr_candidates(game):
    away = game.get('away_name', 'TBD')
    home = game.get('home_name', 'TBD')
    lines = [f"**{away} @ {home}**"]

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
        lines.append("❄️ Paul Skenes pitching = tough for HRs on Mets side")
        lines.append("Pirates side: 💥 Oneil Cruz - raw power potential")
        lines.append("🔥 Bryan Reynolds - consistent contact")
        lines.append("Mets side: Limited upside vs Skenes")
    else:
        lines.append("Power bats to watch in this matchup. Run !hrtoday again closer to first pitch for updated candidates when lineups drop.")

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
    
    embed.set_footer(text="Type !info or !howto for help • Run !hrtoday again later when lineups drop!")
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
    
    embed.set_footer(text="Type !info or !howto for help")
    await ctx.send(embed=embed)

@bot.command(name="hrslate")
async def hr_slate(ctx):
    await hr_tomorrow(ctx)

bot.run(TOKEN)