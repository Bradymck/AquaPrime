import asyncio
import logging
import os
import re
import traceback
import tracemalloc
import warnings
from datetime import datetime, timedelta

import discord
import openai
import pinecone
import pymongo
import weaviate

from discord.ext import commands
from dotenv import load_dotenv

from prompt_generator import PromptGenerator
import openai
from openai.embeddings_utils import get_embedding


tracemalloc.start()
load_dotenv()
# Console Messages
print(discord.__version__)
print(openai.__version__)

# Global Variables🌐
# Load the OpenAI API key
openai.api_key = os.environ['OPENAI_KEY']
client = pymongo.MongoClient(os.environ['MONGO_URI'])
messages_collection = None
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

bot_name = ""
bot_description = "Act as 😾. The iconic meme"
bot_owner = "Grumpy Cat#9218"
bot_color = 0x00ff00
bot_footer = ""
bot_footer_icon = "https://i.imgur.com/g6FSNhL.png"
bot_thumbnail = "https://cdn.discordapp.com/attachments/1147333483610525787/1147333505341210624/Grumpy_Cat_smoking.jpg"
bot_image = "https://cdn.discordapp.com/attachments/1147333483610525787/1147333505341210624/Grumpy_Cat_smoking.jpg"
bot_invite = "https://discord.com/<invite>"
bot_support = "https://discord.gg/trXkq4qj76"
bot_github = "https://github.com/AquaPrime/GrumpyCat"
bot_website = "https://AquaPrime.io/"
bot_donate = "https://www.streamtide.io/AquaPrime"
bot_patreon = "https://www.patreon.com/AquaPrime"
bot_topgg = "https://top.gg/bot/AquaPrime"
bot_discordbotlist = "https://discordbotlist.com/bots/AquaPrime"
bot_discordbotsgg = "https://discord.bots.gg/bots/AquaPrime"
bot_discordextremelist = "https://discordextremelist.xyz/en-US/bots/AquaPrime"
bot_discordbotsggco = "https://discord.bots.gg/bots/AquaPrime"

openai_embed_model = "text-embedding-ada-002"
# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("grumpy_cat")

# Create a dictionary of effects for the spell command
last_execution = {}

# Create an instance of PromptGenerator
prompt_generator = PromptGenerator()


# Initialize logging
def initialize_logging():
  logging.basicConfig(filename='error_log.log', level=logging.DEBUG)
  logging.basicConfig(level=logging.DEBUG,
                      format='%(asctime)s - %(levelname)s - %(message)s',
                      filename='bot.log',
                      filemode='a')
  warnings.filterwarnings("ignore")


# Connect to MongoDB
def connect_to_mongodb():
  global client, messages_collection
  try:
    db = client.get_database('YOUR_DATABASE_NAME')
    messages_collection = db.get_collection('YOUR_COLLECTION_NAME')
    messages_collection.count_documents(
        {})  # This line will trigger a ping to the MongoDB deployment
    print("Pinged your deployment. You successfully connected to MongoDB!")
  except Exception:
    traceback.print_exc()


def process_hdd_context(weaviate_results):
  if weaviate_results is None:
    hdd_context = "No results found in HDD section."
  else:
    message_count = len(weaviate_results['data']['Get']['Message'])
    hdd_context = f"Found {message_count} messages in HDD section.\n"

    # Append the vector search results to the HDD section
    for result in weaviate_results['data']['Get']['Message']:
      username = result['username']
      message = result['message']
      timestamp = result['timestamp']
      hdd_context += f"User: {username}, Message: {message}, Timestamp: {timestamp}\n"

  return hdd_context


