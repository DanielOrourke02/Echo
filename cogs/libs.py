

from colorama import Fore
from time import ctime

import discord
import asyncio
import random
import time
import json
import sys
import os

sys.path.append(os.getcwd())


t = f"{Fore.LIGHTYELLOW_EX}{ctime()}{Fore.RESET}"

DATA_FILE = 'user_data.json'

user_bank_balances = {}  # Holds users' bank 

cosmetics_items = {
    "C.sword": {"name": "Common Sword", "sell": 1000, "chance": 50},
    "Un.sword": {"name": "Uncommon Sword", "sell": 1500, "chance": 30},
    "paper/roll": {"name": "Roll paper for weed", "sell": 1500, "chance": 30},
    "R.sword": {"name": "Rare Sword", "sell": 2500, "chance": 25},
    "weed": {"name": "Weed", "sell": 5000, "chance": 25},
    "Leg.sword": {"name": "Legendary Sword", "sell": 5000, "chance": 15},
    "Gun": {"name": "Glock-18", "sell": 8000, "chance": 15},
    "Stick": {"name": "Dildo", "sell": 10000, "chance": 10},
    "Sulphur": {"name": "Sulphur", "sell": 500, "chance": 40},
    "Charcoal": {"name": "Charcoal", "sell": 300, "chance": 50},
    "Duct_Tape": {"name": "Duct Tape", "sell": 200, "chance": 60},
    "Alarm_Clock": {"name": "Alarm Clock", "sell": 700, "chance": 30},
    "Potato": {"name": "Potato", "sell": 100, "chance": 70},  # For a humorous touch
    "Electronics": {"name": "Electronics", "sell": 1000, "chance": 20},
    "David4": {"name": "David's 4th ball", "sell": 15000, "chance": 2},
    "infinity": {"name": "Infinity Gauntlet", "sell": 25000, "chance": 1}
}

craftables = {
    "Joint": {"name": "Weed rolled in paper", "sell": 10000},
    "C4": {"name": "C4 BOMB", "sell": 25000},
    "Excalibur": {"name": "The Excalibur", "sell": 16000},
    "Assault_Rifle": {"name": "Assault Rifle", "sell": 23000},
    "Hell_Stick": {"name": "Stick of hell", "sell": 30000},
    "Infinity_Gauntlet": {"name": "Infinity  Gauntlet", "sell": 60000}
}

shop_items = {
    "mute1d": {"name": "Mute someone (1d)", "cost": 100000},
    "mute15m": {"name": "Mute someone (15mins)", "cost": 50000},
    "mute10m": {"name": "Mute someone (10mins)", "cost": 35000},
    "mute5m": {"name": "Mute someone (5mins)", "cost": 25000}
}

combined_items = {**cosmetics_items, **craftables}

# Create the file if it doesn't exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)

# Load user data from the file
try:
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
        user_balances = data.get('user_balances', {})
        user_bank_balances = data.get('user_bank_balances', {})
except (FileNotFoundError, json.decoder.JSONDecodeError):
    user_balances = {}
    user_bank_balances = {}

def message_log(ctx, command, extra = None):
    log_text = f"{t}{Fore.CYAN} | ${command} {extra} | {ctx.channel} | Executed by {ctx.author}{Fore.RESET}"
    print(log_text)

def save_user_data():
    with open(DATA_FILE, 'w') as f:
        json.dump({'user_balances': user_balances, 'user_bank_balances': user_bank_balances}, f)

def update_bank_interest(user_id):
    # Retrieve last interest update time for the user
    last_interest_update = user_bank_balances.get(f"{user_id}_last_interest_update", 0)

    # Calculate time difference since last update
    time_difference = time.time() - last_interest_update

    # If 24 hours have passed, apply interest
    if time_difference >= 24 * 60 * 60:
        # Calculate interest amount (10% of current bank balance)
        interest_amount = int(get_bank_balance(user_id) * 0.10)

        # Update bank balance with interest
        update_bank_balance(user_id, interest_amount)

        # Update last interest update time
        user_bank_balances[f"{user_id}_last_interest_update"] = time.time()
        save_user_data()

