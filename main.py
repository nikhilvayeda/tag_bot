import os
import discord
from discord.ext import commands

# Constants
MODS_ROLE_ID = 727418087523090483
ALL_TAGS = []
PREFIX = ":"
TOKEN = os.getenv("TOKEN")

client = commands.Bot(command_prefix=PREFIX)
client.remove_command("help")


@client.event
async def on_ready():
    print('ready...')


@client.command()
@commands.has_any_role(MODS_ROLE_ID)
async def tag(ctx, _tag=None, *,_info=None):
    if _tag == None or _info == None:
        await ctx.send(f"Provide all parameters.\nCorrect format : `{PREFIX}tag tag_name info`\n\n"\
                 f"Example :\n```\n{PREFIX}tag monday maths - https://meet.google.com/xxx-xx-xxx\n"\
                 "phy - https://meet.google.com/xxx-xx-xxx```")

        return None

    for i in ALL_TAGS:
        if _tag.lower() == i["tag"]:
            await ctx.send("Tag is already present, replacing the old one.")
            i["info"] = _info
            break

    else:
        ALL_TAGS.append({"author" : ctx.author, "tag" : _tag.lower(), "info" : _info})
        await ctx.send(f"Added a tag named `{_tag}`")



@client.command()
async def fetch(ctx, _tag=None):
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



@client.command()
async def help(ctx):
    main_str = "**__Tag Bot__**\n"\
     f"`{PREFIX}fetch tag_name` - Use to fetch tags.\n"\
     f"`{PREFIX}tag tag_name info` - Use to create new tags and also to replace the old ones."\
     "(only Mods can use this)"

    await ctx.send(main_str)

client.run(TOKEN)
