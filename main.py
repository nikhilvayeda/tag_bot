import os
import random
import discord
from discord.ext import commands, tasks

# Constants
MODS_ROLE_ID = 727418087523090483
BOT_SPAM_CHANNEL = 743799693338738779
ALL_TAGS = []
PREFIX = ":"
TOKEN = os.getenv("TOKEN")

client = commands.Bot(command_prefix=PREFIX)
client.remove_command("help")


@client.event
async def on_ready():
    keepAlive.start()
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{PREFIX}help"))
    print('ready...')


@client.command()
@commands.has_any_role(MODS_ROLE_ID)
async def tag(ctx, _tag=None, *,_info=None):
    if ctx.guild != None:
        if _tag == None or _info == None:
            await ctx.send(f"Provide all parameters.\nCorrect format : `{PREFIX}tag tag_name info`\n\n"\
                     f"Example :\n```\n{PREFIX}tag monday maths - https://meet.google.com/xxx-xx-xxx\n"\
                     "phy - https://meet.google.com/xxx-xx-xxx```")

            return None

        for i in ALL_TAGS:
            if _tag.lower() == i["tag"]:
                await ctx.send("Tag is already present, replacing the old one.")
                i["info"] = _info
                i["author"] = ctx.author
                break

        else:
            ALL_TAGS.append({"author" : ctx.author, "tag" : _tag.lower(), "info" : _info})
            await ctx.send(f"Added a tag named `{_tag}`")
    else:
        await ctx.send("[Error] `tag` is a server only command.")



@client.command()
async def fetch(ctx, _tag=None):
    if ctx.guild != None:
        if _tag == None:
            await ctx.send(f"Provide the name of the tag you want to fetch.\nCorrect format : `{PREFIX}fetch tag_name`\n\n"\
                     f"Example :\n```\n{PREFIX}fetch monday```")

            return None


        for i in ALL_TAGS:
            if _tag.lower() == i['tag']:
                main_str = f"**__Tag Name : {i['tag']}__**\n"
                main_str += f"{i['info']}\n\n"
                main_str += f"This tag was added by **{i['author']}**"
                await ctx.send(main_str)
                break

        else:
            await ctx.send(f"No tag was found named `{_tag}`")
    else:
        await ctx.send("[Error] `fetch` is a server only command.")


@client.command()
@commands.has_any_role(MODS_ROLE_ID)
async def delete(ctx, _tag=None):
    if ctx.guild != None:
        if _tag == None:
            await ctx.send(f"Provide the name of the tag you want to delete.\nCorrect format : `{PREFIX}delete tag_name`\n\n"\
                     f"Example :\n```\n{PREFIX}delete monday```")
            return None

        for i in ALL_TAGS:
            if _tag.lower() == i['tag']:
                main_str = f"__**Tag Bot**__"
                main_str += f"Deleted the tag named **{i['tag']}**\n"
                main_str += f"with content :\n**{i['info']}**\n\n"
                main_str += f"This tag was added by **{i['author']}**"
                await ctx.send(main_str)
                ALL_TAGS.remove(i)
                break

        else:
            await ctx.send(f"No tag found named `{_tag}`.")


@client.command()
async def help(ctx):
    main_str = "**__Tag Bot__**\n"\
     f"`{PREFIX}fetch tag_name` - Use to fetch tags.\n"\
     f"`{PREFIX}tag tag_name info` - Use to create new tags and also to replace the old ones."\
     "(only Mods can use this)"

    await ctx.send(main_str)


@tasks.loop(seconds=60)
async def keepAlive():
    await client.get_channel(BOT_SPAM_CHANNEL).send(f"{client.user.mention}")


@client.event
async def on_message(message):
    if "<@!742780894619893881>" in message.content.split() or client.user.mention in message.content.split():
        if not message.author.bot:
            await message.channel.send(f"{message.author.mention}\nUse `{PREFIX}help` to see more options.")
        else:
            await message.channel.send(f"ok")

        return None

    await client.process_commands(message)


client.run(TOKEN)
