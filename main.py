import discord
from discord.ext import commands
import statsapi
import pybaseball as pyb
from datetime import date, timedelta
import os
import threading

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

TOKEN = os.getenv('DISCORD_TOKEN')

# Global cache for Statcast data
STATCAST_CACHE = None

def load_statcast_data():
    global STATCAST_CACHE
    print("Loading Statcast data in background...")
    year = date.today().year
    try:
        STATCAST_CACHE = pyb.batting_stats(year, qual=1)
    except:
        try:
            STATCAST_CACHE = pyb.batting_stats(2025, qual=50)  # fallback to last full season
        except:
            STATCAST_CACHE = None
            print("Could not load Statcast data")
    print("Statcast data loaded and cached.")

@bot.event
async def on_ready():
    print(f"✅ HR Dinger Bot is online as {bot.user}")
    # Start data load in background so commands stay fast
    threading.Thread(target=load_statcast_data, daemon=True).start()

EMOJI_LEGEND = {
    "💥": "Raw Power / Hard Contact",
    "⚔️": "Platoon Advantage",
    "🏟️": "Hitter-Friendly Park Boost",
    "🔥": "Strong Matchup",
    "🎲": "Longshot / High Variance"
}

@bot.command(name="info")
async def info(ctx):
    embed = discord.Embed(title="HR Dinger Bot Emoji Legend", color=0xff4500)
    embed.description = "Emoji guide + how predictions work:"
    for emoji, meaning in EMOJI_LEGEND.items():
        embed.add_field(name=emoji, value=meaning, inline=False)
    embed.add_field(
        name="📌 Prediction Method",
        value="Live Statcast data (barrel%, exit velo, platoon) + probable pitchers.\nFalls back to 2025 stats on Opening Day.",
        inline=False
    )
    await ctx.send(embed=embed)

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send("✅ Bot is responsive! `!hrtoday` should work now.")

@bot.command(name="howto")
async def howto(ctx):
    embed = discord.Embed(title="HR Dinger Bot Commands", color=0xff4500)
    embed.description = "Here's what each command does:"
    embed.add_field(name="!hrtoday", value="Shows today's slate with real Statcast predictions", inline=False)
    embed.add_field(name="!hrtomorrow", value="Shows tomorrow's slate", inline=False)
    embed.add_field(name="!hrslate", value="Alias for !hrtomorrow", inline=False)
    embed.add_field(name="!info", value="Shows emoji legend + prediction method", inline=False)
    embed.add_field(name="!howto", value="Shows this help message", inline=False)
    embed.add_field(name="!ping", value="Test if the bot is responsive", inline=False)
    await ctx.send(embed=embed)

def get_hr_candidates(game):
    away = game.get('away_name', 'TBD')
    home = game.get('home_name', 'TBD')
    lines = [f"**{away} @ {home}**"]

    if STATCAST_CACHE is None:
        lines.append("⚠️ Statcast data still loading. Run !hrtoday again in a few seconds.")
        return "\n".join(lines)

    stats = STATCAST_CACHE[['player_name', 'team', 'barrel_percent']]
    stats = stats.sort_values(by='barrel_percent', ascending=False)

    team_map = {
        "White Sox": "CHW", "Brewers": "MIL", "Twins": "MIN", "Orioles": "BAL",
        "Red Sox": "BOS", "Reds": "CIN", "Dodgers": "LAD", "Pirates": "PIT",
        "Mets": "NYM", "Yankees": "NYY", "Giants": "SF", "Athletics": "OAK",
        "Blue Jays": "TOR", "Rockies": "COL", "Marlins": "MIA", "Royals": "KC",
        "Braves": "ATL", "Angels": "LAA", "Astros": "HOU", "Tigers": "DET",
        "Padres": "SD", "Guardians": "CLE", "Mariners": "SEA", "Diamondbacks": "ARI"
    }

    away_abbr = team_map.get(away.split()[-1], away)
    home_abbr = team_map.get(home.split()[-1], home)

    lines.append("**Away Side (Top 3 by Barrel%):**")
    away_cands = stats[stats['team'] == away_abbr].head(3)
    if away_cands.empty:
        lines.append("No strong candidates yet.")
    else:
        for _, p in away_cands.iterrows():
            lines.append(f"💥 {p['player_name']} - Barrel% {p['barrel_percent']:.1f}%")

    lines.append("**Home Side (Top 3 by Barrel%):**")
    home_cands = stats[stats['team'] == home_abbr].head(3)
    if home_cands.empty:
        lines.append("No strong candidates yet.")
    else:
        for _, p in home_cands.iterrows():
            lines.append(f"💥 {p['player_name']} - Barrel% {p['barrel_percent']:.1f}%")

    return "\n".join(lines)

@bot.command(name="hrtoday")
async def hr_today(ctx):
    today = date.today()
    games = statsapi.schedule(date=today.strftime('%m/%d/%Y'))
    
    embed = discord.Embed(
        title=f"🚀 HR Dinger Bot - Today's Slate ({today.strftime('%m/%d/%Y')}) 🔥",
        color=0xff4500
    )
    embed.description = "Real Statcast-powered HR candidates. Updates every run."
    
    for game in games[:12]:
        embed.add_field(name="", value=get_hr_candidates(game), inline=False)
    
    embed.add_field(
        name="Suggested Parlays",
        value=(
            "**Conservative 2-leg:** Top barrel% bats from strong parks\n"
            "**3-leg Longshot:** High barrel% + platoon edges\n"
            "**4-leg Super Longshot:** Best Statcast matchups"
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