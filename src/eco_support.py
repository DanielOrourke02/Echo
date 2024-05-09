

from utilities import *


DATA_FILE = 'user_data.json'

COOLDOWN_FILE = 'cooldowns.json'

user_bank_balances = {}  # Holds users' bank 

last_planting_time = {}

robbery_cooldown = {}  # Dictionary to track cooldowns

lottery_pool = set()

required_participants = 5 # chance = code break

entry_fee = config.get('entry_fee')

refund_timer = config.get('lottery_cooldown') # seconds

daily_reward = config.get('daily_reward')

# List of all cosmetics
cosmetics_items = {
    # Swords
    "r.sword": {"name": "Rare Sword", "sell": 2500, "chance": 25},
    "leg.sword": {"name": "Legendary Sword", "sell": 5000, "chance": 15},
    "mythical_sword": {"name": "Mythical sword", "sell": 12500, "chance": 5},

    # Tools
    "shovel": {"name": "Shovel used for digging", "sell": 1000, "chance": 23},
    "bow": {"name": "Bow used for hunting", "sell": 1000, "chance": 20},

    # Other items (High to low chance)
    "infinity": {"name": "Infinity Gauntlet", "sell": 30000, "chance": 5},
    "david4": {"name": "David's 4th ball", "sell": 25000, "chance": 7},
    "stick": {"name": "Stick", "sell": 15000, "chance": 15},
    "gun": {"name": "Glock-18", "sell": 8000, "chance": 18},
    "tech": {"name": "Electronics", "sell": 1000, "chance": 20},
    "weed": {"name": "Weed", "sell": 5000, "chance": 30},
    "sulphur": {"name": "Sulphur", "sell": 500, "chance": 40},
    "charcoal": {"name": "Charcoal", "sell": 300, "chance": 50},
    "clock": {"name": "Alarm Clock", "sell": 700, "chance": 30},
    "roll": {"name": "Roll", "sell": 1500, "chance": 32},
    "potato": {"name": "Potato", "sell": 100, "chance": 70},
}


# List of all items you can craft
craftables = {
    "joint": {"name": "Weed rolled in paper", "sell": 10000},
    "poo": {"name": "Its poo made by the gods", "sell": 2000},
    "c4": {"name": "C4 BOMB", "sell": 25000},
    "excalibur": {"name": "The Excalibur", "sell": 35000},
    "m4a1": {"name": "Assault Rifle", "sell": 30000},
    "excalibur": {"name": "Excalibur", "sell": 30000},
    "8_incher": {"name": "Long hard Stick", "sell": 40000},
    "complete_gauntlet": {"name": "Infinity  Gauntlet", "sell": 60000}
}


shop_items = {
    "silver": {"name": "Silver, Store your money in silver", "cost": 1000},
    "gold": {"name": "Gold Store your money in gold", "cost": 10000},
    "shovel": {"name": "Buy a shovel for digging", "cost": 1000},
    "bow": {"name": "Buy a bow for hunting", "cost": 1000},
    "stove": {"name": "A stove used for cooing", "cost": 25000},
    "red": {"name": "Red phosphorus", "cost": 4000},
    "chemical": {"name": "Special Chemical", "cost": 4000},
}

combined_items = {**cosmetics_items, **craftables}

ABS_PATH = os.path.abspath(os.path.dirname(__file__))

# crafting recipes
crafting_recipes = {
    "excalibur": {
        "gun": 2,
        "mythical_sword": 1,
        "result": "excalibur"  # A powerful sword that only the one can handle
    },
    "m4a1": {
        "gun": 2,
        "stick": 1,
        "result": "m4a1"  # Shoot down your enemies
    },
    "8_incher": {
        "stick": 1,
        "david4": 1,
        "result": "8_incher"  # A unique and 8 inch weapon
    },
    "complete_gauntlet": {
        "infinity": 1,
        "leg.sword": 1,
        "david4": 1,
        "result": "complete_gauntlet"  # The most powerful item in the game
    },
    "c4": {
        "sulphur": 2,
        "charcoal": 1,
        "clock": 1,
        "potato": 5,  # Because why not?
        "tech": 2,
        "result": "c4" # C4 Bomb for bombing kids
    },
    "poo": {
        "charcoal": 3,
        "sulphur": 1,
        "result": "poo"
    },
    "joint": {
        "roll": 1,
        "weed": 1,
        "result": "joint" # Get high asf 
    }
}


# Create the file if it doesn't exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)

if not os.path.exists(COOLDOWN_FILE):
    with open(COOLDOWN_FILE, 'w') as f:
        json.dump({}, f)

