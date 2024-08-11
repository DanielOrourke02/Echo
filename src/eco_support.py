"""
This file contains anything economy game related
e.g functions to load databases, access databases
"""

from utilities import *


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
    "god": {"name": "An item that only the gods can hold.", "sell": 15000000, "chance": 0.1},
    "infinity": {"name": "Infinity Gauntlet", "sell": 30000, "chance": 5},
    "david4": {"name": "David's 4th ball", "sell": 25000, "chance": 7},
    "stick": {"name": "Stick", "sell": 15000, "chance": 15},
    "gun": {"name": "Glock-18", "sell": 8000, "chance": 19},
    "tech": {"name": "Electronics", "sell": 1000, "chance": 25},
    "weed": {"name": "Weed", "sell": 5000, "chance": 30},
    "sulphur": {"name": "Sulphur", "sell": 500, "chance": 40},
    "charcoal": {"name": "Charcoal", "sell": 300, "chance": 50},
    "clock": {"name": "Alarm Clock", "sell": 700, "chance": 30},
    "roll": {"name": "Roll", "sell": 1500, "chance": 33},
    "potato": {"name": "Potato", "sell": 100, "chance": 65},
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
    "complete_gauntlet": {"name": "Infinity  Gauntlet", "sell": 60000},
    "glitch": {"name": "A glitch in the matrix", "sell": 50000000}
}


"""
If you are adding items to the shop do the following:

- Add your custom items
- Turn off bot
- delete items.db in the databases directory
- Start bot
- New items will be created along with the database
Enjoy!
"""
shop_items = {
    "silver": {"desc": "Bank full? Cant afford any gold? Buy some silver", "cost": 1000},
    "gold": {"desc": "Too rich? Banks full? Invest some money into gold. No interest, but its safe.", "cost": 10000},
    "shovel": {"desc": "Dig up treasure, find items and make money!", "cost": 1000},
    "bow": {"desc": "You can now hunt animals! Sell what you find and make money while doing it.", "cost": 1000},
    #"example": {"desc": "This is the item description!!", "cost": 1234},
}

combined_items = {**cosmetics_items, **craftables}

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
    },
    "glitch": {
        "god": 2,
        "result": "glitch" # rarest item in the game, if you have this your legit a god
    }
}

DATA_DB = 'src/databases/user_data.db'
COOLDOWN_DB = 'src/databases/cooldowns.db'
ITEMS_DB = 'src/databases/items.db'