# Weaviate Client
class WeaviateClient:

  def __init__(self):
    try:
      self.client = weaviate.Client(url=os.getenv("WEAVIATE_ENDPOINT"),
                                    auth_client_secret=weaviate.AuthApiKey(
                                        api_key=os.getenv("WEAVIATE_API_KEY")))
      schema = self.client.schema.get()
      print("Weaviate schema:", schema)
    except Exception as e:
      print("Error initializing Weaviate client:", str(e))

  @staticmethod
  def sanitize_string(input_str):
    if not isinstance(input_str, str):
      return ""
    return input_str.replace('"', '\\"').replace('\n', '\\n')

  @staticmethod
  def strip_escape_sequences(input_str):
    return re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', input_str)

  def search_data(self, user_id):
    try:
      sanitized_user_id = self.sanitize_string(user_id)
      sanitized_user_id = self.strip_escape_sequences(sanitized_user_id)
      where_filter = {
          "path": ["username"],
          "operator": "Equal",
          "valueString": sanitized_user_id
      }
      results = self.client.query.get(
          "Message",
          ["username", "message", "timestamp", "channel_id", "server_id"
           ]).with_where(where_filter).do()
      return results
    except Exception as e:
      print(f"Error querying Weaviate: {e}")
      return None


# OpenAI Client
class OpenAI:

  def __init__(self, weaviate_client):
    self.weaviate_client = weaviate_client
    self.api_key = os.environ['OPENAI_KEY']
    openai.api_key = self.api_key

  # Inside the OpenAI class, update the generate_response method as follows
  def generate_response(self, openai_messages):
    try:
      completion = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[{
              "role": "system",
              "content": "You are a helpful assistant."
          }, {
              "role": "user",
              "content": openai_messages
          }],
          max_tokens=250,
          n=1,
          stop=[
              "Human:", "AI:"
          ]  # Stopping tokens may need to be adjusted based on your dialogue format
      )
      return completion.choices[0].message[
          'content'] if completion else "No response generated."
    except Exception:
      traceback.print_exc()
      return "An error occurred while generating a response."


class PineconeClient:
  # Bot should listen for the word "quest" & "guild"
  # When "quest" is read the bot should upsert message data to pinecone database
  # When "#Quest" prompt is received, bot should respond with data regarding "quest" it has in pinecone database

  def __init__(self, PINECONE_API_KEY, PINECONE_INDEX_NAME,
               PINECONE_ENVIRONMENT):
    print("Initializing PineconeClient...")

    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
    self.index_name = PINECONE_INDEX_NAME

    print(f"Index Name: {PINECONE_INDEX_NAME}")
    print(f"Environment: {PINECONE_ENVIRONMENT}")

    def upsert_to_pinecone(self, message_id, message_content, user_id, timestamp):
      print("Upserting to Pinecone...")
      index = pinecone.Index(self.index_name)
      print("Embedding message content for Pinecone upsert...")
      MODEL = "text-embedding-ada-002"

      # Create the embeddings for the message content using the correct API call
      res = openai.Embedding.create(
          model=MODEL,
          input=message_content
      )

      embeds = res['data']
      print("Embedding process completed.")

      # Check if the index exists and create it if not
      if self.index_name not in pinecone.list_indexes():
          pinecone.create_index(self.index_name, dimension=len(embeds[0]['embedding']))
          index = pinecone.Index(self.index_name)
          print("Index created: ", self.index_name)
        
      def summarize(self, keyword, user_id):
        print("Fetching from Pinecone...")
        index = pinecone.Index(self.index_name)
        openai.api_key = os.environ["OPENAI_KEY"]
        one_day_ago = int((datetime.utcnow() - timedelta(days=1)).timestamp())
      # Generate the embedding for the keyword
      query_embedding = get_embedding(keyword, openai.api_key)
      query_response = index.query(
          top_k=10,
          include_values=False,
          include_metadata=True,
          vector=query_embedding,
          filter={
              "user_id": {
                  "$eq": str(user_id)
              },
              "timestamp": {
                  "$gte": one_day_ago
              },
          },
      )

      print("Data upsertion complete.")
      return upsert_response

  def summarize(self, keyword, user_id):
    print("Fetching from Pinecone...")

    index = pinecone.Index(self.index_name)
    openai.api_key = os.environ["OPENAI_KEY"]

    one_day_ago = int((datetime.utcnow() - timedelta(days=1)).timestamp())

    query_response = index.query(
        top_k=10,
        include_values=False,
        include_metadata=True,
        vector=res["data"][0]["embedding"],
        filter={
            "user_id": {
                "$eq": str(user_id)
            },
            "timestamp": {
                "$gte": one_day_ago
            },
        },
    )

    message_list = [
        match["metadata"]["message"] for match in query_response["matches"]
    ]

    print("Message List reterieved from pinecone: ", message_list)

    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role":
                "system",
                # Change this prompt to get different summary responses
                "content":
                "You are a knowledgeable record keeper, well-versed in the details of quests and guilds. Provide a detailed summary for each event mentioned below and keep the response under 2000 characters in length.",
            },
            {
                "role": "user",
                "content": str(message_list)
            },
        ],
        n=1,
        # Use max_tokens variable to change the length of the response
        # max_tokens=250,
        temperature=0,
    )

    print(completion.choices[0].message)

    reply = completion.choices[0].message.content.strip()
    reply = reply.split("Assistant:")[0].strip()
    reply = reply.split("User:")[0].strip()

    # Truncate the message if it's longer than 2000 characters
    if len(reply) > 2000:
      reply = reply[:1997] + "..."

    return reply


