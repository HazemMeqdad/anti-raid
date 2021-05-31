import discord
from discord.ext import commands
import database as db
import config


class AntiRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        guild = role.guild
        user = None
        async for log in guild.audit_logs(limit=1, action=discord.AuditLogAction.role_create):
            print('{0.user} did {0.action} to {0.target}'.format(log))
            user = log.user
        limit = db.select_action(user.id, "role_create") + 1
        db.insert_action(user.id, "role_create", limit)
        if int(limit) >= config.action['role']:
            bot = guild.get_member(self.bot.user.id)
            bot_top_role_position = bot.top_role.position
            _user = guild.get_member(user.id)
            roles = tuple(i for i in _user.roles if i.is_default() == False or i.is_bot_managed() == False if
                          i.position < bot_top_role_position if i != guild.default_role
                          if i.is_premium_subscriber() == False)
            await _user.remove_roles(*roles, reason="anti role create")
            await role.delete()

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        guild = role.guild
        user = None
        async for log in guild.audit_logs(limit=1, action=discord.AuditLogAction.role_delete):
            print('{0.user} did {0.action} to {0.target}'.format(log))
            user = log.user
        limit = db.select_action(user.id, "role_create") + 1
        db.insert_action(user.id, "role_create", limit)
        if int(limit) >= config.action['role']:
            bot = guild.get_member(self.bot.user.id)
            bot_top_role_position = bot.top_role.position
            _user = guild.get_member(user.id)
            roles = tuple(i for i in _user.roles if i.is_default() == False or i.is_bot_managed() == False if
                          i.position < bot_top_role_position if i != guild.default_role
                          if i.is_premium_subscriber() == False)
            await _user.remove_roles(*roles, reason="anti role delete")


def setup(bot):
    bot.add_cog(AntiRoles(bot))


