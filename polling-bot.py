import discord
from discord.ext import commands
import os
import time

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

token = os.getenv('POLLING_BOT_TOKEN')

def all_equal(iterator):
    iterator = iter(iterator)
    try:
        first = next(iterator)
    except StopIteration:
        return True
    return all(first == x for x in iterator)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


@bot.command(name='poll')
async def poll(ctx, question, *choices):
    print(ctx.author.display_name)
    if len(choices) < 2:
        await ctx.send("You need to provide more choices for the poll.")
    if len(choices) > 10:
        await ctx.send("You can only provide up to 10 choices for the poll.")
    
    emoji_numbers = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
    answers = []
    for i in range(len(choices)):
        answers.append(f'{emoji_numbers[i]} - {choices[i]}')
    
    embed = discord.Embed(title=question, description="\n\n".join(answers), color=ctx.author.color)
    embed.set_footer(text=f"Poll created by {ctx.author.name}.")
    message = await ctx.send(embed=embed)
    for emoji in emoji_numbers[:len(choices)]:
        await message.add_reaction(emoji)
    
    time.sleep(5)

    newmessage = await ctx.fetch_message(message.id)
    choices_ = {}
    reactions = newmessage.reactions
    result = "TIE"
    for i in range(len(reactions)):
        choices_[reactions[i].emoji] = reactions[i].count - 1
    print(reactions)

    if all_equal(choices_.values()):
        result = "TIE"
    else:
        result = max(choices_, key=choices_.get)

    print(result)

    embed = discord.Embed(title=question, description=f"Result: {result}", color=ctx.author.color)
    embed.set_footer(text=f"Poll created by {ctx.author.name}.")
    await newmessage.edit(embed=embed)


bot.run(token)
