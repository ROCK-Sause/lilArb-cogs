import discord
import csv
from redbot.core import commands
import random

MAX_QUEUE_6MANS = 6
MAX_QUEUE_4MANS = 4
filename_4man 'PlayerData_4man.csv'
filename_6man = 'PlayerData_6man.csv' 
active_lobbies = [] #used to check if lobby is valid

class Arb6Mans(commands.Cog, name="Queue Commands"):
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot
        self.sixMans_queue = []  # 6mans = Orange
        self.fourMans_queue = [] # 4mans = Blue
        self.team_one = []
        self.team_two = []

    @commands.command(name='q', aliases=['queue'], description='Allows a user to join the queue.')
    async def queue(self, ctx):

        if ctx.channel.name != "4mans_queue" and ctx.channel.name != "6mans_queue":
            await ctx.send(f"No queueing in the {ctx.channel.name} channel.")
            return

        player = ctx.author

        if ctx.channel.name == "4mans_queue":
            if player in self.sixMans_queue:
                await ctx.send("You cannot queue in 6mans and 4mans at the same time.")
                return
            if player in self.fourMans_queue:
                await ctx.send(f'You are already in the 4mans queue!')
                return
            if len(self.fourMans_queue) == 6:
                return
            self.fourMans_queue.append(player)

            if len(self.fourMans_queue) < 6:
                blue_embed = discord.Embed(title=f'{len(self.fourMans_queue)} players are in the 4mans queue!')
                blue_embed.color = discord.Color.blue()
                blue_embed.description = f'{player.mention} has joined the queue.'
                await ctx.send(embed=blue_embed)

            if len(self.fourMans_queue) == MAX_QUEUE_4MANS:
                user = f'bear{random.randint(1, 1000)}'
                password = f'den{random.randint(1, 1000)}'
                credentials = f'**Here are your lobby details**\n\t__Username__: {user}\n\t__Password__: {password}'
                bluepop_embed = discord.Embed(title=f'4mans queue has been popped! {MAX_QUEUE_4MANS} players have queued up.')
                bluepop_embed.color = discord.Color.green()
                await ctx.send(embed=bluepop_embed)
                await ctx.send(" ".join(player.mention for player in self.fourMans_queue))
                for member in self.fourMans_queue:
                    await member.send(credentials)
                await self.create_lobby(ctx)
                await self.random_teams(ctx, self.fourMans_queue, MAX_QUEUE_4MANS)
                self.fourMans_queue = []
                new_queue = discord.Embed(title=f'4mans queue has been reset', color=discord.Color.blue())
                await ctx.send(embed=new_queue)

        if ctx.channel.name == "6mans_queue":
            if player in self.fourMans_queue:
                await ctx.send("You cannot queue in 6mans and 4mans at the same time.")
                return
            if player in self.sixMans_queue:
                await ctx.send(f'You are already in the 6mans queue!')
                return
            if len(self.sixMans_queue) == 6:
                return
            self.sixMans_queue.append(player)
            if len(self.sixMans_queue) < 6:
                orange_embed = discord.Embed(title=f'{len(self.sixMans_queue)} players are in the 6mans queue!')
                orange_embed.color = discord.Color.orange()
                orange_embed.description = f'{player.mention} has joined the queue.'
                await ctx.send(embed=orange_embed)

            if len(self.sixMans_queue) == MAX_QUEUE_6MANS:
                user = f'bear{random.randint(1, 1000)}'
                password = f'den{random.randint(1, 1000)}'
                credentials = f'**Here are your lobby details**\n\t__Username__: {user}\n\t__Password__: {password}'
                orangepop_embed = discord.Embed(title=f'Queue has been popped! {MAX_QUEUE_6MANS} players have queued up')
                orangepop_embed.color = discord.Color.green()
                await ctx.send(embed=orangepop_embed)
                await ctx.send(" ".join(player.mention for player in self.sixMans_queue))
                for member in self.sixMans_queue:
                    await member.send(credentials)

                await self.create_lobby(ctx)
                await self.random_teams(ctx, self.sixMans_queue, MAX_QUEUE_6MANS)

                self.sixMans_queue = []
                new_queue = discord.Embed(title=f'Orange queue has been reset', color=discord.Color.orange())
                await ctx.send(embed=new_queue)

    @commands.command(name="start", description="Creates a lobby if all players are ready to play.")
    async def manual_lobby(self, ctx):
        if ctx.channel.name != "4mans_queue" and ctx.channel.name != "6mans_queue":
            await ctx.send(f"Please go to correct channels (6mans_queue) or (4mans_queue).")
            return
        if ctx.channel.name == "4mans_queue":
            await self.create_lobby(ctx)
        if ctx.channel.name == "6mans_queue":
            await self.create_lobby(ctx)
        user = f'bear{random.randint(1, 1000)}'
        password = f'den{random.randint(1, 1000)}'
        credentials = f'**Here are your lobby details**\n\t__Username__: {user}\n\t__Password__: {password}'
        await ctx.author.send(credentials)

    @commands.command(name="dq", description="Lets the user leave the queue.")
    async def leave_lobby(self, ctx):
        if ctx.channel.name != "4mans_queue" and ctx.channel.name != "6mans_queue":
            await ctx.send(f"Please go to correct channels (6mans_queue) or (4mans_queue).")
            return
        player = ctx.author
        if ctx.channel.name == "4mans_queue":
            if player not in self.fourMans_queue:
                await ctx.send("You are not currently in the 4mans queue.")
                return
            self.fourMans_queue.remove(player)
            leave_embed = discord.Embed(title=f'{len(self.fourMans_queue)} players are in the 4mans queue')
            leave_embed.description = f'{player.mention} has left.'
            leave_embed.color = discord.Color.dark_red()
            await ctx.send(embed=leave_embed)

        if ctx.channel.name == "6mans_queue":
            if player not in self.sixMans_queue:
                await ctx.send("You are not currently in the 6mans queue.")
                return
            self.sixMans_queue.remove(player)
            leave_embed = discord.Embed(title=f'{len(self.sixMans_queue)} players are in the 6mans queue')
            leave_embed.description = f'{player.mention} has left.'
            leave_embed.color = discord.Color.dark_red()
            await ctx.send(embed=leave_embed)

    @commands.command(name="status", description="Displays current status of the queue.")
    async def queue_status(self, ctx):
        if ctx.channel.name != "4mans_queue" and ctx.channel.name != "6mans_queue":
            await ctx.send(f"Please go to correct channels (6mans_queue) or (4mans_queue).")
            return
        if ctx.channel.name == "4mans_queue":
            queue_embed = discord.Embed(title=f'{len(self.fourMans_queue)} players are in the 4mans queue')
            queue_embed.description = (" ".join(player.mention for player in self.fourMans_queue))
            queue_embed.color = discord.Color.blue()
            await ctx.send(embed=queue_embed)
            return
        if ctx.channel.name == "6mans_queue":
            queue_embed = discord.Embed(title=f'{len(self.sixMans_queue)} players are in the 6mans queue')
            queue_embed.description = (" ".join(player.mention for player in self.sixMans_queue))
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
        
        if ctx.channel.name == "4mans_queue":
            lobby = f'4Mans Lobby {args[0]}'
        if ctx.channel.name == "6mans_queue":
            lobby = f'6Mans Lobby {args[0]}'
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
        if member not in self.fourMans_queue and member not in self.sixMans_queue:
            await ctx.send(f"{member.display_name} is not in a queue right now.")
            return
        if member in self.fourMans_queue:
            self.fourMans_queue.remove(member)
            await ctx.send(f'{member.display_name} has been successfully removed from the blue queue.')
            return
        if member in self.sixMans_queue:
            self.sixMans_queue.remove(member)
            await ctx.send(f'{member.display_name} has been successfully removed from the orange queue.')

    @commands.command(hidden=True, name="addQueue")
    @commands.has_permissions(manage_channels=True)
    async def add_to_queue(self, ctx, member: discord.Member, queue):
        # You will need to set your own ID here
        if ctx.author.id != 256963559395819520:
            await ctx.send("You do not have permission to use this command.")
            return
        if queue == "4mans":
            self.fourMans_queue.append(member)
            print("Member successfully added to 4mans queue")
            return
        if queue == "6mans":
            self.sixMans_queue.append(member)
            print("Member successfully added to 6mans queue.")
            return

    @staticmethod
    async def create_lobby(ctx):
        server = ctx.guild
        lobby_num = str(random.randint(1, 1000)) 
        active_lobbies.append(lobby_num)                         
        #there is a 1/1000 chance there is the same lobby number and I will deal with it later
        ctx.channel.name
        if ctx.channel.name == "4mans_queue":
            lobby = f'4Mans Lobby {lobby_num}'
            lobby_VC = f'4Mans {lobby_num}'
            max_vc = 4
            user_vc = 2
        if ctx.channel.name == "6mans_queue":
            lobby = f'6Mans Lobby {lobby_num}'
            lobby_VC = f'6Mans {lobby_num}'
            max_vc = 6
            user_vc = 3
        category_channel = await server.create_category_channel(lobby)

        lobby_embed = discord.Embed(title=f'New Lobby has been created', type="rich", color=discord.Color.green())
        lobby_embed.add_field(name=f'Please join {lobby}', value=f"Have fun and don't suck", inline=True)
        await ctx.send(embed=lobby_embed)
        await category_channel.create_voice_channel(lobby_VC, user_limit=max_vc)
        await category_channel.create_voice_channel("Blue Team", user_limit=user_vc)
        await category_channel.create_voice_channel("Orange Team", user_limit=user_vc)

    async def random_teams(self, ctx, players, max_players):
        team_limit = int(max_players/2)
        self.team_one = random.sample(players, team_limit)
        for player in self.team_one:
            players.remove(player)
        self.team_two = players

        teams_embed = discord.Embed(color=discord.Color.green())
        teams_embed.add_field(name="**Blue Team**", value=f'{" ".join(player.name for player in self.team_one)}',
                              inline=False)
        teams_embed.add_field(name="**Orange Team**", value=f'{" ".join(player.name for player in self.team_two)}',
                              inline=False)
        await ctx.send(embed=teams_embed)

    @commands.command(name="report", description="Reports lobby as a win or loss, deletes lobby from active lobbies, adjustes elo of players, deletes lobby.")
    def report_lobby(command, self, active_lobbies, member: discord.Member):
        # Check if the command starts with ".report"
        if not command.startswith(".report"):
            return "Invalid command format. Please use .report <lobby number> <result>."
    
        # Split the command into parts
        parts = command.split()
        
        # Ensure the command has exactly 3 parts
        if len(parts) != 3:
            return "Invalid command format. Please use .report <lobby number> <result>."
        
        # Extract the lobby number and result
        _, lobby_number, result = parts
        
        # Validate the lobby number (should be a digit)
        if not lobby_number.isdigit():
            return "Invalid lobby number. It should be a numeric value."

        #Validate lobby number is an active lobby
        if not lobby_num in active_lobbies:
            return "Lobby number is not active. Please confirm the lobby number is correct."

        #remove lobby number from active_lobbies
        lobby_number = int(lobby_number)
        active_lobbies.remove(lobby_number)
        
        # Validate the result and store the value (should be 'w' for win)
        if result.lower() == 'w':
            is_winner = True
        elif result.lower() == 'l':
            is_winner = False
        else:
            return "Invalid result. Only 'w' for win or 'l' for loss is accepted."
        
        #Validate players are in correct database and add player and assign elo if necessary
        if ctx.channel.name == "6mans_queue":
            filename = filename_6mans
        if ctx.channel.name == "4mans_queue":
            filename = filename_4mans 
        update_players_in_csv(filename, team_one, team_two)
        #Determine author
        player = ctx.author
        #Determine what team is author on and did they win
        if player in team_one
            if is_winner
                winning_team = team_one
            else
                winning_team = team_two
        elif player in team_two
            if is_winner
                winning_team = team_two
            else
                winning_team = team_one
        else
            return "Player reporting not found on either team."
        #modify elo values appropiately 
        update_elo_after_match(filename, team_one, team_two, winning_team)
        
    def update_players_in_csv(filename, team_one, team_two):
        # Read existing players from the CSV file
        existing_players = {}
        with open(filename, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                existing_players[row['Player Name']] = row['ELO']
        
        # Combine team_one and team_two
        all_players = team_one + team_two
        
        # Check and add missing players
        new_entries = []
        for player in all_players:
            if player not in existing_players:
                # Assign a default ELO value (1500) for new players
                new_entries.append({"Player Name": player, "ELO": 1500})
        
        # Write back to the CSV file
        with open(filename, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["Player Name", "ELO"])
            
            # If the file is empty, write the header
            if file.tell() == 0:
                writer.writeheader()
            
            # Write new entries
            writer.writerows(new_entries)
        
    def update_elo_after_match(filename, team_one, team_two, winning_team):
        # Read the current ELO ratings
        players_elo = {}
        if os.path.exists(filename):
            with open(filename, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    players_elo[row['Player Name']] = int(row['ELO'])
        
        # Update ELO ratings based on match result
        if winning_team == "team_one":
            for player in team_one:
                if player in players_elo:
                    players_elo[player] += 10
            for player in team_two:
                if player in players_elo:
                    players_elo[player] -= 10
        elif winning_team == "team_two":
            for player in team_one:
                if player in players_elo:
                    players_elo[player] -= 10
            for player in team_two:
                if player in players_elo:
                    players_elo[player] += 10
    
    # Write the updated ELO ratings back to the CSV file
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["Player Name", "ELO"])
        writer.writeheader()
        for player, elo in players_elo.items():
            writer.writerow({"Player Name": player, "ELO": elo})

    @commands.command(name='rank-check', description='Allows a user check elo of any user.')
    def get_player_elo(filename, player_name):
        if ctx.channel.name == "6mans_queue":
            filename = filename_6mans
        if ctx.channel.name == "4mans_queue":
            filename = filename_4mans
        if os.path.exists(filename):
            with open(filename, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['Player Name'] == player_name:
                         print(f"{player_name}'s ELO is {row['ELO']}")
                        return
        print(f"{player_name} is not found in the leaderboards.")

    @commands.command(name='leaderboard', description='Allows a user to show top 10 players on leaderboard.')
    def get_top_10_players(filename):
        if ctx.channel.name == "6mans_queue":
            filename = filename_6mans
        if ctx.channel.name == "4mans_queue":
            filename = filename_4mans
        players_elo = []
        if os.path.exists(filename):
            with open(filename, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    players_elo.append({"Player Name": row['Player Name'], "ELO": int(row['ELO'])})
        
        # Sort the players by ELO in descending order and get the top 10
        top_10_players = sorted(players_elo, key=lambda x: x['ELO'], reverse=True)[:10]
        # Print the top 10 players
        print("Top 10 Players by ELO:")
        for player in top_10_players:
            print(f"{player['Player Name']}: {player['ELO']}")

