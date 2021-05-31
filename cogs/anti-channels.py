import discord
from discord.ext import commands
import database as db
import config


class AntiChannels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        guild = channel.guild
        user = None
        async for log in guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete):
            print('{0.user} did {0.action} to {0.target}'.format(log))
            user = log.user
        limit = db.select_action(user.id, "channel_delete") + 1
        db.insert_action(user.id, "channel_delete", limit)
        if int(limit) >= config.action['channel']:
            bot = guild.get_member(self.bot.user.id)
            bot_top_role_position = bot.top_role.position
            _user = guild.get_member(user.id)
            roles = tuple(i for i in _user.roles if i.is_default() == False or i.is_bot_managed() == False if
                          i.position < bot_top_role_position if i != guild.default_role
                          if i.is_premium_subscriber() == False)
            await _user.remove_roles(*roles, reason="anti channel delete")

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        guild = channel.guild
        user = None
        async for log in guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_create):
            print('{0.user} did {0.action} to {0.target}'.format(log))
            user = log.user
        limit = db.select_action(user.id, "channel_create") + 1
        db.insert_action(user.id, "channel_create", limit)
        if int(limit) >= config.action['channel']:
            bot = guild.get_member(self.bot.user.id)
            bot_top_role_position = bot.top_role.position
            _user = guild.get_member(user.id)
            roles = tuple(i for i in _user.roles if i.is_default() == False or i.is_bot_managed() == False if
                          i.position < bot_top_role_position if i != guild.default_role
                          if i.is_premium_subscriber() == False)
            await _user.remove_roles(*roles, reason="anti channel delete")


def setup(bot):
    bot.add_cog(AntiChannels(bot))
