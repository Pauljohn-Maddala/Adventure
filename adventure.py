import json
import sys

abbreviations = {
    "n": "north",
    "no": "north",
    "nor": "north",
    "nort": "north",
    "north": "north",
    "e": "east",
    "ea": "east",
    "eas": "east",
    "east": "east",
    "w": "west",
    "we": "west",
    "wes": "west",
    "west": "west",
    "s": "south",
    "so": "south",
    "sou": "south",
    "sout": "south",
    "south": "south",
    "ne": "northeast",
    "northe": "northeast",
    "northea": "northeast",
    "northeas": "northeast",
    "northeast": "northeast",
    "nw": "northwest",
    "northw": "northwest",
    "northwe": "northwest",
    "northwes": "northwest",
    "northwest": "northwest",
    "se": "southeast",
    "southe": "southeast",
    "southea": "southeast",
    "southeas": "southeast",
    "southeast": "southeast",
    "sw": "southwest",
    "southw": "southwest",
    "southwe": "southwest",
    "southwes": "southwest",
    "southwest": "southwest",
    "i": "inventory"
    # Additional abbreviations as needed
}

direction_abbreviations = {
    "n": "north",
    "e": "east",
    "s": "south",
    "w": "west",
    "ne": "northeast",
    "nw": "northwest",
    "se": "southeast",
    "sw": "southwest",
    # Extend with other abbreviations as needed
}

