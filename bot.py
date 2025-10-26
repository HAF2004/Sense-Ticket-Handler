import discord
from discord.ext import commands
from discord.ui import Button, View
import aiohttp
import asyncio
import re
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# ============================================
# BOT CONFIGURATION
# ============================================
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


# ============================================
# CONFIGURATION
# ============================================
ROBLOX_GROUP_ID = 35908807  # SENSE of our heart
REQUIRED_ROLE_NAME = "💚・Our Lovely Sense Member"
DISCORD_VERIFIED_ROLE_ID = 1431176844279021578  # Role to give after verification
ATTUNED_SOUL_ROLE_ID = 1431246790954451156  # Staff notification role
TICKET_CATEGORY_ID = 1430958759852769373
TICKET_CHANNEL_PREFIX = "ticket-"


COLOR_PRIMARY = 0x5865F2
COLOR_SUCCESS = 0x57F287
COLOR_WARNING = 0xFFC107
COLOR_DANGER = 0xED4245
COLOR_INFO = 0x9B59B6
COLOR_PINK = 0xFFC0CB


# ============================================
# ROBLOX API FUNCTIONS
# ============================================

def extract_roblox_username(display_name):
    """Extract Roblox username from Discord display name (Bloxlink format)"""
    # Try to find @username pattern
    match = re.search(r'@(\w+)', display_name)
    if match:
        return match.group(1)
    
    # Try without @ symbol
    username = re.sub(r'[^\w\s]', '', display_name).strip().split()[0]
    return username if username else None


async def get_roblox_user_by_username(username):
    """Get Roblox user data from username"""
    url = "https://users.roblox.com/v1/usernames/users"
    payload = {"usernames": [username], "excludeBannedUsers": False}
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('data'):
                        return data['data'][0]
    except Exception as e:
        print(f"Error getting Roblox user: {e}")
    return None


async def check_group_membership_and_role(user_id, group_id, required_role):
    """Check if user is in group with specific role"""
    url = f"https://groups.roblox.com/v2/users/{user_id}/groups/roles"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    for group in data.get('data', []):
                        if group['group']['id'] == group_id:
                            role_name = group['role']['name']
                            if role_name == required_role:
                                return True, role_name
                            else:
                                return False, f"Wrong role: {role_name}"
                    return False, "Not in group"
    except Exception as e:
        print(f"Error checking group: {e}")
    
    return False, "API Error"


# ============================================
# UTILITY FUNCTION
# ============================================

def get_main_menu_embed_and_view():
    """Create main menu embed and view"""
    embed = discord.Embed(
        title="✦ SENSE Support Center ✦",
        description=(
            "**Welcome to SENSE Support!** 💫\n\n"
            "Thank you for reaching out. Please select one of the options below:"
        ),
        color=COLOR_PRIMARY
    )
    
    embed.add_field(
        name="",
        value=(
            "```text\n"
            "📝 Register Member\n"
            "Join the SENSE community and get registration steps.\n"
            "```\n"
            "```text\n"
            "❓ Question\n"
            "Browse FAQs and get instant answers to common questions.\n"
            "```\n"
            "```text\n"
            "✨ Request Role\n"
            "Verify your membership and get the Attuned Soul role.\n"
            "```\n"
            "```text\n"
            "💬 Live Chat\n"
            "Connect with a staff member for personalized help.\n"
            "```"
        ),
        inline=False
    )
    
    embed.add_field(
        name="",
        value="**Click the button below that matches your need:** ⬇️",
        inline=False
    )
    
    embed.set_footer(text="SENSE Community • Support Team Available 24/7")
    embed.timestamp = discord.utils.utcnow()
    
    return embed, MainMenuView()


# ============================================
# EVENT: DETECT NEW TICKET CHANNEL
# ============================================

