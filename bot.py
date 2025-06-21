import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
import asyncio

load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

LOCAL_UTC_OFFSET = timedelta(hours=6)  # Bangladesh UTC+6

TARGET_USERNAMES = {
    "lutfar5656",
    "srabonbaoppy",
    "mahbub0357",
    "irfan_aff",
    "ninjalock44",
    "mhsakib1102",
    "shahidujzamanshahid",
    "utsho_dey"
}

MESSAGE = """Hi [Teammate's Name],

I wanted to quickly highlight something crucial to our success—money-generating questions. Think of them as the oxygen for our business. Without them, progress slowly fades, and growth stalls.

To keep things moving in the right direction, please take a moment to fill out this form:
👉 https://forms.gle/HjAgBdQ3oLwafPPp9
"""

async def wait_until(target_hour: int, target_minute: int):
    """Wait asynchronously until the target time in local time."""
    while True:
        now = datetime.now(timezone.utc) + LOCAL_UTC_OFFSET
        if now.hour > target_hour or (now.hour == target_hour and now.minute >= target_minute):
            break
        seconds_to_wait = 30  # check every 30 seconds
        await asyncio.sleep(seconds_to_wait)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    # Wait until 17:30 local time
    print("Waiting until 17:30 to send messages...")
    await wait_until(17, 30)

    print("Sending messages now...")

    for guild in bot.guilds:
        print(f"Checking guild: {guild.name}")
        for member in guild.members:
            if not member.bot and member.name in TARGET_USERNAMES:
                try:
                    personalized_msg = MESSAGE.replace("[Teammate's Name]", member.name)
                    await member.send(personalized_msg)
                    print(f"✅ DM sent to {member.name}")
                except Exception as e:
                    print(f"❌ Failed to send DM to {member.name}: {e}")

    print("Waiting 5 minutes before shutting down...")
    await asyncio.sleep(5 * 60)

    print("Closing bot now.")
    await bot.close()

bot.run(TOKEN)
