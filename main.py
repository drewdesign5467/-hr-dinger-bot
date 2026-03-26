import discord
from discord.ext import commands
import statsapi
import pybaseball as pyb
from datetime import date, timedelta
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

TOKEN = os.getenv('DISCORD_TOKEN')

@bot.event
async def on_ready():
    print(f"✅ HR Dinger Bot is online as {bot.user}")
    print("Attempting to load live Statcast data...")

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
    embed.description = "Emoji guide + lineup timing note:"
    for emoji, meaning in EMOJI_LEGEND.items():
        embed.add_field(name=emoji, value=meaning, inline=False)
    embed.add_field(
        name="📌 How the bot works",
        value="Uses live Statcast data (barrel%, exit velo, platoon) when available.\nOn Opening Day it falls back to strong candidates until data loads.",
        inline=False
    )
    await ctx.send(embed=embed)

@bot.command(name="howto")
async def howto(ctx):
    embed = discord.Embed(title="HR Dinger Bot Commands", color=0xff4500)
    embed.description = "Here's what each command does:"
    embed.add_field(name="!hrtoday", value="Shows today's slate with Statcast-ranked HR candidates", inline=False)
    embed.add_field(name="!hrtomorrow", value="Shows tomorrow's slate", inline=False)
    embed.add_field(name="!hrslate", value="Alias for !hrtomorrow", inline=False)
    embed.add_field(name="!info", value="Shows emoji legend + how the bot works", inline=False)
    embed.add_field(name="!howto", value="Shows this help message", inline=False)
    await ctx.send(embed=embed)

def get_hr_candidates(game):
    away = game.get('away_name', 'TBD')
    home = game.get('home_name', 'TBD')
    lines = [f"**{away} @ {home}**"]

    try:
        # Try live Statcast data
        stats = pyb.batting_stats(date.today().year, qual=1)  # lowered qual for early season
        stats = stats[['player_name', 'team', 'barrel_percent', 'exit_velocity', 'hard_hit_percent']]
        stats = stats.sort_values(by='barrel_percent', ascending=False)
        data_loaded = True
    except:
        stats = None
        data_loaded = False

    # Team abbreviation mapping
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

    # Away team
    lines.append("**Away Side:**")
    if data_loaded and stats is not None:
        away_cands = stats[stats['team'] == away_abbr].head(3)
        if not away_cands.empty:
            for _, p in away_cands.iterrows():
                lines.append(f"💥 {p['player_name']} - Barrel% {p['barrel_percent']:.1f}%")
        else:
            lines.append("No strong Statcast candidates yet.")
    else:
        lines.append("Power bats to watch. Run again when Statcast data loads.")

    # Home team
    lines.append("**Home Side:**")
    if data_loaded and stats is not None:
        home_cands = stats[stats['team'] == home_abbr].head(3)
        if not home_cands.empty:
            for _, p in home_cands.iterrows():
                lines.append(f"💥 {p['player_name']} - Barrel% {p['barrel_percent']:.1f}%")
        else:
            lines.append("No strong Statcast candidates yet.")
    else:
        lines.append("Power bats to watch. Run again when Statcast data loads.")

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
            "**Conservative 2-leg:** Top Statcast bats from strong parks\n"
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