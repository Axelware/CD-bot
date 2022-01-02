# Future
from __future__ import annotations

# Standard Library
from typing import Literal

# Packages
import discord
from discord.ext import commands

# My stuff
from core import config, values
from core.bot import CD
from utilities import checks, custom, enums, exceptions, objects, utils


def setup(bot: CD) -> None:
    bot.add_cog(Settings(bot))


class Settings(commands.Cog):
    """
    Change the bots settings.
    """

    def __init__(self, bot: CD) -> None:
        self.bot: CD = bot

    def cog_check(self, ctx: commands.Context[CD]) -> Literal[True]:

        if not ctx.guild:
            raise commands.NoPrivateMessage()

        return True

    @staticmethod
    async def _is_mod(
        ctx: custom.Context,
        message: str
    ) -> None:

        try:
            await commands.check_any(  # type: ignore
                checks.is_owner(),  # type: ignore
                checks.is_guild_owner(),  # type: ignore
                checks.has_any_permission(  # type: ignore
                    manage_channels=True,
                    manage_roles=True,
                    manage_guild=True,
                    kick_members=True,
                    ban_members=True,
                    administrator=True,
                ),
            ).predicate(ctx=ctx)

        except commands.CheckAnyFailure:
            raise exceptions.EmbedError(
                colour=values.RED,
                description=message
            )

    # Prefix

    @commands.group(name="prefix", invoke_without_command=True)
    async def _prefix(self, ctx: custom.Context) -> None:
        """
        Shows the bots prefix.
        """

        assert ctx.guild is not None
        guild_config = await self.bot.config.get_guild_config(ctx.guild.id)

        await ctx.send(
            embed=utils.embed(
                colour=values.MAIN,
                description=f"My prefix in this server is `{guild_config.prefix or config.PREFIX}`",
            )
        )

    @_prefix.command(name="set")
    async def _prefix_set(self, ctx: custom.Context, prefix: objects.FakePrefixConverter) -> None:
        """
        Sets the bots prefix.

        **Arguments:**
        `prefix`: The prefix to set, surround it with quotes if you want it to contain spaces.

        **Example:**
        - `cd prefix set !` - allows you to use `!help`
        - `cd prefix set "music "` - allows you to use `music help`

        **Note:**
        You can only use this command if you meet one of the following requirements:
        - You are the owner of the bot.
        - You are the owner of the server.
        - You have the `Manage Channels`, `Manage Roles`, `Manage Guild`, `Kick Members`, `Ban Members`, or `Administrator` permission.
        """

        await self._is_mod(ctx, "You don't have permission to change this servers prefix.")

        assert ctx.guild is not None
        guild_config = await self.bot.config.get_guild_config(ctx.guild.id)

        await guild_config.set_prefix(prefix.prefix)

        await ctx.send(
            embed=utils.embed(
                colour=values.GREEN,
                description=f"Set this servers prefix to `{prefix.prefix}`",
            )
        )

    @_prefix.command(name="reset")
    async def _prefix_reset(self, ctx: custom.Context) -> None:
        """
        Resets the bots prefix.

        **Note:**
        You can only use this command if you meet one of the following requirements:
        - You are the owner of the bot.
        - You are the owner of the server.
        - You have the `Manage Channels`, `Manage Roles`, `Manage Guild`, `Kick Members`, `Ban Members`, or `Administrator` permission.
        """

        await self._is_mod(ctx, "You don't have permission to change this servers prefix.")

        assert ctx.guild is not None
        guild_config = await self.bot.config.get_guild_config(ctx.guild.id)

        if not guild_config.prefix:
            raise exceptions.EmbedError(
                colour=values.RED,
                description="This server has not set a custom prefix.",
            )

        await guild_config.set_prefix(None)

        await ctx.send(
            embed=utils.embed(
                colour=values.GREEN,
                description=f"Reset this servers prefix to `{config.PREFIX}`",
            )
        )

    # DJ role

    @commands.group(name="dj", invoke_without_command=True)
    async def _dj(self, ctx: custom.Context) -> None:
        """
        Shows this servers DJ role.
        """

        assert ctx.guild is not None
        guild_config = await self.bot.config.get_guild_config(ctx.guild.id)

        if not guild_config.dj_role_id:
            raise exceptions.EmbedError(
                colour=values.RED,
                description="This server has not set a DJ role.",
            )

        if not (role := ctx.guild.get_role(guild_config.dj_role_id)):
            await guild_config.set_dj_role_id(None)
            raise exceptions.EmbedError(
                colour=values.RED,
                description="This servers DJ role was deleted, please set a new one.",
            )

        await ctx.send(
            embed=utils.embed(
                colour=values.MAIN,
                description=f"This servers DJ role is {role.mention}.",
            )
        )

    @_dj.command(name="set")
    async def _dj_set(self, ctx: custom.Context, *, role: discord.Role) -> None:
        """
        Sets this servers DJ role.

        **Arguments:**
        `role`: The role to set as the DJ role, can be a mention, id, or name.

        **Note:**
        You can only use this command if you meet one of the following requirements:
        - You are the owner of the bot.
        - You are the owner of the server.
        - You have the `Manage Channels`, `Manage Roles`, `Manage Guild`, `Kick Members`, `Ban Members`, or `Administrator` permission.
        """

        await self._is_mod(ctx, "You don't have permission to change this servers DJ role.")

        assert ctx.guild is not None
        guild_config = await self.bot.config.get_guild_config(ctx.guild.id)

        await guild_config.set_dj_role_id(role.id)

        await ctx.send(
            embed=utils.embed(
                colour=values.GREEN,
                description=f"Set this severs DJ role to {role.mention}.",
            )
        )

    @_dj.command(name="reset")
    async def _dj_reset(self, ctx: custom.Context) -> None:
        """
        Resets this servers DJ role.

        **Note:**
        You can only use this command if you meet one of the following requirements:
        - You are the owner of the bot.
        - You are the owner of the server.
        - You have the `Manage Channels`, `Manage Roles`, `Manage Guild`, `Kick Members`, `Ban Members`, or `Administrator` permission.
        """

        await self._is_mod(ctx, "You don't have permission to change this servers DJ role.")

        assert ctx.guild is not None
        guild_config = await self.bot.config.get_guild_config(ctx.guild.id)

        if not guild_config.dj_role_id:
            raise exceptions.EmbedError(
                colour=values.RED,
                description="This server has not set a DJ role.",
            )

        await guild_config.set_dj_role_id(None)

        await ctx.send(
            embed=utils.embed(
                colour=values.GREEN,
                description="Reset this servers DJ role.",
            )
        )

    # Embed size

    # DJ role

    @commands.group(name="embed-size", aliases=["embed_size", "embedsize", "es"], invoke_without_command=True)
    async def _embed_size(self, ctx: custom.Context) -> None:
        """
        Shows this servers embed size
        """

        assert ctx.guild is not None
        guild_config = await self.bot.config.get_guild_config(ctx.guild.id)

        await ctx.send(
            embed=utils.embed(
                colour=values.MAIN,
                description=f"This servers embed size is `{guild_config.embed_size.name.title()}`.",
            )
        )

    @_embed_size.command(name="set")
    async def _embed_size_set(self, ctx: custom.Context, *, embed_size: enums.EmbedSize) -> None:
        """
        Sets this servers embed size.

        **Arguments:**
        `embed_size`: The embed size to set, can be `large`, `medium`, or `small`.

        **Note:**
        You can only use this command if you meet one of the following requirements:
        - You are the owner of the bot.
        - You are the owner of the server.
        - You have the `Manage Channels`, `Manage Roles`, `Manage Guild`, `Kick Members`, `Ban Members`, or `Administrator` permission.
        """

        await self._is_mod(ctx, "You don't have permission to change this servers embed size.")

        assert ctx.guild is not None
        guild_config = await self.bot.config.get_guild_config(ctx.guild.id)

        await guild_config.set_embed_size(embed_size)

        await ctx.send(
            embed=utils.embed(
                colour=values.GREEN,
                description=f"Set this severs embed size to `{embed_size.name.title()}`.",
            )
        )

    @_embed_size.command(name="reset")
    async def _embed_size_reset(self, ctx: custom.Context) -> None:
        """
        Resets this servers embed size.

        **Note:**
        You can only use this command if you meet one of the following requirements:
        - You are the owner of the bot.
        - You are the owner of the server.
        - You have the `Manage Channels`, `Manage Roles`, `Manage Guild`, `Kick Members`, `Ban Members`, or `Administrator` permission.
        """

        await self._is_mod(ctx, "You don't have permission to change this servers embed size.")

        assert ctx.guild is not None
        guild_config = await self.bot.config.get_guild_config(ctx.guild.id)

        await guild_config.set_embed_size(enums.EmbedSize.LARGE)

        await ctx.send(
            embed=utils.embed(
                colour=values.GREEN,
                description=f"Reset this servers embed size back to `{guild_config.embed_size.name.title()}`.",
            )
        )
