import discord
import openai
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

discord_token = os.getenv('DISCORD_TOKEN')
openai.api_key = os.getenv('OPENAI_API_KEY')
channel_id = int(os.getenv('CHANNEL_ID'))

# Define the intents you want to use
intents = discord.Intents.all()
intents.typing = False
intents.presences = False

# Create the bot instance with the specified intents
client = discord.Client(intents=intents,debug=True) 


@client.event
async def on_ready():
    print("We have logged in as {}".format(client.user))


def ask_question(question):
    response = openai.Completion.create(
        engine="text-davinci-003",  # Choose the appropriate OpenAI model
        prompt=question,
        max_tokens=100,  # Set the desired response length
        temperature=0.6,  # Adjust the temperature for response randomness
        n=1,  # Set the number of responses to generate
        stop=None,  # Add a custom stop sequence if needed
    )
    return response.choices[0].text


@client.event
async def on_message(message):
    print("Received message content:", message.content)
    if message.author == client.user:
        return

    if message.content.startswith('/ask'):
        question = message.content.replace('/ask', '').strip()
        print('Question:{}'.format(question))
        response = ask_question(question)
        await client.get_channel(channel_id).send(response)


client.run(discord_token)


