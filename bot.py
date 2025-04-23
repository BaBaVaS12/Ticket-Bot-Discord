import discord
from discord.ext import commands
from discord import ButtonStyle, Interaction
from discord.ui import Button, View

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# View baraye dokme "Create Ticket"
class TicketCreateView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketCreateButton())

class TicketCreateButton(Button):
    def __init__(self):
        super().__init__(label="🎫 Create Ticket", style=ButtonStyle.green)

    async def callback(self, interaction: Interaction):
        guild = interaction.guild
        category = discord.utils.get(guild.categories, name="Tickets")
        if category is None:
            category = await guild.create_category("Tickets")

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True)
        }

        channel = await guild.create_text_channel(f"ticket-{interaction.user.name}", overwrites=overwrites, category=category)
        await channel.send(
            f"{interaction.user.mention} Welcome! Please say your problem.",
            view=TicketCloseView()
        )
        await interaction.response.send_message(f"Your ticket was created: {channel.mention}", ephemeral=True)

# View baraye dokme "Close Ticket"
class TicketCloseView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketCloseButton())

class TicketCloseButton(Button):
    def __init__(self):
        super().__init__(label="❌ Close Ticket", style=ButtonStyle.red)

    async def callback(self, interaction: Interaction):
        await interaction.channel.delete()

@bot.event
async def on_ready():
    print(f"Bot login shod: {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Slash command ha sync shod: {len(synced)} ta")
    except Exception as e:
        print(e)

# Command baraye ersal payam ticket be chanel
@bot.command()
async def setticket(ctx):
    view = TicketCreateView()
    await ctx.send("Baraye sakhte ticket, ruye dokme zir bezan:", view=view)

bot.run("")