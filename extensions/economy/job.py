import datetime, discord
from discord.ext import commands
from discord import ui
from ._base import EconomyBase
from utils import Interaction
from .utils import add_money

# Jobs dictionary with hourly pay for each job and their respective emojis
jobs_data = {
    "doctor": {"pay": 500, "emoji": "🩺"},     
    "teacher": {"pay": 300, "emoji": "📚"},
    "engineer": {"pay": 400, "emoji": "🛠️"},
    "artist": {"pay": 200, "emoji": "🎨"},
    "chef": {"pay": 350, "emoji": "🍳"}
}

class JobSelection(ui.View):
    def __init__(self, bot, ctx):
        super().__init__(timeout=60)  # Timeout for the interaction
        self.bot = bot
        self.ctx = ctx
        self.value = None

        # Create a dropdown select menu for jobs
        self.add_item(JobDropdown())

    async def interaction_check(self, interaction: Interaction) -> bool:
        # Ensure that only the original user can interact with the dropdown
        return interaction.user == self.ctx.author

    async def on_timeout(self):
        # Handle what happens when the interaction times out
        await self.ctx.send("Job selection timed out! Please try again.", ephemeral=True)

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
            placeholder="Choose your job...",  # Placeholder for the dropdown
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: Interaction):
        selected_job = self.values[0]
        await interaction.client.pool.execute(
            "UPDATE economy SET job = $1, last_claim = $2 WHERE user_id = $3",
            selected_job, datetime.datetime.now(datetime.timezone.utc), interaction.user.id
        )
        


        await interaction.response.send_message(
            f"Congatula! You're now a {selected_job.capitalize()} earning ${jobs_data[selected_job]['pay']} per hour.",
            ephemeral=True
        )

class JobCog(EconomyBase):
    @commands.hybrid_command(description="Get a job or claim your passive income!")
    async def job(self, ctx):
        user_job = await self.bot.pool.fetchval("SELECT job FROM economy WHERE user_id = $1", ctx.user.id)

        if not user_job:            
            await self.send_embed(ctx, text="You don't have a job yet! Please choose one from the dropdown below.", view=JobSelection(self.bot, ctx))
        
        else:
            await self.claim_income(ctx, user_job)

    async def claim_income(self, ctx, user_job):
        # Fetch the last time user claimed their income
        last_claim = await self.bot.pool.fetchval("SELECT last_claim FROM economy WHERE user_id = $1", ctx.user.id)

        if last_claim is None:
            last_claim = datetime.datetime.now(datetime.timezone.utc)

        now = datetime.datetime.now(datetime.timezone.utc)
        hours_passed = (now - last_claim).total_seconds() // 3600  # Convert seconds to hours

        if hours_passed < 1:
            await self.send_embed(ctx, text=f"Your hourly earnings are available every hour. Please check back later.", return_embed=False)
            return

        hourly_pay = jobs_data[user_job]["pay"]
        total_income = int(hours_passed) * hourly_pay

        await self.bot.pool.execute("UPDATE economy SET last_claim = $1 WHERE user_id = $2", now, ctx.user.id)
        await add_money(self.bot, ctx.author.id, total_income)

        await self.send_embed(ctx, text=f"You've claimed ${total_income} from your job as a {user_job.capitalize()}. Keep working hard!", return_embed=False)
