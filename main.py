# This example requires the 'message_content' intent.
import json
import os
import sys

import interactions


def load_faq_json(file_path):
    if not os.path.exists(file_path):
        # File doesn't exist, create it
        with open(file_path, 'w') as file:
            file.write('{}')  # Writing an empty JSON object if you want an empty file
        print(f"Created faq {file_path}")
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def read_file_as_string(file_path):
    with open(file_path, 'r') as file:
        file_contents = file.read()
    return file_contents


key_file_path = "./key"
faq_dict_path = "./faq.json"
faq_list = load_faq_json(faq_dict_path)
reserved = ["list"]


def handle_faq(key) -> str:
    if key == "list":
        return f"# {len(sorted_keys())} available faqs:\n```" + ", ".join(sorted_keys()) + "```"
    if key in faq_list:
        faq = faq_list[key]
        return "## " + faq["question"] + "\n" + faq["answer"]
    else:
        return f"unknown argument {key}. try help"


def save_faq():
    with open(faq_dict_path, 'w') as file:
        json.dump(faq_list, file, indent=4)  # indent=4 for pretty formatting


def sorted_keys():
    return sorted(list(faq_list.keys()) + ["list", "help"])


def set_faq(key, value):
    if key in reserved:
        return False
    faq_list[key] = value
    save_faq()
    return True


def get_def_faq(key):
    if key in faq_list:
        return faq_list[key]
    else:
        return {"question": "?", "answer": "!"}


def del_faq(key):
    if key in reserved:
        return False
    if key not in faq_list:
        return True
    del faq_list[key]
    save_faq()
    return True


token = read_file_as_string(key_file_path)
bot = interactions.Client(token=token,
                          default_scope=474510862514782208)


@bot.command(
    name="faq",
    description="Get answers to frequently asked questions.",
    options=[
        interactions.Option(
            name="key",
            description="Key of the faq",
            type=interactions.OptionType.STRING,
            required=True
        ),
    ],
)
async def faq_key(ctx: interactions.CommandContext, key: str):
    """This is the first command I made!"""
    await ctx.send(handle_faq(key))


@bot.command(
    name="faq_set",
    description="Set answers to frequently asked questions.",
    default_member_permissions=interactions.Permissions.MANAGE_MESSAGES,
    options=[
        interactions.Option(
            name="key",
            description="Key of the faq",
            type=interactions.OptionType.STRING,
            required=True,
        ),
        interactions.Option(
            name="type",
            description="type of the entry",
            type=interactions.OptionType.STRING,
            required=True,
            choices=[interactions.Choice(name="Question", value="question"),
                     interactions.Choice(name="Answer", value="answer")],
        ),
        interactions.Option(
            name="text",
            description="Text for chosen type",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def faq_set(ctx: interactions.CommandContext, key: str, type: str, text: str):
    """This is the first command I made!"""
    entry = get_def_faq(key)
    entry[type] = text.replace("\\n", "\n").replace("\\t", "\t")
    success = set_faq(key, entry)
    await ctx.send(f"{key} -> {text} ({type})\n{'success' if success else 'failed'}")


@bot.command(
    name="faq_del",
    description="Delete faq entry.",
    options=[
        interactions.Option(
            name="key",
            description="Key of the faq",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
    default_member_permissions=interactions.Permissions.MANAGE_MESSAGES,
)
async def faq_del(ctx: interactions.CommandContext, key: str):
    success = del_faq(key)
    await ctx.send(f"delete {key}: {'success' if success else 'failed'}")


@bot.command(
    name="faq_stop",
    description="Exit the bot (for autorestart).",
    default_member_permissions=interactions.Permissions.MANAGE_MESSAGES,
)
async def exit_bot(ctx):
    await ctx.send("Exiting bot...")
    sys.exit()

print(f"start bot with token {token}")
bot.start()
