import discord
from discord.ext import commands

from helpers import EmbedHelper, make_request, ENV, DISCORD_BOT_TOKEN
from logger import log


# region Setup Bot

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)

# endregion

# region Bot Events


@bot.event
@log
async def on_ready():
    if ENV == 'development':
        return
    print(f'{bot.user.mention} is Alive!')
    channel_id = 1218672958189338814
    channel = bot.get_channel(channel_id)
    await channel.send(f"{bot.user.mention} is Alive!")


@bot.event
@log
async def on_shutdown():
    if ENV == 'development':
        return
    channel_id = 1218672958189338814
    channel = bot.get_channel(channel_id)
    await channel.send(f"{bot.user.mention} is turning off now.")

# endregion

# region Bot Commands


@bot.command(name="hello_world")
@log
async def hello_world(ctx: commands.Context):
    """Bot says hello to user"""
    # print(ctx.author.mention)
    # print(ctx.channel.id)
    await ctx.send(f"Hello {ctx.author.mention}!")


@bot.command(name="help_me_ai")
@log
async def help_me_ai(ctx):
    """Shows this message"""
    embed = discord.Embed(title="Bot Commands", description="Here are the available commands:")
    for command in bot.commands:
        embed.add_field(name=command.name, value=command.help, inline=False)
    await ctx.send(embed=embed)


@bot.command(name="run_ai")
@commands.cooldown(rate=1, per=30, type=commands.BucketType.user)
@log
async def run_ai(ctx: commands):
    """
    Gets information from an AI: `$run_ai <request>`.
    **You can only request information every 30 seconds**
    """

    request = ctx.message.content.replace("$run_ai", "").strip()
    response = make_request(request)
    await ctx.send(embed=EmbedHelper.embed_ai_response(request, response, request))
    # else:
    #     await ctx.send(embed=EmbedHelper.embed_error_message("500 (Internal Server Error)", "Command Failed to Run", request))

# endregion

if __name__ == "__main__":
    bot.run(DISCORD_BOT_TOKEN)

# in wsl run
# ollama run llama2-uncensored to get dialog OR
# ollama serve to enable requests
