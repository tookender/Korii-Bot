import random, discord
from discord.ext import commands
from discord import ui
from ._base import EconomyBase, GuildContext
from utils import Interaction, Embed, constants
from .utils import add_money
from datetime import timedelta

jobs_data = {
    "doctor": {"pay": 500, "emoji": "🩺"},     
    "teacher": {"pay": 300, "emoji": "📚"},
    "engineer": {"pay": 400, "emoji": "🛠️"},
    "artist": {"pay": 200, "emoji": "🎨"},
    "chef": {"pay": 350, "emoji": "🍳"}
}

class JobSelection(ui.View):
    def __init__(self, bot, ctx):
        super().__init__(timeout=60)
        self.bot = bot
        self.ctx = ctx
        self.value = None

        self.add_item(JobDropdown())

    async def interaction_check(self, interaction: Interaction) -> bool:
        if interaction.user.id == self.ctx.author.id:
            return True

        message = random.choice(constants.NOT_YOUR_BUTTON)
        await interaction.response.send_message(message.replace("[user]", self.ctx.author.display_name), ephemeral=True)
        return False

    async def on_timeout(self) -> None:
        for child in self.children:
            child.disabled = True
            child.style = discord.ButtonStyle.grey
        await self.ctx.message.edit(view=self)
        self.stop()

class JobDropdown(ui.Select):
    def __init__(self):
        # Generate options from the jobs_data
        options = [
            discord.SelectOption(
                label=job.capitalize(),
                description=f"Earn ${info['pay']} per hour",
                emoji=info["emoji"],
                value=job
            )
            for job, info in jobs_data.items()
        ]

        super().__init__(
            placeholder="Choose your job...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: Interaction):
        selected_job = self.values[0]
        await interaction.client.pool.execute(
            "UPDATE economy SET job = $1, last_job_claim = $2 WHERE user_id = $3",
            selected_job, discord.utils.utcnow(), interaction.user.id
        )

        embed = Embed(
            title="Congratulations!",
            description=f"You've chosen {selected_job.capitalize()} as your job! You're now earning ${jobs_data[selected_job]['pay']} per hour.",
        )

        await interaction.response.edit_message(embed=embed, view=None)

class JobCog(EconomyBase):
    @commands.hybrid_command(description="Get a job or claim your passive income!")
    async def job(self, ctx: GuildContext):
        user_job = await self.bot.pool.fetchval("SELECT job FROM economy WHERE user_id = $1 AND guild_id = $2", ctx.author.id, ctx.guild.id)

        if not user_job:            
            await self.send_embed(ctx, text="You don't have a job yet!\nPlease choose one from the dropdown below.", view=JobSelection(self.bot, ctx))
        
        else:
            await self.claim_income(ctx, user_job)

    async def claim_income(self, ctx: GuildContext, user_job):
        last_claim = await self.bot.pool.fetchval("SELECT last_job_claim FROM economy WHERE user_id = $1 AND guild_id = $2", ctx.author.id, ctx.guild.id)

        if last_claim is None:
            last_claim = discord.utils.utcnow()

        now = discord.utils.utcnow()
        time_since_last_claim = now - last_claim
        hours_passed = time_since_last_claim.total_seconds() // 3600  # Convert seconds to hours

        if hours_passed < 1:
            next_claim_time = last_claim + timedelta(hours=1)
            
            return await self.send_embed(
                ctx, 
                text=f"You can claim your next earnings {discord.utils.format_dt(next_claim_time, 'R')}.",
            )

        hourly_pay = jobs_data[user_job]["pay"]
        total_income = int(hours_passed) * hourly_pay

        await self.bot.pool.execute("UPDATE economy SET last_job_claim = $1 WHERE user_id = $2 AND guild_id = $3", now, ctx.author.id, ctx.guild.id)
        await add_money(self.bot, ctx.author.id, ctx.guild.id, total_income)
        await self.send_embed(ctx, text=f"You've claimed ${total_income} from your job as a {user_job.capitalize()}. Keep working hard!", return_embed=False)