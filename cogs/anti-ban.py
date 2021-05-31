import discord
from discord.ext import commands
import database as db
import config


class AntiBan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        member = None
        async for log in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
            print('{0.user} did {0.action} to {0.target}'.format(log))
            member = log.user
        limit = db.select_action(member.id, "ban") + 1
        db.insert_action(member.id, "ban", limit)
        if int(limit) >= config.action['ban']:
            bot = guild.get_member(self.bot.user.id)
            bot_top_role_position = bot.top_role.position
            _user = guild.get_member(member.id)
            roles = tuple(i for i in _user.roles if i.is_default() == False or i.is_bot_managed() == False if
                          i.position < bot_top_role_position if i != guild.default_role
                          if i.is_premium_subscriber() == False)
            await _user.remove_roles(*roles, reason="anti ban ride")


def setup(bot):
    bot.add_cog(AntiBan(bot))