# Process OS Context
def process_os_context():
  os_context = "Aqua Prime, a virtual world where players engage in a multifaceted TTRPG experience."
  return os_context


# Sanitize Message
def sanitize_message(message_content):
  return re.sub(r'<@!?[0-9]+>', '', message_content)


# Process RAM Context
def process_ram_context(ram_messages, bot_user_id):
  static_instruction = "Bot Instructions: Handle the following user messages.\n"
  user_messages = [
      msg for msg in ram_messages.split('\n') if str(bot_user_id) not in msg
  ]
  return static_instruction + '\n'.join(user_messages)


# Process User Context
def process_user_context():
  user_context = "This is the core message..."
  return user_context


# Command Error Handler
@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
    minutes = int(error.retry_after // 60)
    seconds = int(error.retry_after % 60)
    await ctx.send(
        f"You're on cooldown! Please wait {minutes} minutes and {seconds} seconds before using this command again."
    )
  else:
    pass


# Bot Ready Event
@bot.event
async def on_ready():
  print(f'Logged in as {bot.user.name} - {bot.user.id}')
  print(f'This bot is in {len(bot.guilds)} guilds!')


#pineconeClient
pinecone_client = PineconeClient(
    os.environ["PINECONE_API_KEY"],
    os.environ["PINECONE_INDEX_NAME"],
    os.environ["PINECONE_ENVIRONMENT"],
)


# Bot Message Event
@bot.event
async def on_message(message):
  try:
    weaviate_client = WeaviateClient()
    OpenAI(weaviate_client)
    if message.author == bot.user:
      return

    keywords = ["quest", "guild"]
    command_keywords = {"#quest": "Quest", "#guild": "Guild"}
    is_command = any(command in message.content.lower()
                     for command in command_keywords)

    if not is_command and any(keyword in message.content.lower()
                              for keyword in keywords):

      async def background_upsert(message):
        message_id = message.id
        message_content = re.sub(r"<@!?[0-9]+>", "", message.content).strip()
        user_id = message.author.id
        timestamp = int(datetime.utcnow().timestamp())
        upsert_response = pinecone_client.upsert_to_pinecone(
            message_id, message_content, user_id, timestamp)

        upsert_response

      asyncio.create_task(background_upsert(message))
    else:
      pass

    for command, keyword in command_keywords.items():
      if command in message.content.lower():
        user_id = message.author.id

        reply = pinecone_client.summarize(keyword, user_id)
        async with message.channel.typing():
          await asyncio.sleep(2)  # optional, to enhance the typing effect
          await message.channel.send(reply)

    #try:
    # Retrieve the Weaviate search results
    # weaviate_results = weaviate_client.search_data(str(message.author.id))
    #print("Weaviate search results:", weaviate_results)
    #except Exception as e:
    #print(f"Weaviate search error: {e}")
    # return

    #try:
    # Retrieve the Weaviate search results
    #weaviate_results = weaviate_client.search_data(str(message.author.id))
    #print("Weaviate search results:", weaviate_results)
    #except Exception as e:
    # print(f"Weaviate search error: {e}")
    #return

    if bot.user.mentioned_in(message):
      sanitized_message = sanitize_message(message.content)
      mentioned_users = set()
      for user in message.mentions:
        mentioned_users.add((user.name, user.id))

      connect_to_mongodb()

      messages_collection.insert_one({
          'username':
          str(message.author.name),
          'user_id':
          str(message.author.id),
          'message':
          sanitized_message,
          'timestamp':
          str(message.created_at),
          'channel_id':
          str(message.channel.id),
          'server_id':
          str(message.guild.id),
          'message_id':
          str(message.id),
          'reactions': [str(reaction.emoji) for reaction in message.reactions],
          'attachments':
          [str(attachment.url) for attachment in message.attachments],
          'embeds': [str(embed.to_dict()) for embed in message.embeds],
          'mentioned_users': [str(user.id) for user in message.mentions]
      })

    channel = message.channel
    past_messages = messages_collection.find({
        'channel_id': str(channel.id)
    }).sort('_id', -1).limit(5)
    ram_messages = "\n".join([
        f"\033[31m{sanitize_message(msg['message'])}\n\033[0m"
        for msg in past_messages
    ])

    # Generate prompts using PromptGenerator
    process_os_context()
    process_ram_context(ram_messages, bot.user.id)

    # Pass the Weaviate search results to the process_hdd_context function
    #hdd_section = process_hdd_context(weaviate_results)

    # Construct the openai_messages variable
#    openai_messages = prompt_generator.generate_prompt(static_instruction,
#                                                      os_section, ram_section,
#                                                     system_section,
#                                                    hdd_section,
#                                                   user_input_section)

#response = openai_instance.generate_response(openai_messages)

#console_prompt = prompt_generator.generate_prompt(static_instruction,
#                                                 os_section, ram_messages,
#                                                system_section,
#                                               hdd_section,
#                                             user_input_section)
#print("\n🤖 Prompt to OpenAI:")
#print(console_prompt)

#response = openai_instance.generate_response(openai_messages)
#response_sections = response.split("HDD:")
#assistant_reply = response_sections[0]

#if assistant_reply.strip():
# async with message.channel.typing():
#  await asyncio.sleep(2)
# if len(assistant_reply) > 2000:
#  assistant_reply = assistant_reply[:
#                                   2000]  # Truncate the response to fit the Discord limit
#await message.channel.send(assistant_reply.strip())

  except Exception:
    traceback.print_exc()

  await bot.process_commands(message)


# Run the Bot
def run_bot():
  try:
    # Initialize the Weaviate client and OpenAI instance
    weaviate_client = WeaviateClient()
    OpenAI(weaviate_client)

    # Connect to MongoDB
    connect_to_mongodb()

    # Load the game commands
    async def load_game_commands():
      await bot.load_extension('gameCommands')
      print("Game commands loaded successfully")
      # Load the cogs
    async def load_cogs():
      await bot.load_extension('cogs.admin')
      await bot.load_extension('cogs.fun')
      await bot.load_extension('cogs.info')
      await bot.load_extension('cogs.moderation')
      await bot.load_extension('cogs.music')
      await bot.load_extension('cogs.owner')
      await bot.load_extension('cogs.reactions')
      await bot.load_extension('cogs.search')

    @bot.event
    async def on_ready():
      print(f'Logged in as {bot.user.name} - {bot.user.id}')
      print(f'This bot is in {len(bot.guilds)} guilds!')
      await load_game_commands()


# Move the create_task call inside the on_ready event

# Run the bot

    bot.run(os.environ['DISCORD_TOKEN'])

  except Exception:
    traceback.print_exc()
  # Take a snapshot and display the top 10 memory blocks allocated
  snapshot = tracemalloc.take_snapshot()
  top_stats = snapshot.statistics('lineno')
  print("[ Top 10 ]")
  for stat in top_stats[:10]:
    print(stat)
run_bot()