def load_cooldowns():
    try:
        with open(COOLDOWN_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Create the file if it doesn't exist
        with open(COOLDOWN_FILE, 'w') as f:
            json.dump({}, f)
        return {}

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


def load_user_plants():
    try:
        with open('user_plants.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_cooldowns(cooldowns):
    with open(COOLDOWN_FILE, 'w') as f:
        json.dump(cooldowns, f)


def save_user_plants(data):
    with open('user_plants.json', 'w') as f:
        json.dump(data, f, indent=4)


def save_user_data():
    with open(DATA_FILE, 'w') as f:
        json.dump({'user_balances': user_balances, 'user_bank_balances': user_bank_balances}, f)


def user_has_plants(user_id):
    user_plantations = load_user_plants()
    return str(user_id) in user_plantations


def update_plants():
    global user_carrot_plantations
    loaded_data = load_user_plants()
    
    for user_id, plantation_data in loaded_data.items():
        current_time = datetime.now().timestamp()
        time_left_seconds = max(0, plantation_data[0] - current_time)
        if time_left_seconds <= 0:
            # Harvest the crops if the growth time has passed
            harvested_amount = plantation_data[1]
            total_profit = harvested_amount * carrot_sell
            update_user_balance(user_id, total_profit)
            del user_carrot_plantations[user_id]  # Removing the plantation record
        else:
            # Update the time left in the percentage
            growth_percentage = min(100, ((growth_duration - time_left_seconds) / growth_duration) * 100)
            user_carrot_plantations[user_id] = (current_time + growth_duration, plantation_data[1])

    # Save the updated data
    save_user_plants(user_carrot_plantations)


def update_bank_interest(user_id, max_bank_size):
    # Retrieve last interest update time for the user
    last_interest_update = user_bank_balances.get(f"{user_id}_last_interest_update", 0)

    # Calculate time difference since last update
    time_difference = time.time() - last_interest_update

    # If 24 hours have passed, apply interest 24 * 60 * 60 == 1 day/24 hours
    if time_difference >= 3:
        print("updated bank interest!")
        # Calculate interest amount (10% of current bank balance)
        bank_balance = get_bank_balance(user_id)
        interest_amount = int(bank_balance * 0.10)

        # Cap the interest at whatever the max bank size is
        interest_amount = min(interest_amount, max_bank_size - bank_balance)

        update_bank_balance(user_id, interest_amount)

        user_bank_balances[f"{user_id}_last_interest_update"] = time.time()
        save_user_data()
        

def get_user_bank_balance(user_id):
    update_bank_interest(user_id, max_bank_size)  # Update interest before returning balance
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


# COOLDOWN FUNCTIONS


def get_current_time():
    return time.time()


def get_cooldown_remaining(user_id, action, cooldowns, cooldown_duration):
    try:
        last_action_time = cooldowns.get(f"{user_id}_{action}", 0)
        current_time = get_current_time()

        return current_time - last_action_time
    except Exception as e:
        print(e)


def can_perform_action(user_id, action, cooldown_duration):
    cooldowns = load_cooldowns()
    cooldown_remaining = get_cooldown_remaining(user_id, action, cooldowns, cooldown_duration)
    return cooldown_remaining >= cooldown_duration


def update_last_action_time(user_id, action):
    try:
        cooldowns = load_cooldowns()
        cooldowns[f"{user_id}_{action}"] = get_current_time()

        save_cooldowns(cooldowns)
    except Exception as e:
        print(e)


def can_sell_meth(user_id):
    return can_perform_action(user_id, "sell", 1 * 3600)  # 1 hour in seconds


def can_rob(user_id):
    return can_perform_action(user_id, "rob", 1 * 3600)  # 1 hour in seconds


def can_claim_daily(user_id):
    return can_perform_action(user_id, "claim", 24 * 3600)  # 24 hours in seconds


def can_dig(user_id):
    return can_perform_action(user_id, "dig", 15 * 60)  # 15 minutes in seconds


def can_hunt(user_id):
    return can_perform_action(user_id, "hunt", 10 * 60)  # 10 minutes in seconds


def can_scavenge(user_id):
    return can_perform_action(user_id, "scavenge", 5 * 60)  # 5 minutes in seconds


def can_beg(user_id):
    return can_perform_action(user_id, "beg", 30)  # 30 seconds


def can_plant(user_id):
    return can_perform_action(user_id, "plant", growth_duration * 3600)  # 12 hours in seconds


def plant_carrots(user_id, amount):
    total_cost = amount * cost_per_carrot

    try:
        # Update balance and record plantation details
        update_user_balance(user_id, -total_cost)  # Deducting the cost for planting

        user_plantations = load_user_plants()

        # Store user's ID, planted amount, and time planted
        user_plantations[str(user_id)] = {
            'amount_planted': amount,
            'time_planted': get_current_time(),
        }

        save_user_plants(user_plantations)
    except Exception as e:
        print(e)


def set_last_claim_time(user_id):
    update_last_action_time(user_id, "claim")


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
