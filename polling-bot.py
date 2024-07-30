import discord
from discord.ext import commands
import os
import time
from datetime import datetime
from datetime import timedelta
import asyncio

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
async def poll(ctx, question, hours, *choices):

    try:
        await ctx.message.delete()
    except Exception as e:
        await ctx.send(f"The bot faced an error!, please try again later!")
        print(e)
        return

    if len(choices) < 2:
        await ctx.send("You need to provide more choices for the poll.")
        return
    
    if len(choices) > 10:
        await ctx.send("You can only provide up to 10 choices for the poll.")
        return
    
    hours = float(hours)
    endtime = datetime.now() + timedelta(hours=hours)
    formatted_date = endtime.strftime("%d %B, %Y %I:%M%p").lower()

    print(formatted_date)
    print(ctx.author.display_name)

    emoji_numbers = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
    answers = []

    for i in range(len(choices)):
        answers.append(f'{emoji_numbers[i]}\t-\t{choices[i]}')

    embed = discord.Embed(title=question, description="\n\n".join(answers), color=ctx.author.color)
    embed.set_footer(text=f"This poll will end at {formatted_date}\nPoll created by @{ctx.author.name}.")

    message = await ctx.send(embed=embed)

    for emoji in emoji_numbers[:len(choices)]:
        await message.add_reaction(emoji)
    
    try:
        dm_channel = await ctx.author.create_dm()
        embed = discord.Embed(
                    title=f"Hi, @{ctx.author.name}!, I have successfully created a poll for you.\n", 
                    description=f"Question:\n\t***{question}***\n\nOptions:\n\n"+"\n\n".join(answers), 
                    color=ctx.author.color
                )   
        embed.set_footer(text=f"This poll will end at {formatted_date}\nPoll created by @{ctx.author.name}.")
        await dm_channel.send(embed=embed)
    except Exception as e:
        print(f"Failed to send DM to {ctx.author.name}.") 
        print(e)
        await ctx.send(f"@{ctx.author.name} I can't send you a DM. Please check your DM settings.")

    await asyncio.sleep(hours * 60 * 60) 

    newmessage = await ctx.fetch_message(message.id)
    choices_ = {reaction.emoji: reaction.count - 1 for reaction in newmessage.reactions}

    print(newmessage.reactions)

    if all(value == next(iter(choices_.values())) for value in choices_.values()):
        result = "Result - The poll has ended in a tie between all options!"
    else:
        result = max(choices_, key=choices_.get)
        winners = [key for key in choices_ if choices_[key] == choices_[result]]
        if len(winners) == 1:
            winner_index = emoji_numbers.index(winners[0])
            result = f"Result - {choices[winner_index]} won the poll with {newmessage.reactions[emoji_numbers.index(winners[0])].count} votes."
        elif len(winners) > 1:
            result = f"Following options won the poll with same number of votes ({newmessage.reactions[emoji_numbers.index(winners[0])].count}):\n"
            result += "\n\t".join(
                [f"{winner}\t**{choices[emoji_numbers.index(winner)]}**" for winner in winners]
            )    

    print(result)

    ending_at = datetime.now().strftime("%d %B, %Y %I:%M%p").lower()

    embed = discord.Embed(title=question, description=result, color=ctx.author.color)
    embed.set_footer(text=f"This poll ended at {ending_at}.\nPoll created by @{ctx.author.name}.")
    
    await newmessage.edit(embed=embed)

    try:
        dm_channel = await ctx.author.create_dm()

        embed = discord.Embed(
                    title=f"Hi, @{ctx.author.name}!, Your poll has ended.\n", 
                    description=f"Question:\n\t***{question}***\n\nOptions:\n\n"+"\n\n".join(answers)+f"\n\n{result}", 
                    color=ctx.author.color
                )   
        embed.set_footer(text=f"This poll ended at {ending_at}\nPoll created by @{ctx.author.name}.")

        await dm_channel.send(embed=embed)
    except:
        await ctx.send(f"@{ctx.author.name} I can't send you a DM. Please check your DM settings.")

bot.run(token)
