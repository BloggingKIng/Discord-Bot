import discord
import os 
import requests
import random
import sqlite3

intents =  discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
token = os.getenv('DISCORD_TOKEN')

api_endpoint = "https://api.api-ninjas.com/v1/quotes?category=inspirational"
api_key = os.getenv('API_KEY')

sad_words = ["sad", "depress", "unhappy", "angry", "miserable", "cry"]
starter_encouragements = ["Cheer up!", "Hang in there.", "You are a great person!", "Hard Times will pass."]

con = sqlite3.connect('data.db')    
cur = con.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS encouragements(encouragement TEXT)')

def get_quote():
    response = requests.get(
        api_endpoint,
        headers={'X-Api-Key': api_key}
    )
    if response.status_code == requests.codes.ok:
        return f"\"*{response.json()[0]['quote']}*\"\n\t" + " " + f"({response.json()[0]['author']})"
    else:
        return "I could not retrieve a quote from the API. Try again later!"

def update_encouragements(encouraging_message):
    if encouraging_message:
        cur.execute('INSERT INTO encouragements VALUES (?)', (encouraging_message,))
        con.commit()

def delete_encouragement(number):
    cur.execute('DELETE FROM encouragements WHERE rowid = ?', (number,))
    con.commit()

@client.event
async def on_ready():
    print('Logged in as', {client.user})

responding = True
@client.event
async def on_message(msg):
    global responding
    if msg.author == client.user:
        return
    
    if msg.content.startswith('/greet'):
        person_name = msg.content.split()[1]
        await msg.channel.send(f'Hello {person_name}!')
    
    if msg.content.startswith('/inspire'):
        quote = get_quote()
        await msg.channel.send(quote)

    if msg.content.startswith('/new'):
        encouraging_message = msg.content.split(" ", 1)[1]
        update_encouragements(encouraging_message)
        await msg.channel.send("New encouraging message added.")
    
    if msg.content.startswith('/del'):
        number = int(msg.content.split(" ")[1])
        delete_encouragement(number)
        db_encouragements = cur.execute('SELECT * FROM encouragements').fetchall()
        message = 'Encouragements:'
        for i in range(len(db_encouragements)):
            message = message + '\n' + str(db_encouragements[i][0])
        await msg.channel.send(message if len(db_encouragements) > 0 else 'No encouragement found in database.')
        await msg.channel.send("Encouraging message deleted.")
    
    if msg.content.startswith('/list'):
        db_encouragements = cur.execute('SELECT rowid, encouragement FROM encouragements').fetchall()
        message = 'Encouragements:'
        for i in range(len(db_encouragements)):
            print(db_encouragements[i])
            message = message + '\n' + str(db_encouragements[i][0]) + f" ({db_encouragements[i][1]})"
        if len(db_encouragements) == 0:
            message = 'No encouragement found.'
        await msg.channel.send(message)
    
    if msg.content.startswith('/responding'):
        value = msg.content.split(' ')[1]
        if value.lower() == 'true':
            responding = True
            await msg.channel.send('Responding is on.')
        else:
            responding = False
            await msg.channel.send('Responding is off.')
    
    print(responding)
    if responding == True:
        options = starter_encouragements
        db_encouragements = cur.execute('SELECT * FROM encouragements').fetchall()
        if len(db_encouragements) > 0:
            options = options + list(i[0] for i in db_encouragements)
            print(list(db_encouragements))
    
        if any(word in msg.content for word in sad_words):
            await msg.channel.send(random.choice(options))

client.run(token)