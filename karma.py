import json
import glob
from os import path
from pyrogram import Client, filters
from config import bot_token, owner_id

app = Client(
    "karma",
    bot_token=bot_token,
    api_id=2191715,
    api_hash="f8f5367907ae63115bbdce3524b87671",
)

regex_upvote = r"^((?i)\+|\+\+|\+1|thx|tnx|ty|thank you|thanx|thanks|pro|cool|good|👍)$"
regex_downvote = r"^(\-|\-\-|\-1|👎)$"


# @app.on_message(filters.command(["start"]))
# async def start(_, message):
#     await message.reply_text(
#         "Hey, I'm A Karma Bot, You Can Upvote Or Downvote Someone Using Me, Join @TheHamkerChat For Support!"
#     )


# @app.on_message(filters.command(["help"]))
# async def help(_, message):
#     await message.reply_text(
#         """+ To Upvote A Message.
# - To Downvote A Message.
# /karma To Check Karma Points Of This Group."""
#     )


@app.on_message(filters.text
                & filters.group
                & filters.incoming
                & filters.reply
                & filters.regex(regex_upvote)
                & ~filters.via_bot
                & ~filters.bot
                & ~filters.edited)
async def upvote(_, message):
    if message.reply_to_message.from_user.id == message.from_user.id:
        return

    chat_id = message.chat.id
    user_id = message.reply_to_message.from_user.id
    user_mention = message.reply_to_message.from_user.mention
    filename = f"{chat_id}.json"

    if not path.exists(filename):
        sample_bot = {"1527962675": 1}
        with open(filename, "w") as f:
            f.write(json.dumps(sample_bot))
    with open(filename) as f2:
        members = json.load(f2)
    if not f"{user_id}" in members:
        members[f"{user_id}"] = 1
    else:
        members[f"{user_id}"] += 1
    with open(filename, "w") as f3:
        f3.write(json.dumps(members))
    await message.reply_text(
        f'Incremented Karma of {user_mention} By 1 \nTotal Points: {members[f"{user_id}"]}'
    )


@app.on_message(filters.text
                & filters.group
                & filters.incoming
                & filters.reply
                & filters.regex(regex_downvote)
                & ~filters.via_bot
                & ~filters.bot
                & ~filters.edited)
async def downvote(_, message):
    if message.reply_to_message.from_user.id == message.from_user.id:
        return
    chat_id = message.chat.id
    user_id = message.reply_to_message.from_user.id
    user_mention = message.reply_to_message.from_user.mention
    filename = f"{chat_id}.json"

    if not path.exists(filename):
        sample_bot = {"1527962675": 1}
        with open(filename, "w") as f:
            f.write(json.dumps(sample_bot))
    with open(filename) as f2:
        members = json.load(f2)
    if not f"{user_id}" in members:
        members[f"{user_id}"] = 1
    else:
        members[f"{user_id}"] -= 1
    with open(filename, "w") as f3:
        f3.write(json.dumps(members))
    await message.reply_text(
        f'Decremented Karma Of {user_mention} By 1 \nTotal Points: {members[f"{user_id}"]}'
    )


@app.on_message(filters.command(["karma"]) & filters.group)
async def karma(_, message):
    chat_id = message.chat.id
    filename = f"{chat_id}.json"
    with open(filename) as f2:
        members = json.load(f2)
    if not message.reply_to_message:
        output = ""
        m = 0
        for i in members.keys():
            try:
                output += f"`{(await app.get_chat(i)).username}: {list(members.values())[m]}`\n"
            except:
                pass
            m += 1
        await message.reply_text(output)

    else:
        user_id = message.reply_to_message.from_user.id
        await message.reply_text(f'Total Points: {members[f"{user_id}"]}')


@app.on_message(filters.command(["backup"]) & filters.user(owner_id))
async def backup(_, message):
    m = await message.reply_text("Sending..")
    files = glob.glob("*n")
    for i in files:
        await app.send_document(owner_id, i)
    await m.edit("Backup Sent In Your PM")


app.run()
