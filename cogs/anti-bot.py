import discord
from discord.ext import commands


class AntiBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot:
            if member.public_flags.verified_bot:
                bot = member.guild.get_member(self.bot.user.id)
                bot_top_role_position = bot.top_role.position
                roles = tuple(i for i in member.roles if i.is_default() == False or i.is_bot_managed() == False if
                         i.position < bot_top_role_position if i != member.guild.default_role)
                try:
                    await member.remove_roles(*roles, reason="anti bot")
                except discord.errors.Forbidden:
                    x = None
                auto_mod_role = member.guild.get_role(848831443466846238)
                await member.add_roles(auto_mod_role, reason='verified bot')
                async for log in member.guild.audit_logs(limit=1, action=discord.AuditLogAction.bot_add):
                    print('{0.user} did {0.action} to {0.target}'.format(log))
                try:
                    bot_role = [i for i in member.roles if i.is_bot_managed()][0]
                    permissions = discord.Permissions()
                    permissions.update(
                        kick_members=False,
                        ban_members=False,
                        administrator=False,
                        manage_channels=False,
                        manage_guild=False,
                        view_audit_log=False,
                        manage_messages=False,
                        mention_everyone=False,
                        view_guild_insights=False,
                        mute_members=False,
                        deafen_members=False,
                        move_members=False,
                        manage_nicknames=False,
                        manage_roles=False,
                        manage_permissions=False,
                        manage_webhooks=False,
                        manage_emojis=False,
                        use_slash_commands=False
                    )
                    await bot_role.edit(permissions=permissions)
                except IndexError:
                    return
                return
            await member.guild.ban(member)
            user = None
            async for log in member.guild.audit_logs(limit=1, action=discord.AuditLogAction.bot_add):
                print('{0.user} did {0.action} to {0.target}'.format(log))
                user = log.user
            bot = member.guild.get_member(self.bot.user.id)
            bot_top_role_position = bot.top_role.position
            _user = member.guild.get_member(user.id)
            roles = tuple(i for i in _user.roles if i.is_default() == False or i.is_bot_managed() == False if
                          i.position < bot_top_role_position if i != member.guild.default_role)
            await _user.remove_roles(*roles, reason="anti bot")


def setup(bot):
    bot.add_cog(AntiBot(bot))

