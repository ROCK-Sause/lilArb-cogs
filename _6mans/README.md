# Private Six Mans Bot
A 6mans type bot written using the discord.py wrapper.
The purpose is to create six-mans queues for Rocket League and handle auto assigning teams.
The bot was custom built for a friend's server so commands in here relate specifically to channels found in that server.
The queueing feature works as two seperate queues using #blue_queue and #orange_queue channels.



## Installation 
1. Clone repository ```git clone https://github.com/dch0017/Python6Mans.git```
2. Install requirements ```pip3 install -r requirements.txt```
3. Run the bot.py. You will encounter an error, this is it creating the config.ini file in the directory.
4. Enter your prefix and bot token in the config.ini file.
5. Run the bot.py

## How It Works
Players add themselves to a queue for a game using the !q command in the correct channels. Once a queue has reached 6 players it will 'pop'. The players will be notified that the queue has popped with a mention and will receive DM's with a username and password for a rocket league lobby. The bot will then create a lobby category and two team voice channels. Team's will then be auto selected and players will be told to join the lobby. The queue will then be reset.

## Current Features
- Queue Control
- Auto assigning teams
- Creation and deletion of Discord voice channels for teams


## Commands

__**Standard Commands**__

All commands must be done in the correct #blue_queue or #orange_queue channels.

*!q*

- This will add the player that used the command to the queue corresponding to the channel command was called in. Players cannot queue in both the blue and orange queues simultaneously.

*!lobby*

- This creates a lobby channel and two team voice channels.

*!leave*

- This lets the players leave the queue if they are currently in.

*!status*

- Shows the current status of the queue corresponding to the channel command was called in.


__**Admin Commands**__

On top of all standard commands, admins have access to a few extra commands.

*!delete [lobby number]*

- This will delete the lobby and two corresponding Team channels with it.

  - Example: !delete 247

*!clearChat [number]*

- The [number] after the command is optional, if none is given a standard 5 messages will be deleted.

  - Example: !clearChat

  - Example2: !clearChat 100

*!remove [@player]*

- This command will find and remove a player from a queue.

  - Example: !remove @ToastyDZ#2727

