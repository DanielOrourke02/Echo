<h1 align="center">Hi 👋, I'm Daniel Jones</h1>
<h3 align="center">I'm a passionate Python and C++ developer</h3>
<h3 align="center">Welcome To my github project!👋</h3>

# More about me and my projects

[📁 Active Projects](https://github.com/DanielJones02/Active-Projects)

# Echo Bot

A cool bot with lots and lots of commands and many different features. Scroll down to see the installation and the list of all the commands.

# MAJOR UPDATE COMMING SOON (BUG FIXES)

### todo

Add a GUI control dashboard

make code much neater and remove all DRY (dont repeat yourself)

add fertelizer (for plants to speed up process)

add more gambling games

Polish project, fix all bugs and release v4

# Installation

(first have python installled from the python website or micrisoft store)

1. `git clone https://github.com/DanielJones02/Echo` or `download the latest release`

2. `cd Echo`, clone into the directory.

3. Open config.json and do the following:

 - Add your bot token (required for the bot to work)

 - Add your user id for admin commands (required for config editing and reading from discord

 - add your bot invite link (scroll down for all the permissions needed) (optional)

4. for windows simply run `win-run.bat` and for linux do the following `chmod +x linux-run.sh` then `./linux-run.sh` (untested I tink those commands work). All requirements will be installed (you can disable auto installation by setting skip-installation to true)

<h3 align="left">Connect with me:</h3>
<p align="left">
</p>
<h3 align="left">Hire Me: https://discord.gg/kNWkT8xWg6 Or DM ME: mal023</h3>
</p>

# KNOWN BUGS

`Buttons` - Buttons will no longer work after a bot restart (ticket button and verify button)


## General Commands

| Command                   | Description                                      |
|---------------------------|--------------------------------------------------|
| `help`                    | Get help for commands.                           |
| `economy`                 | List economy commands.                           |
| `moderation`              | Get help for moderation commands (Admin only).   |
| `ping`                    | Get the bot's current latency.                   |
| `say <message>`           | Repeat a message.                                |
| `coinflip <heads/tails`   | Flip a coin.                                     |
| `avatar <@user>`          | Output a users avatar                            |
| `dice`                    | Roll a six-sided die.                            |
| `8ball <question>`        | Ask an 8ball a question.                         |
| `quote`                   | Get a daily quote from an API.                   |
| `qr <text/link>`          | Generate a QR code from a link.                  |
| `membercount`             | Get the member count of the server.              |
| `calculator <+-*/>`       | Perform basic calculations.                      |
| `joke`                    | Get a random joke.                               |
| `user_info <@user>        | Get info on a user                               |
| `server_info`             | Get the servers info                             |

## Economy Commands

| Command                  | Description                                           |
|--------------------------|-------------------------------------------------------|
| `balance`                | Checks your current bank and pocket balance.          |
| `baltop`                 | Displays the richest people leaderboard.              |
| `daily`                  | Claims your daily reward.                             |
| `shop`                   | Views available items in the shop.                    |
| `trade <@user> <item_id>`| Gives an item to a player.                            |
| `cosmetics`              | Lists available cosmetics and their prices.           |
| `buy <item_id>`          | Buys an item from the shop.                           |
| `sell <item_id>`         | Sells an item for its value.                          |
| `beg`                    | Beg for money.                                        |
| `hunt`                   | hunt for cosmetics and money. (with a bow)            |
| `dig`                    | Dig for cosmetics and money. (with a shovel)          |
| `scrap`                  | Find cosmetics and money.                             |
| `shoot <@user>`          | Shoot a user with a gun or a M4A1                     |
| `bomb <@user>`           | Bomb a user with C4                                   |
| `inventory`              | Lists items in your inventory.                        |
| `pay <amount>`           | Pay someone money.                                    |
| `deposit <amount/max`    | Deposit money into your bank (earns interest).        |
| `withdraw <amount>`      | Withdraw money from your bank.                        |
| `rob <@user>`            | Rob a user and potentially steal some of their money. |
| `plant <amount/max>`     | Plant crops to sell later at a profit.                |
| `harvest`                | Harvest your planted crops.                           |
| `craft <recipe_name>`    | Craft items.                                          |
| `recipes`                | Shows craftable items and required materials.         |
| `lottery`                | Participate in a lottery for a chance to win money.   |
| `gamble <amount>`        | Gamble your money with a 1/3 chance of winning.       |
| `blackjack <amount>`     | Play a cool interactive blackjacks game.              |
| `slots <amount>`         | Play slots with a small chance of winning big.        |

## Moderation Commands

| Command             | Description                                      |
|---------------------|--------------------------------------------------|
| `kick <@user> <reason>` | Kick a user from the server.                 |
| `ban <@user> <reason>`  | Ban a user from the server.                  |
| `mute <@user> <reason>` | Mute a user in the server.                   |
| `unmute <@user> <reason>` | Unmute a user in the server.               |
| `clear <amount>`        | Clear a specified number of messages in a channel. |
| `ticketpanel <message>` | Create a ticket panel for support.           |
| `setup-verify <role_name> <message>` | Set up a verification panel.    |
| `lockchannel`       | Lock a channel for a specified duration.         |
| `unlockchannel`     | Unlock a channel.                                |
| `lockserver`        | Lock the entire server for a specified duration. |
| `unlockserver`      | Unlock the entire server.                        |
| `config_view`       | Read config.json from discord (admin id only)    |
| `config_edit <varialbe> <new_value>` | Edit config.json from discord.  |

## Shop (ingame)

| Item   | Description                                | Cost  |
|--------|--------------------------------------------|-------|
| Silver | Store your money in silver                 | 1000  |
| Gold   | Store your money in gold                   | 10000 |


## Craftable Items (ingame)

| Item               | Ingredients                                  | Description                                      |
|--------------------|----------------------------------------------|--------------------------------------------------|
| Excalibur         | 2 guns, 1 mythical_sword                      | A powerful sword that only the one can handle    |
| M4A1              | 2 guns, 1 stick                               | Shoot down your enemies                          |
| 8_Incher          | 1 stick, 1 david4                             | A unique and 8 inch weapon                       |
| Complete_Gauntlet | 1 infinity, 1 leg.sword, 1 david4             | The most powerful item in the game               |
| C4                | 2 sulphur, 1 charcoal, 1 clock, 5 potatoes, 2 tech | C4 Bomb for bombing people                  |
| Poo               | 3 charcoal, 1 sulphur                         | Just poo                                         |
| Joint             | 1 roll, 1 weed                                | Get high asf                                     |

## Findable Items (ingame)

I call them 'cosmetics', but they are items you get from running: dig, hunt and scrap. These items can be used to craft items that sell for more e.g Joint, C4

| Item             | Description                     | Sell Value | Chance (%) |
|------------------|---------------------------------|------------|-------------|
| Rare Sword       | Rare Sword                      | 2500       | 25          |
| Legendary Sword  | Legendary Sword                 | 5000       | 15          |
| Mythical sword   | Mythical sword                  | 12500      | 5           |
| Shovel           | Shovel used for digging         | 1000       | 23          |
| Bow              | Bow used for hunting            | 1000       | 20          |
| Infinity Gauntlet| Infinity Gauntlet               | 30000      | 5           |
| David's 4th ball | David's 4th ball                | 25000      | 7           |
| Stick            | Stick                           | 15000      | 15          |
| Glock-18         | Glock-18                        | 8000       | 18          |
| Electronics      | Electronics                     | 1000       | 20          |
| Weed             | Weed                            | 5000       | 25          |
| Sulphur          | Sulphur                         | 500        | 40          |
| Charcoal         | Charcoal                        | 300        | 50          |
| Alarm Clock      | Alarm Clock                     | 700        | 30          |
| Roll             | Roll paper for weed             | 1500       | 30          |
| Potato           | Potato                          | 100        | 70          |



<h3 align="left">Connect with me:</h3>
<p align="left">
</p>
<h3 align="left">Hire Me: https://discord.gg/kNWkT8xWg6 Or DM ME: mal023</h3>
</p>

<div align="center">
  <img src="https://github.com/DanielJones02/Active-Projects/blob/main/images/Visual_Studio_Icon_2019.svg.png" width="48" height="48" alt="Visual Studio" />
  <img src="https://github.com/DanielJones02/Active-Projects/blob/main/images/python.png" alt="Python" />
  <img src="https://github.com/DanielJones02/Active-Projects/blob/main/images/html.png" alt="HTML" />
  <img src="https://github.com/DanielJones02/Active-Projects/blob/main/images/css.png" alt="CSS" />
  <img src="https://github.com/DanielJones02/Active-Projects/blob/main/images/C%2B%2B.png" alt="C++" />
  <img src="https://github.com/DanielJones02/Active-Projects/blob/main/images/linux.png" alt="Linux" />
</div>
