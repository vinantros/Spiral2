import discord
import os
import sqlite3
from discord.ext import commands
from dotenv import load_dotenv
from langchain.memory.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationEntityMemory

# load environment variables
TOKEN = os.environ["DISCORD_BOT_TOKEN"]

# set up Discord bot intents
intents = discord.Intents.all()
intents.messages = True

# initialize OpenAI langchain model and conversation chain
llm = OpenAI(temperature=0)
conversation = ConversationChain(
    llm=llm, 
    verbose=True,
    prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
    memory=ConversationEntityMemory(llm=llm))

# define function to predict output based on input topic
def ai_chat(topic):
    output = conversation.predict(input=topic)
    return output

# define custom Discord bot class
class SpiralBot(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # open database connection
        self.conn = sqlite3.connect('developers.db')

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(message.author.id)
        # create cursor for database connection
        c = self.conn.cursor()
        
        if message.content.lower().startswith('spiral'):
            # check if user is authorized to use bot
            c.execute("SELECT id FROM developers WHERE id = ?", (str(message.author.id),))
            result = c.fetchone()
            if result is not None:
                member_name = message.author.name
                member_message = message.content

                # import feature to handle authorized user's message
                from features import jailbreak
                response = jailbreak.jailbreak_chat(member_name, member_message)
                await message.channel.send(response)
            else:
                # predict output and send response to Discord channel
                topic = message.content.lower().replace("spiral ", "")
                answer = ai_chat(topic)
                await message.channel.send(answer)
        # process commands
        await self.process_commands(message)

    def cog_unload(self):
        # close database connection when bot is unloaded
        self.conn.close()

# instantiate custom bot object and run bot
bot = SpiralBot(command_prefix='!', intents=intents)
bot.load_extension('cogs.Cogs')
bot.run(TOKEN)