# Create the databases and tables if they don't exist
def initialize_databases():
    # Initialize user data database
    conn = sqlite3.connect(DATA_DB)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_balances (
            user_id TEXT PRIMARY KEY,
            balance INTEGER DEFAULT 0,
            inventory TEXT DEFAULT '[]'
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_bank_balances (
            user_id TEXT PRIMARY KEY,
            balance INTEGER DEFAULT 0,
            last_interest_update REAL DEFAULT 0
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_carrot_plantations (
            user_id TEXT PRIMARY KEY,
            harvest_time REAL,
            amount INTEGER
        )
    ''')
    conn.commit()
    conn.close()

    # Initialize cooldowns database
    conn = sqlite3.connect(COOLDOWN_DB)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS cooldowns (
            user_id TEXT,
            action TEXT,
            last_action_time REAL,
            PRIMARY KEY (user_id, action)
        )
    ''')
    conn.commit()
    conn.close()
    
    conn = sqlite3.connect(ITEMS_DB)
    c = conn.cursor()
    # Create items table if not exists
    c.execute('''
        CREATE TABLE IF NOT EXISTS items (
            item_name TEXT PRIMARY KEY,
            desc TEXT,
            cost INTEGER
        )
    ''')

    # Insert data into items table
    for item_name, item_data in shop_items.items():
        c.execute('''
            INSERT OR IGNORE INTO items (item_name, desc, cost) VALUES (?, ?, ?)
        ''', (item_name, item_data['desc'], item_data['cost']))

    conn.commit()
    conn.close()

initialize_databases()


def load_cooldowns():
    conn = sqlite3.connect(COOLDOWN_DB)
    c = conn.cursor()
    c.execute('SELECT * FROM cooldowns')
    cooldowns = {f"{row[0]}_{row[1]}": row[2] for row in c.fetchall()}
    conn.close()
    return cooldowns


def load_user_plants():
    try:
        conn = sqlite3.connect(DATA_DB)
        c = conn.cursor()
        c.execute('SELECT * FROM user_carrot_plantations')
        user_plantations = {}
        for row in c.fetchall():
            user_id, harvest_time, amount_planted = row
            try:
                harvest_time = float(harvest_time)
                amount_planted = int(amount_planted)
                user_plantations[user_id] = (harvest_time, amount_planted)
            except ValueError as e:
                continue  # Skip this row if conversion fails
        conn.close()
        return user_plantations
    except Exception as e:
        print(f"Error loading user plantations: {e}")
        return {}  # Return an empty dictionary or handle the error as appropriate


def save_cooldowns(cooldowns):
    conn = sqlite3.connect(COOLDOWN_DB)
    c = conn.cursor()
    for key, value in cooldowns.items():
        user_id, action = key.split('_')
        c.execute('REPLACE INTO cooldowns (user_id, action, last_action_time) VALUES (?, ?, ?)', (user_id, action, value))
    conn.commit()
    conn.close()


def save_user_plants(user_plantations):
    try:
        conn = sqlite3.connect(DATA_DB)
        c = conn.cursor()
        c.execute('DELETE FROM user_carrot_plantations')
        for user_id, (harvest_time, amount_planted) in user_plantations.items():
            c.execute('INSERT INTO user_carrot_plantations (user_id, harvest_time, amount) VALUES (?, ?, ?)',
                      (user_id, harvest_time, amount_planted))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error saving user plantations: {e}")
  

def user_has_plants(user_id):
    user_plantations = load_user_plants()
    return str(user_id) in user_plantations


def update_plants():
    try:
        global user_carrot_plantations
        user_carrot_plantations = load_user_plants()
        
        if user_carrot_plantations is None:
            print("No user carrot plantations loaded.")  # Debug statement
            return  # Handle the case where data loading failed or returned None

        current_time = datetime.now().timestamp()
        
        for user_id, (harvest_time, amount) in user_carrot_plantations.items():
            time_left_seconds = max(0, harvest_time - current_time)
            if time_left_seconds <= 0:
                # Harvest the crops if the growth time has passed
                total_profit = amount * carrot_sell
                update_user_balance(user_id, total_profit)
                del user_carrot_plantations[user_id]  # Removing the plantation record
            else:
                # Update the time left in the percentage
                growth_percentage = min(100, ((growth_duration - time_left_seconds) / growth_duration) * 100)
                user_carrot_plantations[user_id] = (harvest_time, amount)  # Ensure consistency

        # Save the updated data
        save_user_plants(user_carrot_plantations)

    except Exception as e:
        print(f"Error updating plants: {e}")
        

def plant_carrots(user_id, amount):
    total_cost = amount * cost_per_carrot

    try:
        # Update balance and record plantation details
        update_user_balance(user_id, -total_cost)  # Deducting the cost for planting

        user_plantations = load_user_plants()

        # Store user's ID, planted amount, and time planted in a tuple
        user_plantations[str(user_id)] = (
            get_current_time(),
            amount
        )

        save_user_plants(user_plantations)
    except Exception as e:
        print(e)


def update_bank_interest(user_id, max_bank_size):
    conn = sqlite3.connect(DATA_DB)
    c = conn.cursor()
    
    c.execute('SELECT last_interest_update FROM user_bank_balances WHERE user_id = ?', (user_id,))
    last_interest_update = c.fetchone()
    last_interest_update = last_interest_update[0] if last_interest_update else 0
    
    time_difference = time.time() - last_interest_update

    if time_difference >= 24 * 60 * 60:
        bank_balance = get_user_bank_balance(user_id)
        interest_amount = int(bank_balance * 0.10)
        interest_amount = min(interest_amount, max_bank_size - bank_balance)
        
        update_bank_balance(user_id, interest_amount)
        
        c.execute('REPLACE INTO user_bank_balances (user_id, last_interest_update) VALUES (?, ?)', (user_id, time.time()))
        conn.commit()
    
    conn.close()


# Function to retrieve user inventory from the database
def get_user_inventory(user_id):
    try:
        conn = sqlite3.connect(DATA_DB)
        c = conn.cursor()
        c.execute('SELECT inventory FROM user_balances WHERE user_id = ?', (user_id,))
        inventory = c.fetchone()
        conn.close()
        return json.loads(inventory[0]) if inventory and inventory[0] else []
    except Exception as e:
        print(f"Error in get_user_inventory: {e}")
        return []


def add_item_to_inventory(user_id, item_name):
    try:
        inventory = get_user_inventory(user_id)
        inventory.append(item_name)
        inventory_json = json.dumps(inventory)
        
        conn = sqlite3.connect(DATA_DB)
        c = conn.cursor()

        # Check if the user already has an entry in user_balances
        c.execute('SELECT * FROM user_balances WHERE user_id = ?', (user_id,))
        existing_entry = c.fetchone()

        if existing_entry:
            # Update existing entry
            c.execute('UPDATE user_balances SET inventory = ? WHERE user_id = ?', (inventory_json, user_id))
        else:
            # Insert new entry
            c.execute('INSERT INTO user_balances (user_id, inventory) VALUES (?, ?)', (user_id, inventory_json))

        conn.commit()
        conn.close()

    except Exception as e:
        print(f"Error in add_item_to_inventory: {e}")


def remove_item_from_inventory(user_id, item_name):
    try:
        inventory = get_user_inventory(user_id)
        
        if item_name in inventory:
            inventory.remove(item_name)
            inventory_json = json.dumps(inventory)
            
            conn = sqlite3.connect(DATA_DB)
            c = conn.cursor()

            # Update only the inventory field using UPDATE statement
            c.execute('UPDATE user_balances SET inventory = ? WHERE user_id = ?', (inventory_json, user_id))
            conn.commit()
            conn.close()

    except Exception as e:
        print(f"Error removing item from inventory: {e}")


def get_user_balance(user_id):
    conn = sqlite3.connect(DATA_DB)
    c = conn.cursor()
    c.execute('SELECT balance FROM user_balances WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    if result is None:
        c.execute('INSERT INTO user_balances (user_id) VALUES (?)', (user_id,))
        conn.commit()
        result = (0,)
    conn.close()
    return result[0]


def get_user_bank_balance(user_id):
    conn = sqlite3.connect(DATA_DB)
    c = conn.cursor()
    c.execute('SELECT balance FROM user_bank_balances WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    if result is None:
        c.execute('INSERT INTO user_bank_balances (user_id) VALUES (?)', (user_id,))
        conn.commit()
        result = (0,)
    conn.close()
    return result[0]


def update_user_balance(user_id, amount):
    # Retrieve the current balance and inventory
    current_balance = get_user_balance(user_id)
    current_inventory = get_user_inventory(user_id)

    # Calculate the new balance
    new_balance = current_balance + amount

    # Open connection to the database
    conn = sqlite3.connect(DATA_DB)
    c = conn.cursor()

    try:
        # Use REPLACE INTO to update the user's balance and inventory
        c.execute('REPLACE INTO user_balances (user_id, balance, inventory) VALUES (?, ?, ?)',
                  (user_id, new_balance, json.dumps(current_inventory)))

        # Commit changes to the database
        conn.commit()
        
    except Exception as e:
        print(f"Error updating user balance: {e}")

    finally:
        # Close the database connection
        conn.close()


def update_bank_balance(user_id, amount):
    balance = get_user_bank_balance(user_id) + amount
    conn = sqlite3.connect(DATA_DB)
    c = conn.cursor()
    c.execute('REPLACE INTO user_bank_balances (user_id, balance) VALUES (?, ?)', (user_id, balance))
    conn.commit()
    conn.close()


def update_bank_balance(user_id, amount):
    balance = get_user_bank_balance(user_id) + amount
    conn = sqlite3.connect(DATA_DB)
    c = conn.cursor()
    c.execute('REPLACE INTO user_bank_balances (user_id, balance) VALUES (?, ?)', (user_id, balance))
    conn.commit()
    conn.close()


# COOLDOWN FUNCTIONS


def get_current_time():
    return time.time()


def get_cooldown_remaining(user_id, action, cooldowns, cooldown_duration):
    last_action_time = cooldowns.get(f"{user_id}_{action}", 0)
    current_time = get_current_time()
    return current_time - last_action_time


def can_perform_action(user_id, action, cooldown_duration):
    cooldowns = load_cooldowns()
    cooldown_remaining = get_cooldown_remaining(user_id, action, cooldowns, cooldown_duration)
    return cooldown_remaining >= cooldown_duration


def update_last_action_time(user_id, action):
    cooldowns = load_cooldowns()
    cooldowns[f"{user_id}_{action}"] = get_current_time()
    save_cooldowns(cooldowns)

def can_rob(user_id):
    return can_perform_action(user_id, "rob", 1 * 3600)  # 1 hour in seconds


def can_claim_daily(user_id):
    return can_perform_action(user_id, "claim", 24 * 3600)  # 24 hours in seconds


def can_dig(user_id):
    return can_perform_action(user_id, "dig", 1 * 60)


def can_hunt(user_id):
    return can_perform_action(user_id, "hunt", 1 * 60)


def can_scavenge(user_id):
    return can_perform_action(user_id, "scavenge", 1 * 60)


def can_beg(user_id):
    return can_perform_action(user_id, "beg", 15)  # 30 seconds


def can_plant(user_id):
    return can_perform_action(user_id, "plant", growth_duration * 3600)  # 12 hours in seconds


def set_last_claim_time(user_id):
    update_last_action_time(user_id, "claim")


def log_purchase(user_id, mode ,username , item_name, item_cost):
    if mode == 1:
        with open("src/databases/logs.txt", "a") as log_file:
            log_file.write(f"User {user_id} | {username} bought {item_name} for {item_cost} Credits.\n")
    elif mode == 0:
        with open("src/databases/logs.txt", "a") as log_file:
            log_file.write(f"User {user_id} | {username} sold {item_name} for {item_cost} Credits.\n")
