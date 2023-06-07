import discord
from discord.ext import commands
import sqlite3
from io import BytesIO

class Cogs(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot
    
    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot
        self.conn = sqlite3.connect('developers.db')
        self.c = self.conn.cursor()

    @commands.command() # creates a prefixed command
    async def hello(self, ctx): # all methods now must have both self and ctx parameters
        await ctx.send('Hello!')


    @discord.slash_command()
    async def add_developer(self, ctx, new_dev: discord.User):
        # Check if the user executing the command is a developer
        self.c.execute("SELECT id FROM developers WHERE id = ?", (str(ctx.author.id),))
        result = self.c.fetchone()
        if result is None:
            await ctx.send("Sorry, you must be a developer to use this command.")
            return
        self.c.execute("SELECT id FROM developers WHERE id = ?", (str(new_dev.id),))
        result = self.c.fetchone()
        if result is None:
            self.c.execute("INSERT INTO developers VALUES (?)", (str(new_dev.id),))
            self.conn.commit()
            await ctx.send(f'Added {new_dev.name} to developer list.')
        else:
            await ctx.send(f'{new_dev.name} is already in developer list.')
     
    # remove_developer command       
    @commands.command(name='remove_developer')
    async def remove_developer(self, ctx, dev: discord.User):
        self.c.execute("SELECT id FROM developers WHERE id = ?", (str(dev.id),))
        result = self.c.fetchone()
        if result is not None:
            self.c.execute("DELETE FROM developers WHERE id = ?", (str(dev.id),))
            self.conn.commit()
            await ctx.send(f'Removed {dev.name} from developer list.')
        else:
            await ctx.send(f'{dev.name} is not in developer list.')

    
    @discord.slash_command()
    async def youtube(self, ctx, url: str):
        from features import search
        if url.startswith("https://www.youtube.com/watch?v=") or url.startswith("https://youtu.be/"):
            await ctx.respond("Watching video...")
        else:
            await ctx.respond("Invalid URL!")
            
        response = search.youtube(url)
        await ctx.respond(response)
        
    @discord.user_command()
    async def greet(self, ctx, member: discord.Member):
        await ctx.respond(f'{ctx.author.mention} says hello to {member.mention}!')
        
        
    @discord.slash_command()
    async def imagine(self, ctx, first: str):
        prompt = [first]
        from features import imagine
        img_data = imagine(prompt)
        if img_data is None:
            await ctx.respond("An error occurred while generating the image.")
        else:
            buffer = BytesIO(img_data)
            buffer.seek(0)
            file = discord.File(buffer, filename="imagine.jpg")
            await ctx.respond(f"Imagine: {first}", file=file)

    @commands.Cog.listener() # Event listeners
    async def on_member_join(self, member): # This is called when a member joins the server
        await member.send('Welcome to hell')

    def cog_unload(self):
        self.conn.close()
        
def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(Cogs(bot)) # add the cog to the bot