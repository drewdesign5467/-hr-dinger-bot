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
    embed.description = "Emoji guide:"
    for emoji, meaning in EMOJI_LEGEND.items():
        embed.add_field(name=emoji, value=meaning, inline=False)
    embed.add_field(
        name="📌 Note",
        value="Early predictions use probable starters. Run !hrtoday again closer to first pitch for updated candidates when lineups drop.",
        inline=False
    )
    await ctx.send(embed=embed)

@bot.command(name="howto")
async def howto(ctx):
    embed = discord.Embed(title="HR Dinger Bot Commands", color=0xff4500)
    embed.description = "Here's what each command does:"
    embed.add_field(name="!hrtoday", value="Shows today's slate with 3 candidates from each team", inline=False)
    embed.add_field(name="!hrtomorrow", value="Shows tomorrow's slate", inline=False)
    embed.add_field(name="!hrslate", value="Alias for !hrtomorrow", inline=False)
    embed.add_field(name="!info", value="Shows emoji legend + lineup timing note", inline=False)
    embed.add_field(name="!howto", value="Shows this help message", inline=False)
    await ctx.send(embed=embed)

def get_hr_candidates(game):
    away = game.get('away_name', 'TBD')
    home = game.get('home_name', 'TBD')
    lines = [f"**{away} @ {home}**"]

    # Away team - 3 candidates
    if "White Sox" in away:
        lines.append("💥⚔️ Munetaka Murakami (LHB vs RHP) - elite raw power + platoon edge")
        lines.append("💥 Luis Robert Jr. - speed + power combo")
        lines.append("🔥 Andrew Benintendi - contact + pop")
    elif "Twins" in away:
        lines.append("💥 Young power bats to watch")
        lines.append("🔥 Contact/power combo players")
        lines.append("Check lineup for best matchups")
    elif "Red Sox" in away:
        lines.append("🏟️💥 Jarren Duran - speed + pop")
        lines.append("🏟️ Willson Contreras - power bat")
        lines.append("💥 Roman Anthony - rising threat")
    elif "Pirates" in away:
        lines.append("❄️ Paul Skenes pitching limits upside")
        lines.append("💥 Oneil Cruz - raw power potential")
        lines.append("🔥 Bryan Reynolds - consistent contact")
    else:
        lines.append("Away side: Power bats to watch. Check lineup closer to first pitch.")

    # Home team - 3 candidates
    if "Brewers" in home:
        lines.append("Brewers side: Power bats to watch in home matchup")
        lines.append("Check lineup for best candidates")
        lines.append("Park + weather will matter")
    elif "Orioles" in home:
        lines.append("🏟️ Tyler O'Neill - Camden Yards boost")
        lines.append("💥 Gunnar Henderson - young power")
        lines.append("⚔️ Adley Rutschman - switch-hitter")
    elif "Reds" in home:
        lines.append("🏟️💥 Jarren Duran types in GABP - big park boost")
        lines.append("Power bats thrive here")
        lines.append("Check confirmed lineup")
    elif "Dodgers" in home:
        lines.append("💥 Will Smith - strong vs righties")
        lines.append("💥 Shohei Ohtani - elite power")
        lines.append("🔥 Freddie Freeman - veteran consistency")
    elif "Mets" in home:
        lines.append("Mets side: Limited upside vs Skenes")
        lines.append("Power bats to watch if lineup favors them")
        lines.append("