class AdventureGame:
    def __init__(self, map_file):
        self.map_file = map_file
        self.game_map = None
        self.current_location = 0
        self.player_inventory = []
        self.game_running = True
        self.load_map()

    def load_map(self):
        with open(self.map_file, 'r') as file:
            self.game_map = json.load(file)

    def start_game(self):
        self.look()
        while self.game_running:
            try:
                print("What would you like to do?",end=" ")
                command = input().strip().lower()
                self.process_command(command)
            except EOFError:
                print("\nUse 'quit' to exit.")
                continue

    def process_command(self, command):
        command_parts = command.split()
        base_command = command_parts[0]

        # Check if command is an abbreviation and get its full form
        if base_command in abbreviations:
            base_command = abbreviations[base_command]

        # Check if the command is a direction or a verb
        if base_command in direction_abbreviations:
            base_command = "go"

       # Process the command as a movement if it's a direction or an abbreviation for a direction
        if base_command in direction_abbreviations.values() or base_command in direction_abbreviations:
            self.move_player(direction_abbreviations.get(base_command, base_command))
        elif base_command == "go":
            # Handle 'go' followed by a direction
            if len(command_parts) > 1:
                direction = direction_abbreviations.get(command_parts[1], command_parts[1])
                self.move_player(direction)
            else:
                print("Sorry, you need to 'go' somewhere.")
        elif base_command == "look":
            self.look()
        elif base_command == "get":
            self.handle_get_command(command_parts)
        elif base_command == "drop":
            self.handle_drop_command(command_parts)
        elif base_command == "inventory":
            self.show_inventory()
        elif base_command == "items":
            self.show_items()
        elif base_command == "trade":
            self.handle_trade_command(command_parts)
        elif base_command == "help":
            self.show_help()
        elif base_command == "exits":
            self.show_exits()
        elif base_command == "quit":
            print("Goodbye!")
            self.game_running = False 
        else:
            print("Invalid command. Try 'help' for a list of valid commands.")

    def move_player(self, direction):
        current_location = self.game_map[self.current_location]
        if direction in current_location["exits"]:
            next_location_index = current_location["exits"][direction]
            next_location = self.game_map[next_location_index]
            if next_location.get("locked", False) and "key" in next_location:
                required_item = next_location["key"]
                if required_item in self.player_inventory:
                    print("You go "+direction+".")
                    print(f"Using {required_item} to unlock the door.")
                    self.current_location = next_location_index
                    self.look()
                    self.check_conditions()
                else:
                    print("You go "+direction+".")
                    print("The door is locked. You need something to unlock it.")
            else:
                self.current_location = next_location_index
                print("You go "+direction+".")
                print()
                self.look()
                self.check_conditions()
        else:
            print("There's no way to go "+ direction + ".")
    
    def check_conditions(self):
        location = self.game_map[self.current_location]
        conditions = location.get("conditions", {})
        
        # Check winning condition
        win_condition = conditions.get("win")
        if win_condition and win_condition["item"] in self.player_inventory:
                print(win_condition["message"])
                self.game_running = False 
        elif conditions.get("lose"):
            lose_condition = conditions.get("lose")
            print(lose_condition["message"])
            self.game_running = False 

        '''# Check losing condition
        lose_condition = conditions.get("lose")
        #print(lose_condition["message"])
        if lose_condition and win_condition["item"] not in self.player_inventory:
            lose_condition = conditions.get("lose")
            print(lose_condition["message"])
            sys.exit(0)'''
    
    def look(self):
        location = self.game_map[self.current_location]
        self.check_conditions()
        print(f"> {location['name']}\n")
        print(f"{location['desc']}\n")
        items = location.get("items", [])
        if items:
            print("Items: " + " ".join(items) + "\n")
        exits = location.get("exits", {})
        exits_description = " ".join(exits.keys())
        print(f"Exits: {exits_description}\n")
        #print("What would you like to do?",end=" ") 

    def handle_get_command(self, command_parts):
        if len(command_parts) > 1:
            item_abbr = " ".join(command_parts[1:])
            self.get_item_by_abbr(item_abbr)
            self.check_conditions()
        else:
            print("Sorry, you need to 'get' something.")

    def get_item_by_abbr(self, item_abbr):
        location = self.game_map[self.current_location]
        matching_items = [item for item in location.get("items", []) if item.lower().startswith(item_abbr.lower())]
        
        if len(matching_items) == 1:
            self.pick_up_item(matching_items[0])
        elif len(matching_items) > 1:
            self.ask_for_item_clarification(matching_items)
        else:
            print("There's no "+str(item_abbr)+" anywhere.")

    def ask_for_item_clarification(self, matching_items):
        print("Did you mean one of these items? " + ", ".join(matching_items))
        choice = input("").strip().lower()
        if choice in matching_items:
            self.pick_up_item(choice)
        else:
            print("Invalid item choice.")

    def pick_up_item(self, item_name):
        location = self.game_map[self.current_location]
        if item_name in location.get("items", []):
            location["items"].remove(item_name)
            self.player_inventory.append(item_name)
            print(f"You pick up the {item_name}.")
            # Immediately check for win/lose conditions after picking up an item
            self.check_conditions()


    def handle_drop_command(self, command_parts):
        if len(command_parts) > 1:
            item = " ".join(command_parts[1:])
            if item in self.player_inventory:
                self.player_inventory.remove(item)
                self.game_map[self.current_location].setdefault("items", []).append(item)
                print(f"You dropped the {item}.")
            else:
                print(f"You don't have {item} in your inventory.")
        else:
            print("You must specify an item to drop.")

    def handle_trade_command(self, command_parts):
        current_location = self.game_map[self.current_location]
        if current_location.get("trader"):
            if len(command_parts) == 2:
                item_to_trade = command_parts[1]
                if item_to_trade in self.player_inventory and item_to_trade == current_location["trader"]["wants"]:
                    self.player_inventory.remove(item_to_trade)
                    self.player_inventory.append(current_location["trader"]["offers"])
                    print(f"You traded your {item_to_trade} for {current_location['trader']['offers']}.")
                else:
                    print(f"The trader does not want {item_to_trade}.")
            else:
                print("To trade, specify 'trade [item]'.")
        else:
            print("There is no one to trade with here.")

    def show_inventory(self):
        if self.player_inventory:
            #self.check_conditions()
            print("Inventory:")
            for i in self.player_inventory:
                print(" ",i)
        else:
            print("You're not carrying anything.")

    def show_items(self):
        location = self.game_map[self.current_location]
        items = location.get("items", [])
        if items:
            print("Items in this location:", ", ".join(items))
        else:
            print("There are no items here.")

    def show_exits(self):
        location = self.game_map[self.current_location]
        exits = location.get("exits", {})
        if exits:
            print("Available exits:", " ".join(exits.keys()))
        else:
            print("There are no exits from here.")

    def show_help(self):
        print("Available commands:")
        print("  go [direction] - Move in the specified direction (north, south, east, west).")
        print("  get [item] - Pick up an item from the current location.")
        print("  drop [item] - Drop an item from your inventory into the current location.")
        print("  trade [item] - Trade an item with a character in the current location.")
        print("  inventory - Show the items you are carrying.")
        print("  look - Describe the current location.")
        print("  items - List all items in the current location.")
        print("  exits - Show all available exits from the current location.")
        print("  help - Display this help message.")
        print("  quit - Exit the game.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 adventure.py [map_file]")
        return
    map_file = sys.argv[1]
    game = AdventureGame(map_file)
    game.start_game()

if __name__ == "__main__":
    main()