@bot.event
async def on_guild_channel_create(channel):
    """Auto-greet when ticket is created"""
    if isinstance(channel, discord.TextChannel):
        if channel.category_id == TICKET_CATEGORY_ID and TICKET_CHANNEL_PREFIX in channel.name.lower():
            await asyncio.sleep(2)
            embed, view = get_main_menu_embed_and_view()
            await channel.send(embed=embed, view=view)


# ============================================
# MAIN MENU VIEW
# ============================================

class MainMenuView(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(emoji="📝", style=discord.ButtonStyle.primary, row=0)
    async def register_button(self, interaction: discord.Interaction, button: Button):
        """Registration Guide Button"""
        embed = discord.Embed(
            title="📝 Member Registration Guide",
            description="**𝜗𝜚⋆₊˚ HOW TO JOIN SENSE CLAN ⋆₊˚𝜗𝜚**\n",
            color=COLOR_PINK
        )
        
        embed.add_field(
            name="",
            value=(
                "```text\n"
                "📌 Step 1: Join Our Roblox Community\n"
                "• Change your display name to: username+sense\n"
                "• Example: dipsysense\n"
                "```"
            ),
            inline=False
        )
        
        embed.add_field(
            name="",
            value="🔗 [Click to Join Community](https://www.roblox.com/communities/35908807/SENSE-of-our-heart#!/about)",
            inline=False
        )
        
        embed.add_field(
            name="",
            value=(
                "```text\n"
                "📸 Step 2: Submit Proof\n"
                "• Screenshot of Roblox profile with new display name\n"
                "• Screenshot of community join request\n"
                "• Send both screenshots in this ticket\n"
                "```"
            ),
            inline=False
        )
        
        embed.add_field(
            name="",
            value=(
                "```text\n"
                "✨ Step 3: Follow Our TikTok\n"
                "• Follow SENSE on TikTok\n"
                "• Send screenshot proof of following\n"
                "```"
            ),
            inline=False
        )
        
        embed.add_field(
            name="",
            value="🔗 [Follow on TikTok](https://www.tiktok.com/@makeseense?_t=ZS-8vqQi2vaX9c&_r=1)",
            inline=False
        )
        
        embed.set_footer(text="Registration: Weekends only (Sat-Sun)")
        embed.timestamp = discord.utils.utcnow()
        
        await interaction.response.edit_message(embed=embed, view=BackToMainView())
    
    @discord.ui.button(emoji="❓", style=discord.ButtonStyle.primary, row=0)
    async def question_button(self, interaction: discord.Interaction, button: Button):
        """FAQ Menu Button"""
        embed = discord.Embed(
            title="❓ Frequently Asked Questions",
            description="Select a question below to get help! 💡\n",
            color=COLOR_PRIMARY
        )
        
        embed.add_field(
            name="",
            value=(
                "```text\n"
                "1️⃣ How do I join SENSE?\n"
                "Registration schedule and how to become a member\n"
                "```\n"
                "```text\n"
                "2️⃣ Server Rules\n"
                "Community guidelines and policies you must follow\n"
                "```\n"
                "```text\n"
                "3️⃣ Game Tutorial\n"
                "Get help from staff for game tutorials and guidance\n"
                "```"
            ),
            inline=False
        )
        
        embed.set_footer(text="SENSE Community • Support Available 24/7")
        embed.timestamp = discord.utils.utcnow()
        
        await interaction.response.edit_message(embed=embed, view=QuestionView())
    
    @discord.ui.button(emoji="✨", style=discord.ButtonStyle.primary, row=0)
    async def request_role_button(self, interaction: discord.Interaction, button: Button):
        """Request Attuned Soul Role with Auto-Verification"""
        embed = discord.Embed(
            title="✨ Request Attuned Soul Role",
            description="**Choose your verification method:**\n",
            color=COLOR_WARNING
        )
        
        embed.add_field(
            name="",
            value=(
                "```text\n"
                "🎮 Automatic Verification\n"
                "Click 'Request Attuned Soul' to verify automatically.\n"
                "Bot will check your SENSE Roblox group membership.\n"
                "```"
            ),
            inline=False
        )
        
        embed.add_field(
            name="",
            value=(
                "```text\n"
                "✅ Requirements:\n"
                "• Must be in SENSE Roblox group\n"
                "• Must have role: 💚・Our Lovely Sense Member\n"
                "• Discord name must show Roblox username (via Bloxlink)\n"
                "```"
            ),
            inline=False
        )
        
        embed.add_field(
            name="",
            value=(
                "```text\n"
                "❓ Need Help?\n"
                "Click 'Help!' if you need manual assistance from staff.\n"
                "```"
            ),
            inline=False
        )
        
        embed.set_footer(text="Choose your verification method below")
        embed.timestamp = discord.utils.utcnow()
        
        await interaction.response.edit_message(embed=embed, view=RoleRequestView())
    
    @discord.ui.button(emoji="💬", style=discord.ButtonStyle.primary, row=0)
    async def livechat_button(self, interaction: discord.Interaction, button: Button):
        """Live Chat Request Button"""
        role = interaction.guild.get_role(ATTUNED_SOUL_ROLE_ID)
        
        embed = discord.Embed(
            title="💬 Live Chat Support Requested",
            description="**Support staff has been notified!**\n",
            color=COLOR_DANGER
        )
        
        embed.add_field(
            name="Staff Notification:",
            value=f"{role.mention if role else '@Attuned Soul'}",
            inline=False
        )
        
        embed.add_field(
            name="Request Information:",
            value=(
                f"**Request from:** {interaction.user.mention}\n"
                f"**Status:** 🟢 Staff Notified\n"
                f"**Average Response:** 5-10 minutes"
            ),
            inline=False
        )
        
        embed.set_footer(text="Thank you for waiting • SENSE Support")
        embed.timestamp = discord.utils.utcnow()
        
        await interaction.response.send_message(embed=embed, ephemeral=False)


# ============================================
# BACK TO MAIN VIEW
# ============================================

class BackToMainView(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="⬅️ Back", style=discord.ButtonStyle.secondary)
    async def back(self, interaction: discord.Interaction, button: Button):
        embed, view = get_main_menu_embed_and_view()
        await interaction.response.edit_message(embed=embed, view=view)


# ============================================
# QUESTION SUBMENU VIEW
# ============================================

class QuestionView(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(emoji="1️⃣", style=discord.ButtonStyle.primary, row=0)
    async def q1_button(self, interaction: discord.Interaction, button: Button):
        """Question 1: How to Join"""
        embed = discord.Embed(
            title="📅 Registration Schedule",
            description="**When can I join SENSE?**\n",
            color=COLOR_SUCCESS
        )
        
        embed.add_field(
            name="Registration Schedule:",
            value=(
                "• **Open:** Saturdays & Sundays only\n"
                "• **Closed:** Monday through Friday"
            ),
            inline=False
        )
        
        embed.add_field(
            name="💡 Pro Tips:",
            value=(
                "• Follow our social media for notifications\n"
                "• Watch announcements in this server\n"
                "• Registration fills up quickly on weekends!"
            ),
            inline=False
        )
        
        embed.set_footer(text="Registration • Weekend Only")
        embed.timestamp = discord.utils.utcnow()
        
        await interaction.response.edit_message(embed=embed, view=BackToQuestionView())
    
    @discord.ui.button(emoji="2️⃣", style=discord.ButtonStyle.primary, row=0)
    async def q2_button(self, interaction: discord.Interaction, button: Button):
        """Question 2: Server Rules"""
        embed = discord.Embed(
            title="‿̩͙⊱༻ ♱ GUIDELINES & POLICIES ♱ ༺⊰‿̩͙",
            description="Please follow these rules to maintain a positive community:\n",
            color=COLOR_INFO
        )
        
        embed.add_field(
            name="",
            value=(
                "```text\n"
                "📜 Terms and Conditions\n"
                "Follow Discord TOS. Must be 15+ years old.\n"
                "Limited cursing allowed - please be mindful of others.\n"
                "```"
            ),
            inline=False
        )
        
        embed.add_field(
            name="",
            value=(
                "```text\n"
                "🔞 No NSFW Content\n"
                "Refrain from posting or discussing explicit content of any kind.\n"
                "```"
            ),
            inline=False
        )
        
        embed.add_field(
            name="",
            value=(
                "```text\n"
                "🚫 No Controversial Topics\n"
                "Political or religious discussions are not allowed in this community.\n"
                "```"
            ),
            inline=False
        )
        
        embed.add_field(
            name="",
            value=(
                "```text\n"
                "⚠️ No Drama\n"
                "Do not involve SENSE in your personal conflicts.\n"
                "Drama will result in immediate removal.\n"
                "```"
            ),
            inline=False
        )
        
        embed.add_field(
            name="",
            value=(
                "```text\n"
                "🤝 Respect Each Other\n"
                "Show respect to all members, staff, and content creators.\n"
                "No harassment, doxxing, racism, sexism, or bullying.\n"
                "```"
            ),
            inline=False
        )
        
        embed.set_footer(text="Breaking rules may result in warnings, kicks, or bans")
        embed.timestamp = discord.utils.utcnow()
        
        await interaction.response.edit_message(embed=embed, view=BackToQuestionView())
    
    @discord.ui.button(emoji="3️⃣", style=discord.ButtonStyle.primary, row=0)
    async def q3_button(self, interaction: discord.Interaction, button: Button):
        """Question 3: Game Tutorial"""
        role = interaction.guild.get_role(ATTUNED_SOUL_ROLE_ID)
        
        embed = discord.Embed(
            title="🎮 Game Tutorial Request",
            description="**Tutorial assistance requested!**\n",
            color=COLOR_PRIMARY
        )
        
        embed.add_field(
            name="Staff Notification:",
            value=f"{role.mention if role else '@Attuned Soul'}",
            inline=False
        )
        
        embed.add_field(
            name="Request Details:",
            value=(
                f"**Request from:** {interaction.user.mention}\n"
                f"**Type:** Game Tutorial Help\n"
                f"**Status:** 🟢 Staff Notified"
            ),
            inline=False
        )
        
        embed.set_footer(text="Staff will help you master the game!")
        embed.timestamp = discord.utils.utcnow()
        
        await interaction.response.send_message(embed=embed, ephemeral=False)
    
    @discord.ui.button(label="⬅️ Back", style=discord.ButtonStyle.secondary, row=0)
    async def back(self, interaction: discord.Interaction, button: Button):
        embed, view = get_main_menu_embed_and_view()
        await interaction.response.edit_message(embed=embed, view=view)


# ============================================
# BACK TO QUESTION VIEW
# ============================================

class BackToQuestionView(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="⬅️ Back to FAQ", style=discord.ButtonStyle.secondary)
    async def back(self, interaction: discord.Interaction, button: Button):
        embed = discord.Embed(
            title="❓ Frequently Asked Questions",
            description="Select a question below to get help! 💡\n",
            color=COLOR_PRIMARY
        )
        
        embed.add_field(
            name="",
            value=(
                "```text\n"
                "1️⃣ How do I join SENSE?\n"
                "Registration schedule and how to become a member\n"
                "```\n"
                "```text\n"
                "2️⃣ Server Rules\n"
                "Community guidelines and policies you must follow\n"
                "```\n"
                "```text\n"
                "3️⃣ Game Tutorial\n"
                "Get help from staff for game tutorials and guidance\n"
                "```"
            ),
            inline=False
        )
        
        embed.set_footer(text="SENSE Community • Support Available 24/7")
        embed.timestamp = discord.utils.utcnow()
        
        await interaction.response.edit_message(embed=embed, view=QuestionView())


# ============================================
# ROLE REQUEST VIEW (AUTO VERIFICATION)
# ============================================

class RoleRequestView(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="👑 Request Attuned Soul", style=discord.ButtonStyle.success, row=0)
    async def verify_roblox_button(self, interaction: discord.Interaction, button: Button):
        """Verify Roblox Group Membership and Give Role"""
        
        # Defer response
        await interaction.response.defer(ephemeral=True)
        
        # Extract Roblox username from Discord name
        display_name = interaction.user.display_name
        roblox_username = extract_roblox_username(display_name)
        
        if not roblox_username:
            embed = discord.Embed(
                title="❌ Cannot Find Roblox Username",
                description=(
                    "I couldn't find your Roblox username in your Discord name.\n\n"
                    "**Please make sure:**\n"
                    "• You've linked your Roblox account with Bloxlink\n"
                    "• Your Discord nickname shows your Roblox username\n"
                    "• Example: `@uppucs` or `uppucs`\n\n"
                    "💡 Use `/verify` command with Bloxlink to link your account."
                ),
                color=COLOR_DANGER
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        
        # Get Roblox user data
        user_data = await get_roblox_user_by_username(roblox_username)
        
        if not user_data:
            embed = discord.Embed(
                title="❌ Roblox Account Not Found",
                description=(
                    f"Couldn't find Roblox account: `{roblox_username}`\n\n"
                    "**Please check:**\n"
                    "• Your Discord name matches your Roblox username\n"
                    "• You've linked with Bloxlink correctly\n"
                    "• The username is spelled correctly"
                ),
                color=COLOR_DANGER
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        
        user_id = user_data['id']
        
        # Check group membership and role
        is_verified, role_info = await check_group_membership_and_role(
            user_id, 
            ROBLOX_GROUP_ID, 
            REQUIRED_ROLE_NAME
        )
        
        if is_verified:
            # SUCCESS - Give Discord role
            role = interaction.guild.get_role(DISCORD_VERIFIED_ROLE_ID)
            
            if role:
                try:
                    await interaction.user.add_roles(role)
                    
                    embed = discord.Embed(
                        title="✅ Verification Successful!",
                        description=(
                            f"**Welcome to SENSE, {user_data['displayName']}!** 💚\n\n"
                            f"You've been verified and given the Attuned Soul role!"
                        ),
                        color=COLOR_SUCCESS
                    )
                    
                    embed.add_field(
                        name="✅ Verified Information:",
                        value=(
                            f"**Roblox Username:** {user_data['name']}\n"
                            f"**Roblox Display Name:** {user_data['displayName']}\n"
                            f"**Group Role:** {REQUIRED_ROLE_NAME}\n"
                            f"**Discord Role:** {role.mention}"
                        ),
                        inline=False
                    )
                    
                    embed.set_thumbnail(url=f"https://www.roblox.com/headshot-thumbnail/image?userId={user_id}&width=150&height=150&format=png")
                    embed.set_footer(text="Verification completed successfully!")
                    embed.timestamp = discord.utils.utcnow()
                    
                    await interaction.followup.send(embed=embed, ephemeral=True)
                    
                except Exception as e:
                    embed = discord.Embed(
                        title="⚠️ Role Error",
                        description=f"Verification passed but couldn't give role: {str(e)}",
                        color=COLOR_DANGER
                    )
                    await interaction.followup.send(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(
                    title="⚠️ Configuration Error",
                    description="Attuned Soul role not found. Please contact staff.",
                    color=COLOR_DANGER
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
        
        else:
            # FAILED - Show reason
            embed = discord.Embed(
                title="❌ Verification Failed",
                description=(
                    f"**Roblox Account:** {user_data['displayName']} (@{user_data['name']})\n"
                    f"**Reason:** {role_info}\n\n"
                    "**Requirements:**\n"
                    "✅ Must join **SENSE of our heart** group\n"
                    "✅ Must have role: **💚・Our Lovely Sense Member**\n\n"
                    "🔗 [Join Group Here](https://www.roblox.com/communities/35908807/SENSE-of-our-heart#!/about)"
                ),
                color=COLOR_DANGER
            )
            
            embed.set_thumbnail(url=f"https://www.roblox.com/headshot-thumbnail/image?userId={user_id}&width=150&height=150&format=png")
            embed.set_footer(text="Join the group with correct role and try again!")
            embed.timestamp = discord.utils.utcnow()
            
            await interaction.followup.send(embed=embed, ephemeral=True)
    
    @discord.ui.button(label="❓ Help!", style=discord.ButtonStyle.secondary, row=0)
    async def manual_help_button(self, interaction: discord.Interaction, button: Button):
        """Manual Role Request for Staff Help"""
        role = interaction.guild.get_role(ATTUNED_SOUL_ROLE_ID)
        
        embed = discord.Embed(
            title="❓ Manual Role Request",
            description="**Staff assistance requested!**\n",
            color=COLOR_INFO
        )
        
        embed.add_field(
            name="",
            value=(
                f"```text\n"
                f"📋 Request Details:\n"
                f"• Requested by: {interaction.user.display_name}\n"
                f"• Type: Manual Role Verification\n"
                f"• Status: 🟡 Pending Staff Review\n"
                f"```"
            ),
            inline=False
        )
        
        embed.add_field(
            name="",
            value=f"👥 **Staff Notification:**\n{role.mention if role else '@Attuned Soul'} will assist you shortly.",
            inline=False
        )
        
        embed.set_footer(text="Thank you for your patience!")
        embed.timestamp = discord.utils.utcnow()
        
        await interaction.response.send_message(
            content=f"{role.mention if role else '@Attuned Soul'}",
            embed=embed,
            ephemeral=False
        )
    
    @discord.ui.button(label="⬅️ Back", style=discord.ButtonStyle.secondary, row=0)
    async def back(self, interaction: discord.Interaction, button: Button):
        embed, view = get_main_menu_embed_and_view()
        await interaction.response.edit_message(embed=embed, view=view)


# ============================================
# SLASH COMMANDS
# ============================================

@bot.tree.command(name="sense", description="Open SENSE Support Center (Only in ticket channels)")
async def sense_command(interaction: discord.Interaction):
    """Slash command to open SENSE Support Center"""
    
    # Check if command is used in a ticket channel
    if not (interaction.channel.category_id == TICKET_CATEGORY_ID and 
            TICKET_CHANNEL_PREFIX in interaction.channel.name.lower()):
        embed = discord.Embed(
            title="❌ Invalid Channel",
            description="This command can only be used in ticket channels!",
            color=COLOR_DANGER
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    # Send SENSE Support Center embed
    embed, view = get_main_menu_embed_and_view()
    await interaction.response.send_message(embed=embed, view=view)


# ============================================
# BOT EVENTS
# ============================================

@bot.event
async def on_ready():
    print(f'✅ SENSE Bot Online')
    print(f'🤖 Bot: {bot.user.name}')
    print(f'📋 Servers: {len(bot.guilds)}')
    print(f'🎮 Roblox Group: {ROBLOX_GROUP_ID}')
    print(f'✅ Required Role: {REQUIRED_ROLE_NAME}')
    print(f'🎫 Discord Verified Role: {DISCORD_VERIFIED_ROLE_ID}')
    
    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f'✅ Synced {len(synced)} slash command(s)')
    except Exception as e:
        print(f'❌ Failed to sync commands: {e}')


@bot.event
async def on_command_error(ctx, error):
    """Handle command errors silently"""
    # Ignore CommandNotFound errors (when someone types ! but no valid command)
    if isinstance(error, commands.CommandNotFound):
        return
    
    # Log other errors
    print(f'Error: {error}')


# ============================================
# RUN BOT
# ============================================
if __name__ == "__main__":
    # Get token from environment variables
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        raise ValueError("No token found. Make sure DISCORD_BOT_TOKEN is set in .env file")
    bot.run(token)