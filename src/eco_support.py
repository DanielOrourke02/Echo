

from utilities import *


# ALL OF THE MAIN FUNCTIONS FOR THE ECONOMY GAME


DATA_FILE = 'user_data.json'

user_bank_balances = {}  # Holds users' bank 

last_planting_time = {}

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
    "Potato": {"name": "Potato", "sell": 100, "chance": 70},
    "Electronics": {"name": "Electronics", "sell": 1000, "chance": 20},
    "David4": {"name": "David's 4th ball", "sell": 15000, "chance": 2},
    "infinity": {"name": "Infinity Gauntlet", "sell": 25000, "chance": 1}
}

craftables = {
    "Joint": {"name": "Weed rolled in paper", "sell": 10000},
    "C4": {"name": "C4 BOMB", "sell": 25000},
    "Excalibur": {"name": "The Excalibur", "sell": 16000},
    "M4A1": {"name": "Assault Rifle", "sell": 30000},
    "8_incher": {"name": "Long hard Stick", "sell": 40000},
    "Complete_Gauntlet": {"name": "Infinity  Gauntlet", "sell": 60000}
}


shop_items = {
    "working": {"name": "Working class slave (role)", "cost": 25000},
    "middle": {"name": "Middle class noob (role)", "cost": 50000},
    "upper": {"name": "Upper class elite (role)", "cost": 100000},
    "protagonist": {"name": "THE PROTAGONIST (role)", "cost": 500000}
}

role_colors = {
    "Working class slave": discord.Color.light_grey(),  # grey
    "Middle class noob": discord.Color.green(),         # green
    "Upper class elite": discord.Color.purple(),        # purple
    "THE PROTAGONIST": discord.Color.gold()             # gold/yellow
}


combined_items = {**cosmetics_items, **craftables}


crafting_recipes = {
    "Excalibur": {
        "Gun": 1,
        "Leg.sword": 1,
        "result": "Excalibur"  # A powerful sword
    },
    "M4A1": {
        "Gun": 2,
        "Stick": 1,
        "result": "M4A1"  # An advanced firearm
    },
    "8_incher": {
        "Stick": 1,
        "David4": 1,
        "result": "8_incher"  # A unique and humorous item
    },
    "Complete_Gauntlet": {
        "infinity": 1,
        "Leg.sword": 1,
        "David4": 1,
        "result": "Complete_Gauntlet"  # The most powerful item in the game
    }
}

# Adding the C4 recipe
crafting_recipes["C4"] = {
    "Sulphur": 2,
    "Charcoal": 1,
    "Duct_Tape": 3,
    "Alarm_Clock": 1,
    "Potato": 5,  # Because why not?
    "Electronics": 2,
    "result": "C4"  # The crafted item
}

# Adding the C4 recipe
crafting_recipes["Joint"] = {
    "paper/roll": 1,
    "weed": 1,
    "result": "Joint"  # The crafted item
}


# Create the file if it doesn't exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)

try:
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
        user_balances = data.get('user_balances', {})
        user_bank_balances = data.get('user_bank_balances', {})
        user_carrot_plantations = data.get('user_carrot_plantations', {})
except FileNotFoundError:
    user_balances = {}
    user_bank_balances = {}
    user_carrot_plantations = {}


async def assign_role_to_user(ctx, role_name):
    role = discord.utils.get(ctx.guild.roles, name=role_name)

    if role is None:
        # Determine the color for the new role
        role_color = role_colors.get(role_name, discord.Color.default())

        # Role not found, create it
        try:
            role = await ctx.guild.create_role(name=role_name, color=role_color)
        except discord.Forbidden:
            print(f"Bot does not have permission to create roles in the guild.")
            return
        except discord.HTTPException as e:
            print(f"Error creating role: {e}")
            return

    # Assign the role to the user
    await ctx.author.add_roles(role)


def save_user_data():
    with open(DATA_FILE, 'w') as f:
        json.dump({'user_balances': user_balances, 'user_bank_balances': user_bank_balances}, f)


def update_bank_interest(user_id):
    # Retrieve last interest update time for the user
    last_interest_update = user_bank_balances.get(f"{user_id}_last_interest_update", 0)

    # Calculate time difference since last update
    time_difference = time.time() - last_interest_update

    # If 24 hours have passed, apply interest 24 * 60 * 60 == 1 day/24 hours
    if time_difference >= 24 * 60 * 60:
        # Calculate interest amount (10% of current bank balance)
        interest_amount = int(get_bank_balance(user_id) * 0.10)

        # Cap the interest at whatever the max bank size is
        interest_amount = min(interest_amount, max_bank_size)

        # Update bank balance with interest
        update_bank_balance(user_id, interest_amount)

        # Update last interest update time
        user_bank_balances[f"{user_id}_last_interest_update"] = time.time()
        save_user_data()



def get_user_bank_balance(user_id):
    update_bank_interest(user_id)  # Update interest before returning balance
    return user_bank_balances.get(str(user_id), 0)


# Get the list of items in their inventory
def get_user_inventory(user_id):
    return user_balances.setdefault(f"{user_id}_inventory", [])


# Add items to their inventory
def add_item_to_inventory(user_id, item_name):
    inventory = get_user_inventory(user_id)
    inventory.append(item_name)
    user_balances[f"{user_id}_inventory"] = inventory
    save_user_data()  # Function to save data to file


# Remove items from their inventory
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


def can_beg(user_id):
    last_beg_time = user_balances.get(f"{user_id}_last_beg", 0)
    current_time = time.time()
    cooldown_remaining = current_time - last_beg_time

    #print(f"Last beg time: {last_beg_time}")
    #print(f"Current time: {current_time}")
    #print(f"Cooldown remaining: {cooldown_remaining}")

    return cooldown_remaining >= 30  # 30 seconds


def plant_carrots(user_id, amount):
    current_time = time.time()
    grow_duration = 3600 * 24  # 2 hours in seconds
    cost_per_carrot = 100
    total_cost = amount * cost_per_carrot

    # Update balance and record plantation details
    update_user_balance(user_id, -total_cost)  # Deducting the cost for planting
    user_carrot_plantations[str(user_id)] = [current_time + grow_duration, amount]
    save_user_data()


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


# Check if the user invoking the command is the admin
def is_admin(ctx):
    return ctx.author.id == config.get("ADMIN_ID")