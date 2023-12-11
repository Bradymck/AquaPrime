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

tracemalloc.start()
load_dotenv()
# Console Messages
print(discord.__version__)
print(openai.__version__)

# Global Variables
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

  def __init__(self, PINECONE_API_KEY, PINECONE_INDEX_NAME):
    try:
      # Add an indented block here
      pass
    except Exception:
      # Exception handling code

  # Run the bot
  async def main():
    bot = MyBot()
    await bot.run(os.environ['DISCORD_TOKEN'])

def run_bot():
  # Define the run_bot function here
  pass

run_bot()

run_bot()
