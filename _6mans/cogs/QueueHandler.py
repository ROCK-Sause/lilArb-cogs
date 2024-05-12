import discord
from discord.ext import commands
import random


MAX_QUEUE = 6


def setup(bot):
    bot.add_cog(QueueHandler(bot))


class QueueHandler(commands.Cog, name="Queue Commands"):
    def __init__(self, bot):
        self.bot = bot
        self.orange_queue = []
        self.blue_queue = []
        self.team_one = []
        self.team_two = []

    @commands.command(name='q', aliases=['queue'], description='Allows a user to join the queue.')
    async def queue(self, ctx):

        if ctx.channel.name != "blue_queue" and ctx.channel.name != "orange_queue":
            await ctx.send(f"No queueing in the {ctx.channel.name} channel.")
            return

        player = ctx.author

        if ctx.channel.name == "blue_queue":
            if player in self.orange_queue:
                await ctx.send("You cannot queue in orange and blue at the same time.")
                return
            if player in self.blue_queue:
                await ctx.send(f'You are already in the blue queue!')
                return
            if len(self.blue_queue) == 6:
                return
            self.blue_queue.append(player)

            if len(self.blue_queue) < 6:
                blue_embed = discord.Embed(title=f'{len(self.blue_queue)} players are in the blue queue!')
                blue_embed.color = discord.Color.blue()
                blue_embed.description = f'{player.mention} has joined the queue.'
                await ctx.send(embed=blue_embed)

            if len(self.blue_queue) == MAX_QUEUE:
                user = random.randint(1, 1000)
                password = random.randint(1, 1000)
                credentials = f'**Here are your lobby details**\n\t__Username__:{user}\n\t__Password__:{password}'
                bluepop_embed = discord.Embed(title=f'Blue queue has been popped! {MAX_QUEUE} players have queued up.')
                bluepop_embed.color = discord.Color.green()
                await ctx.send(embed=bluepop_embed)
                await ctx.send(" ".join(player.mention for player in self.blue_queue))
                for member in self.blue_queue:
                    await member.send(credentials)
                await self.create_lobby(ctx)
                await self.random_teams(ctx, self.blue_queue)
                self.blue_queue = []
                new_queue = discord.Embed(title=f'Blue queue has been reset', color=discord.Color.blue())
                await ctx.send(embed=new_queue)

        if ctx.channel.name == "orange_queue":
            if player in self.blue_queue:
                await ctx.send("You cannot queue in orange and blue at the same time.")
                return
            if player in self.orange_queue:
                await ctx.send(f'You are already in the orange queue!')
                return
            if len(self.orange_queue) == 6:
                return
            self.orange_queue.append(player)
            if len(self.orange_queue) < 6:
                orange_embed = discord.Embed(title=f'{len(self.orange_queue)} players are in the orange queue!')
                orange_embed.color = discord.Color.orange()
                orange_embed.description = f'{player.mention} has joined the queue.'
                await ctx.send(embed=orange_embed)

            if len(self.orange_queue) == MAX_QUEUE:
                user = random.randint(1, 1000)
                password = random.randint(1, 1000)
                credentials = f'**Here are your lobby details**\n\t__Username__:{user}\n\t__Password__:{password}'
                orangepop_embed = discord.Embed(title=f'Queue has been popped! {MAX_QUEUE} players have queued up')
                orangepop_embed.color = discord.Color.green()
                await ctx.send(embed=orangepop_embed)
                await ctx.send(" ".join(player.mention for player in self.orange_queue))
                for member in self.orange_queue:
                    await member.send(credentials)

                await self.create_lobby(ctx)
                await self.random_teams(ctx, self.orange_queue)

                self.orange_queue = []
                new_queue = discord.Embed(title=f'Orange queue has been reset', color=discord.Color.orange())
                await ctx.send(embed=new_queue)

    @commands.command(name="lobby", description="Creates a lobby if 6 players are ready to play.")
    async def manual_lobby(self, ctx):
        if ctx.channel.name != "blue_queue" and ctx.channel.name != "orange_queue":
            await ctx.send(f"Please go to correct channels (orange_queue) or (blue_queue).")
            return
        await self.create_lobby(ctx)
        user = random.randint(1, 1000)
        password = random.randint(1,1000)
        credentials = f'**Here are your lobby details**\n\t__Username__:{user}\n\t__Password__:{password}'
        await ctx.author.send(credentials)

    @commands.command(name="leave", description="Lets the user leave the queue.")
    async def leave_lobby(self, ctx):
        if ctx.channel.name != "blue_queue" and ctx.channel.name != "orange_queue":
            await ctx.send(f"Please go to correct channels (orange_queue) or (blue_queue).")
            return
        player = ctx.author
        if ctx.channel.name == "blue_queue":
            if player not in self.blue_queue:
                await ctx.send("You are not currently in the blue queue.")
                return
            self.blue_queue.remove(player)
            leave_embed = discord.Embed(title=f'{len(self.blue_queue)} players are in the blue queue')
            leave_embed.description = f'{player.mention} has left.'
            leave_embed.color = discord.Color.dark_red()
            await ctx.send(embed=leave_embed)

        if ctx.channel.name == "orange_queue":
            if player not in self.orange_queue:
                await ctx.send("You are not currently in the orange queue.")
                return
            self.orange_queue.remove(player)
            leave_embed = discord.Embed(title=f'{len(self.orange_queue)} players are in the orange queue')
            leave_embed.description = f'{player.mention} has left.'
            leave_embed.color = discord.Color.dark_red()
            await ctx.send(embed=leave_embed)

    @commands.command(name="status", description="Displays current status of the queue.")
    async def queue_status(self, ctx):
        if ctx.channel.name != "blue_queue" and ctx.channel.name != "orange_queue":
            await ctx.send(f"Please go to correct channels (orange_queue) or (blue_queue).")
            return
        if ctx.channel.name == "blue_queue":
            queue_embed = discord.Embed(title=f'{len(self.blue_queue)} players are in the blue queue')
            queue_embed.description = (" ".join(player.mention for player in self.blue_queue))
            queue_embed.color = discord.Color.blue()
            await ctx.send(embed=queue_embed)
            return
        if ctx.channel.name == "orange_queue":
            queue_embed = discord.Embed(title=f'{len(self.orange_queue)} players are in the orange queue')
            queue_embed.description = (" ".join(player.mention for player in self.orange_queue))
            queue_embed.color = discord.Color.orange()
            await ctx.send(embed=queue_embed)
            return

    @commands.command(name="delete", description="Deletes a lobby that was created previously.", hidden=True)
    @commands.has_permissions(manage_channels=True)
    async def delete_lobby(self, ctx, *args):
        server = ctx.guild
        await ctx.channel.purge(limit=1)
        if len(args) == 0:
            await ctx.send("You did not specify a room.")
            return
        try:
            int(args[0])
        except ValueError:
            await ctx.send("That is not a valid lobby number.")
            return

        lobby = f'Lobby {args[0]}'
        for category in server.categories:
            if category.name == lobby:
                for voice_channel in category.voice_channels:
                    await voice_channel.delete()
                await category.delete()
                print(f'\n{ctx.author} deleted {lobby}.\n')
                return
        await ctx.send(f'Could not find {lobby}. My b.')

    @commands.command(name="remove", description="Removes a player from a queue", hidden=True)
    @commands.has_permissions(manage_channels=True)
    async def remove_from_queue(self, ctx, *, member: discord.Member):
        if member not in self.blue_queue and member not in self.orange_queue:
            await ctx.send(f"{member.display_name} is not in a queue right now.")
            return
        if member in self.blue_queue:
            self.blue_queue.remove(member)
            await ctx.send(f'{member.display_name} has been successfully removed from the blue queue.')
            return
        if member in self.orange_queue:
            self.orange_queue.remove(member)
            await ctx.send(f'{member.display_name} has been successfully removed from the orange queue.')

    @commands.command(hidden=True, name="addQueue")
    @commands.has_permissions(manage_channels=True)
    async def add_to_queue(self, ctx, member: discord.Member, queue):
        # You will need to set your own ID here
        if ctx.author.id != 256963559395819520:
            await ctx.send("You do not have permission to use this command.")
            return
        if queue == "blue":
            self.blue_queue.append(member)
            print("Member successfully added to blue queue")
            return
        if queue == "orange":
            self.orange_queue.append(member)
            print("Member successfully added to orange queue.")
            return

    @staticmethod
    async def create_lobby(ctx):
        server = ctx.guild
        lobby_num = str(random.randint(1, 1000))
        lobby = f'Lobby {lobby_num}'
        category_channel = await server.create_category_channel(lobby)

        lobby_embed = discord.Embed(title=f'New Lobby has been created', type="rich", color=discord.Color.green())
        lobby_embed.add_field(name=f'Please join {lobby}', value=f"Have fun and don't suck", inline=True)
        await ctx.send(embed=lobby_embed)
        await category_channel.create_voice_channel(lobby_num, user_limit=6)
        await category_channel.create_voice_channel("Team 1", user_limit=3)
        await category_channel.create_voice_channel("Team 2", user_limit=3)

    async def random_teams(self, ctx, players):
        self.team_one = random.sample(players, 3)
        for player in self.team_one:
            players.remove(player)
        self.team_two = players

        teams_embed = discord.Embed(color=discord.Color.green())
        teams_embed.add_field(name="**Team 1**", value=f'{" ".join(player.name for player in self.team_one)}',
                              inline=False)
        teams_embed.add_field(name="**Team 2**", value=f'{" ".join(player.name for player in self.team_two)}',
                              inline=False)
        await ctx.send(embed=teams_embed)


