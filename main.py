import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive
import giphy_client
import time
import giphy_client
from giphy_client.rest import ApiException
from pprint import pprint
from discord.ext import commands

client = discord.Client()

sad_words = [
    "sad", "dukhi", "depressed", "cry", "unhappy", "angry", "gussa",
    "miserable", "depressing", "low", " :( "
]

happy_words = ["happy", "khush", "smiling", "fine", "Happy", " :)"]

starter_encouragements = [
    "Hang in there. Its gonna be better one day!",
    "Hang in there , friend. You are strong and we will fight this together",
    "Cheer up!, We will make progress together",
    "Hang in there. You will feel better if u listen to music on my friend @Groovy",
    "Zyada tension naa lo aap! Sab theek hojaega",
    "Rab sab dekhraha h. Sabar karo mehar hogi ",
    "Don't worry! Be Happy :) Type $inspire to get inspired."
]

happy_responses = [
    "Me bhi Happy te tu bhi happy ¯\_(ツ)_/¯  ",
    "Happy paaji wishes you always stay happy",
]

weather_starters = [
    "Whats the weather like today?", "Weather today?", "Mausam kesa h aaj?"
]

if "responding" not in db.keys():
    db["responding"] = True


def get_quote():
    response = requests.get('https://zenquotes.io/api/random')
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " - " + json_data[0]['a']
    return (quote)


def get_weather():

    api_key = 'xyz'
    api_address = 'http://api.openweathermap.org/data/2.5/weather?appid=0c42f7f6b53b244c78a418f4f181282a&q='
    city = channel.send(user.input('City Name :'))
    url = api_address + city
    json_data = requests.get(url).json()
    format_add = json_data['base']
    return (format_add)


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

    if message.content.startswith('$weather'):
        weather = get_weather()
        await message.channel.send(weather)

    if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(starter_encouragements))

    if any(word in msg for word in happy_words):
        await message.channel.send(random.choice(happy_responses))


@client.event
async def gif(message):
    if message.author == client.user:
        return
    q = "random"
    api_key = "g9ddOux3MTnFA0cviiUivs9fOJMRTSF6"
    api_instance = giphy_client.DefaultApi()
    api_response = api_instance.gifs_search_get(api_key,
                                                q,
                                                limit=5,
                                                rating='g',
                                                fmt='json')
    lst = list(api_response.data)
    giff = random.choice(lst)

    if message.content.startswith('$gif'):
        await message.channel.send(giff)


keep_alive()
client.run(os.getenv('TOKEN'))
