import discord
from discord.ext import commands


class AntiExe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx):
        x = ctx.attachments
        for i in x:
            if i.content_type == "application/x-msdos-program":
                await ctx.delete()
                try:
                    await ctx.guild.ban(ctx.author, reason="anti exe file")
                except discord.errors.Forbidden:
                    return


def setup(bot):
    bot.add_cog(AntiExe(bot))

