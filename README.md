<h1 align="center">Hi 👋, I'm Daniel Jones</h1>
<h3 align="center">I'm a passionate Python and C++ developer</h3>
<h3 align="center">Welcome To my github project!👋</h3>

# More about me and my projects

[📁 Active Projects](https://github.com/DanielJones02/Active-Projects)

# Echo Bot

Just a discord bot I made in python (discord.py library). It contains a large amount of commands and features that you can use with a very fun and addictive economy game!

# DISCLAIMER: This is in beta, there are still many bugs and updates to fix and to release.

# bot probably DOES NOT WORK AS OF THIS MOMMENT

# Installation

1. `git clone https://github.com/DanielJones02/Echo` or download the latest release

2. IMPORTANT: add your discord token, weather api AND your user id:

Locations
- main.py - add your bot token at the bottom (ESSENTIAL

- economy.py - add your PATH for the the cogs directory there (ESSENTIAL)

- cogs/libs.py - Line 22, add your USER ID there (ESSENTIAL 4 ADMIN COMMANDS)

- cogs/other.py - Line 39, add your weather api key (not essential but $weather wont work)

2. run main.py `python main.py` or `python3 main.py` for linux users. Requirements will auto be installed. Make sure you have python 3.12 installed with pip 3.12.

3. You're finished! Your bot should ne running smoothly now.

# KNOWN BUGS

Economy game - Restarting the bot while users have crops planted WILL wipe all data of planted crops (users will loose all the crops they planted)

## General Commands

| Command                | Description                                   |
|------------------------|-----------------------------------------------|
| `help`                 | Outputs a list of available commands.         |
| `economy`              | Lists economy-related games and features.     |
| `games`                | Lists games you can play.                     |
| `ping`                 | Displays the bot's latency.                   |
| `say <message>`        | Makes the bot repeat the specified message.   |
| `membercount`          | Shows the current guild member count.         |
| `coinflip <heads/tails>` | Initiates a 50/50 coin flip.                 |
| `invite`               | Provides a bot invite link.                   |
| `nuke`                 | Nukes the channel in which the command is used. |
| `nuke_everything`      | Nukes all channels in the guild.              |
| `delete`               | Deletes all channels in the guild.            |
| `clear <amount>`       | Deletes a specified number of messages.       |
| `inventory`            | Checks your inventory.                        |
| `qr <text/link>`       | Generates a QR code from the given text or link. |
| `weather <location>`   | Provides current weather information for a specified location. |
| `ticket`               | Opens a ticket panel.                         |
| `delete`               | Deletes a ticket.                             |
| `add`                  | Adds a user to a ticket.                      |
| `remove`               | Removes a user from a ticket.                 |

## Economy Commands

| Command                  | Description                                           |
|--------------------------|-------------------------------------------------------|
| `bal`                    | Checks your current bank and pocket balance.          |
| `baltop`                 | Displays the richest people leaderboard.              |
| `daily`                  | Claims your daily reward.                             |
| `gamble <amount>`        | Gambles your money with a 50/50 chance of doubling it. |
| `shop`                   | Views available items in the shop.                    |
| `cosmetics`              | Lists available cosmetics and their prices.           |
| `buy <item_id>`          | Buys an item from the shop.                           |
| `sell <item_id>`         | Sells an item for its value.                          |
| `beg`                    | Beg for money.                                        |
| `scrap`                  | Find cosmetics and money.                             |
| `inventory`              | Lists items in your inventory.                        |
| `lottery`                | Participate in a lottery for a chance to win money.   |
| `pay <amount>`           | Pay someone money.                                    |
| `deposit`                | Deposit money into your bank (earns interest).        |
| `withdraw`               | Withdraw money from your bank.                        |
| `rob <@user>`            | Rob a user and potentially steal some of their money. |
| `plant <amount/max>`     | Plant crops to sell later at a profit.                |
| `harvest`                | Harvest your planted crops.                           |
| `craft <recipe_name>`    | Craft items.                                          |
| `recipes`                | Shows craftable items and required materials.         |
