import discord
from discord import app_commands
import statsapi
from datetime import date, timedelta
import os

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

TOKEN = os.getenv('DISCORD_TOKEN')

@tree.command(name="hr-slate", description="Tomorrow's MLB HR watch")
async def hr_slate(interaction: discord.Interaction):
    await interaction.response.defer()
    tomorrow = (date.today() + timedelta(days=1)).strftime('%m/%d/%Y')
    games = statsapi.schedule(date=tomorrow)
    
    embed = discord.Embed(title=f"🚀 HR Dinger Bot - Slate for {tomorrow} 🔥", color=0xff4500)
    embed.description = "Basic slate pull for now. Full HR predictions (barrel%, park, weather) coming in next update."
    
    for game in games[:10]:  # Show up to 10 games
        away = game.get('away_name', 'TBD')
        home = game.get('home_name', 'TBD')
        embed.add_field(name=f"{away} @ {home}", value="HR candidates loading soon...", inline=False)
    
    embed.set_footer(text="Entertainment only. Baseball is random.")
    await interaction.followup.send(embed=embed)

@client.event
async def on_ready():
    await tree.sync()
    print(f"Bot online as {client.user}")

client.run(TOKEN)
