<h1 align="center">Hi 👋, I'm Daniel Jones</h1>
<h3 align="center">I'm a passionate Python and C++ developer</h3>
<h3 align="center">Welcome To my github project!👋</h3>

# More about me and my projects

[📁 Active Projects](https://github.com/DanielJones02/Active-Projects)

# Echo Bot

A cool bot with lots and lots of commands and many different features. Scroll down to see the installation and the list of all the commands.

# MAJOR UPDATE COMMING SOON (BUG FIXES)

### todo

save planted crops to a json file

make code much neater and remove all DRY (dont repeat yourself)

fix embedding

debug code

make code more flexible and robust

add unmute command

# Installation

1. `git clone https://github.com/DanielJones02/Echo` or download the latest release

2. `cd Echo`

3. Open config.json and do the following:

 - Add your bot token

 - Add your user id for admin commands

 - add your bot invite link (scroll down for all the permissions needed

4. for windows simply run `win-run.bat` and for linux do the following `chmod +x linux-run.sh` then `./linux-run.sh` (untested I tink those commands work). All requirements will be installed (you can disable this by setting skip-installation to true)

# KNOWN BUGS

`Economy game` - Restarting the bot while users have crops planted WILL wipe all data of planted crops (users will loose all the crops they planted)

`Buttons` - Buttons will no longer work after a bot restart (ticket button and verify button)

`json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)` - Just delete whatever json file is erroring (only happens with empty json files)


## General Commands

| Command                   | Description                                      |
|---------------------------|--------------------------------------------------|
| `help`                    | Get help for commands.                           |
| `economy`                 | List economy commands.                           |
| `moderation`              | Get help for moderation commands (Admin only).   |
| `ping`                    | Get the bot's current latency.                   |
| `say <message>`           | Repeat a message.                                |
| `coinflip`                | Flip a coin.                                     |
| `avatar`                  | Output a users avatar                            |
| `dice`                    | Roll a six-sided die.                            |
| `dailyquote`              | Get a daily quote from an API.                   |
| `qr <text/link>`          | Generate a QR code from a link.                  |
| `membercount`             | Get the member count of the server.              |
| `calculator`              | Perform basic calculations.                      |
| `joke`                    | Get a random joke.                               |
| `user_info`               | Get info on a user                               |
| `server_info`             | Get the servers info                             |

## Economy Commands

| Command                  | Description                                           |
|--------------------------|-------------------------------------------------------|
| `balance`                | Checks your current bank and pocket balance.          |
| `baltop`                 | Displays the richest people leaderboard.              |
| `daily`                  | Claims your daily reward.                             |
| `gamble <amount>`        | Gambles your money with a 1/3 chance of winning.      |
| `shop`                   | Views available items in the shop.                    |
| `cosmetics`              | Lists available cosmetics and their prices.           |
| `buy <item_id>`          | Buys an item from the shop.                           |
| `sell <item_id>`         | Sells an item for its value.                          |
| `beg`                    | Beg for money.                                        |
| `hunt`                    | hunt for cosmetics and money. (with a bow)           |
| `dig`                    | Dig for cosmetics and money. (with a shovel)          |
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

## Moderation Commands

| Command             | Description                                      |
|---------------------|--------------------------------------------------|
| `kick`              | Kick a user from the server.                     |
| `ban`               | Ban a user from the server.                      |
| `mute`              | Mute a user in the server.                       |
| `clear`             | Clear a specified number of messages in a channel. |
| `ticketpanel`       | Create a ticket panel for support.              |
| `setup-verify`      | Set up a verification panel.                     |
| `lockchannel`       | Lock a channel for a specified duration.         |
| `unlockchannel`     | Unlock a channel.                                |
| `lockserver`        | Lock the entire server for a specified duration. |
| `unlockserver`      | Unlock the entire server.                        |

