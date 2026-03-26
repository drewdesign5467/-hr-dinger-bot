import discord
from discord.ext import commands
import statsapi
from datetime import date, timedelta
import os
import requests
from bs4 import BeautifulSoup

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
    embed.description = "Emoji guide + lineup timing note:"
    for emoji, meaning in EMOJI_LEGEND.items():
        embed.add_field(name=emoji, value=meaning, inline=False)
    embed.add_field(
        name="📌 Lineup Note",
        value="The bot tries to detect confirmed lineups from Rotowire.\n✅ means lineup confirmed for that team.\nRun !hrtoday again closer to first pitch for best accuracy.",
        inline=False
    )
    await ctx.send(embed=embed)

@bot.command(name="howto")
async def howto(ctx):
    embed = discord.Embed(title="HR Dinger Bot Commands", color=0xff4500)
    embed.description = "Here's what each command does:"
    embed.add_field(name="!hrtoday", value="Shows today's slate with current HR candidates and tries to detect confirmed lineups", inline=False)
    embed.add_field(name="!hrtomorrow", value="Shows tomorrow's slate", inline=False)
    embed.add_field(name="!hrslate", value="Alias for !hrtomorrow", inline=False)
    embed.add_field(name="!info", value="Shows emoji legend + lineup timing note", inline=False)
    embed.add_field(name="!howto", value="Shows this help message", inline=False)
    await ctx.send(embed=embed)

def scrape_rotowire_lineups():
    """Try to detect confirmed lineups from Rotowire"""
    try:
        url = "https://www.rotowire.com/baseball/daily-lineups.php"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, "html.parser")
        
        confirmed = {}
        # Look for boxes with "Confirmed Lineup"
        for box in soup.find_all("div", class_=lambda x: x and "lineup" in x.lower()):
            team_elem = box.find("div", class_=lambda x: x and "team" in x.lower())
            if team_elem and "Confirmed Lineup" in box.get_text():
                team_name = team_elem.get_text(strip=True)
                if team_name:
                    confirmed[team_name] = True
        return confirmed
    except Exception as e:
        print(f"Rotowire scrape failed: {e}")
        return {}

@bot.command(name="hrtoday")
async def hr_today(ctx):
    today = date.today()
    games = statsapi.schedule(date=today.strftime('%m/%d/%Y'))
    confirmed = scrape_rotowire_lineups()
    
    embed = discord.Embed(
        title=f"🚀 HR Dinger Bot - Today's Slate ({today.strftime('%m/%d/%Y')}) 🔥",
        color=0xff4500
    )
    embed.description = "Opening Day HR Watch! Trying to detect confirmed lineups from Rotowire."
    
    for game in games[:12]:
        away = game.get('away_name', 'TBD')
        home = game.get('home_name', 'TBD')
        
        away_check = "✅ " if any(away in k for k in confirmed) else ""
        home_check = "✅ " if any(home in k for k in confirmed) else ""
        
        lines = [f"**{away_check}{away} @ {home_check}{home}**"]
        lines.append("Power bats to watch in this matchup. Run !hrtoday again closer to first pitch for updated candidates when lineups drop.")
        
        embed.add_field(name="", value="\n".join(lines), inline=False)
    
    embed.add_field(
        name="Suggested Parlays",
        value=(
            "**Conservative 2-leg:** Tyler O'Neill + Will Smith\n"
            "**3-leg Longshot:** O'Neill + Murakami + Duran (GABP)\n"
            "**4-leg Super Longshot:** O'Neill + Murakami + Will Smith + Duran"
        ),
        inline=False
    )
    
    embed.set_footer(text="Type !info or !howto for help • ✅ = confirmed lineup detected")
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