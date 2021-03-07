import discord
import os
import requests
import json
import random
from replit import db



client = discord.Client()

sad_words = ["sad","dukhi","depressed","cry","unhappy","angry","gussa", "miserable" , "depressing", "low"]

starter_encouragements = [
  "Hang in there. Its gonna be better one day!",
  "Hang in there , friend. You are strong and we will fight this together",
  "Cheer up!, We will make progress together",
  "Hang in there. You will feel better if u listen to music on my friend @Groovy", 
  "Zyada tension naa lo aap! Sab theek hojaega",
  "Rab sab dekhraha h. Sabar karo mehar hogi ",
  "Don't worry! Be Happy :) Type $inspire to get inspired."]

def get_quote():
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragements(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements


@client.event
async def on_ready():
  print('We have logged in {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  msg = message.content

  if message.content.startswith('$hello'):
    await message.channel.send('Hello!')

  if message.content.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

 

  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(starter_encouragements))
  
 
  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)
  
  if msg.startswith("$responding"):
    value = msg.split("$responding ",0)[0]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")


client.run(os.getenv('TOKEN'))