def get_user_bank_balance(user_id):
    update_bank_interest(user_id)  # Update interest before returning balance
    return user_bank_balances.get(str(user_id), 0)

    # Retrieve the bank balance for the user
    return user_bank_balances.get(str(user_id), 0)


def get_user_inventory(user_id):
    return user_balances.setdefault(f"{user_id}_inventory", [])


def add_item_to_inventory(user_id, item_name):
    inventory = get_user_inventory(user_id)
    inventory.append(item_name)
    user_balances[f"{user_id}_inventory"] = inventory
    save_user_data()  # Function to save data to file


def remove_item_from_inventory(user_id, item_name):
    inventory = get_user_inventory(user_id)
    if item_name in inventory:
        inventory.remove(item_name)
        user_balances[f"{user_id}_inventory"] = inventory
        save_user_data()  # Function to save data to file


def get_user_balance(user_id):
    return user_balances.get(str(user_id), 0)


def update_user_balance(user_id, amount):
    user_balances[str(user_id)] = get_user_balance(user_id) + amount
    save_user_data()


def get_bank_balance(user_id):
    return user_bank_balances.get(str(user_id), 0)

def update_bank_balance(user_id, amount):
    user_bank_balances[str(user_id)] = get_bank_balance(user_id) + amount
    save_user_data()


def can_claim_daily(user_id):
    last_claim_time = user_balances.get(f"{user_id}_last_claim", 0)
    current_time = time.time()
    cooldown_remaining = current_time - last_claim_time

    #print(f"Last scavenge time: {last_claim_time}")
    #print(f"Current time: {current_time}")
    #print(f"Cooldown remaining: {cooldown_remaining}")

    return cooldown_remaining >= 24 * 3600  # 24 hours in seconds

def can_scavenge(user_id):
    last_scavenge_time = user_balances.get(f"{user_id}_last_scavenge", 0)
    current_time = time.time()
    cooldown_remaining = current_time - last_scavenge_time

    #print(f"Last scavenge time: {last_scavenge_time}")
    #print(f"Current time: {current_time}")
    #print(f"Cooldown remaining: {cooldown_remaining}")

    return cooldown_remaining >= 5 * 60  # 5 minutes in seconds

def can_fish(user_id):
    last_fishing_time = user_balances.get(f"{user_id}_last_fishing", 0)
    current_time = time.time()
    cooldown_remaining = current_time - last_fishing_time

    # print(f"Last fishing time: {last_fishing_time}")
    # print(f"Current time: {current_time}")
    # print(f"Cooldown remaining: {cooldown_remaining}")

    return cooldown_remaining >= 5 * 60  # 5 minutes in seconds


def can_beg(user_id):
    last_beg_time = user_balances.get(f"{user_id}_last_beg", 0)
    current_time = time.time()
    cooldown_remaining = current_time - last_beg_time

    #print(f"Last beg time: {last_beg_time}")
    #print(f"Current time: {current_time}")
    #print(f"Cooldown remaining: {cooldown_remaining}")

    return cooldown_remaining >= 30  # 30 seconds

def set_last_claim_time(user_id):
    user_balances[f"{user_id}_last_claim"] = time.time()
    save_user_data()

def log_purchase(user_id, mode ,username , item_name, item_cost):
    if mode == 1:
        with open("logs.txt", "a") as log_file:
            log_file.write(f"User {user_id} | {username} bought {item_name} for {item_cost} coins.\n")
    elif mode == 0:
        with open("logs.txt", "a") as log_file:
            log_file.write(f"User {user_id} | {username} sold {item_name} for {item_cost} coins.\n")

def log_sell(user_id, username , item_name, item_cost):
    with open("sell_log.txt", "a") as log_file:
        log_file.write(f"User {user_id} | {username} sell {item_name} for {item_cost} coins.\n")
