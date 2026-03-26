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
    embed.description = "Emoji guide + important note:"
    for emoji, meaning in EMOJI_LEGEND.items():
        embed.add_field(name=emoji, value=meaning, inline=False)
    embed.add_field(
        name="📌 Lineup Note",
        value="Early predictions use probable starters. Run !hrtoday again closer to first pitch for updated candidates when lineups drop.",
        inline=False
    )
    await ctx.send(embed=embed)

@bot.command(name="howto")
async def howto(ctx):
    embed = discord.Embed(title="HR Dinger Bot Commands", color=0xff4500)
    embed.description = "Here's what each command does:"
    embed.add_field(name="!hrtoday", value="Shows today's slate with current HR candidates from both teams", inline=False)
    embed.add_field(name="!hrtomorrow", value="Shows tomorrow's slate", inline=False)
    embed.add_field(name="!hrslate", value="Alias for !hrtomorrow", inline=False)
    embed.add_field(name="!info", value="Emoji legend + lineup timing info", inline=False)
    embed.add_field(name="!howto", value="This help message", inline=False)
    await ctx.send(embed=embed)

def get_hr_candidates(game):
    away = game.get('away_name', 'TBD')
    home = game.get('home_name', 'TBD')
    lines = [f"**{away} @ {home}**"]

    # Away team (Pirates side when Skenes pitches, etc.)
    if "Pirates" in away:
        lines.append("❄️ Paul Skenes pitching = tough for HRs on Mets side")
        lines.append("Pirates side: Power bats to watch (limited upside today)")
        lines.append("💥 Oneil Cruz - raw power potential")
        lines.append("🔥 Bryan Reynolds - consistent contact")
    elif "White Sox" in away:
        lines.append("💥⚔️ Munetaka Murakami (LHB vs RHP) - elite raw power + platoon edge")
        lines.append("💥 Luis Robert Jr. - speed + power combo")
        lines.append("🔥 Andrew Benintendi - contact + pop")
    elif "Twins" in away:
        lines.append("🔥 Tyler O'Neill types - power in favorable spots")
        lines.append("💥 Young power bats to watch")
        lines.append("Check lineup for best matchups")
    elif "Red Sox" in away:
        lines.append("🏟️💥 Jarren Duran - speed + pop")
        lines.append("🏟️ Willson Contreras - power bat")
        lines.append("💥 Roman Anthony - rising threat")
    else:
        lines.append("Away side power bats to watch. Check lineup closer to first pitch.")

    # Home team
    if "Brewers" in home:
        lines.append("Brewers side: Power bats to watch in favorable home matchup")
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
        lines.append("🔥 Freddie Freeman - consistency")
    elif "Mets" in home:
        lines.append("Mets side: Limited upside vs Skenes")
        lines.append("Power bats to watch if lineup favors them")
        lines.append("Focus on Skenes strikeout upside")
    else:
        lines.append("Home side power bats to watch. Check park + weather closer to first pitch.")

    return "\n".join(lines)

@bot.command(name="hrtoday")
async def hr_today(ctx):
    today = date.today()
    games = statsapi.schedule(date=today.strftime('%m/%d/%Y'))
    
    embed = discord.Embed(
        title=f"🚀 HR Dinger Bot - Today's Slate ({today.strftime('%m/%d/%Y')}) 🔥",
        color=0xff4500
    )
    embed.description = "Opening Day HR Watch! 3 candidates per side where possible."
    
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