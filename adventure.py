import json
import sys

class AdventureGame:
    def __init__(self, map_file):
        self.map_file = map_file
        self.game_map = None
        self.current_location = 0
        self.player_inventory = []
        self.load_map()

    def load_map(self):
        with open(self.map_file, 'r') as file:
            self.game_map = json.load(file)

    def start_game(self):
        print("Welcome to the One Piece Adventure Game!")
        self.look()
        while True:
            print("What would you like to do?")
            command = input("> ").strip().lower()
            self.process_command(command)

    def process_command(self, command):
        abbreviations = {
            "n": ["north"],
            "s": ["south"],
            "e": ["east"],
            "w": ["west"],
            "ne": ["northeast"],
            "nw": ["northwest"],
            "se": ["southeast"],
            "sw": ["southwest"],
            "i": ["inventory", "items"],
            "g": ["get", "go"]
            
            # Add more abbreviations as needed
        }

        command_parts = command.split()
        base_command = command_parts[0]

        # Handle abbreviations
        if base_command in abbreviations:
            possible_commands = abbreviations[base_command]
            if len(possible_commands) > 1:
                self.ask_for_clarification(possible_commands)
                return  # Return after clarification to avoid immediate command execution
            else:
                base_command = possible_commands[0]

        # Process the command
        if base_command in ["north", "south", "east", "west", "northeast", "northwest", "southeast", "southwest"]:
            self.move_player(base_command)
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
            print("Thank you for playing!")
            sys.exit(0)
        elif base_command == "go":
            # If 'go' is used, process the next part of the command as a direction
            if len(command_parts) > 1 and command_parts[1] in ["north", "south", "east", "west", "northeast", "northwest", "southeast", "southwest"]:
                self.move_player(command_parts[1])
            else:
                print("Invalid direction. Try 'help' for a list of valid commands.")
        else:
            print("Invalid command. Try 'help' for a list of valid commands.")

    def ask_for_clarification(self, possible_commands):
        print("Did you mean one of these commands? " + ", ".join(possible_commands))
        choice = input("> ").strip().lower()
        if choice in possible_commands:
            self.process_command(choice)  # Re-process the clarified command
        else:
            print("Invalid choice.")

            
    def move_player(self, direction):
        current_location = self.game_map[self.current_location]
        if direction in current_location["exits"]:
            next_location_index = current_location["exits"][direction]
            next_location = self.game_map[next_location_index]
            if next_location.get("locked", False) and "key" in next_location:
                required_item = next_location["key"]
                if required_item in self.player_inventory:
                    print(f"Using {required_item} to unlock the door.")
                    self.current_location = next_location_index
                    self.look()
                else:
                    print("The door is locked. You need something to unlock it.")
            else:
                self.current_location = next_location_index
                self.look()
        else:
            print("You can't go that way.")


    def look(self):
        location = self.game_map[self.current_location]
        print(location["desc"])
        self.show_items()
        self.show_exits()
    
    def handle_get_command(self, command_parts):
        if len(command_parts) > 1:
            item_abbr = " ".join(command_parts[1:])
            self.get_item_by_abbr(item_abbr)
        else:
            print("You must specify an item to get.")

    def get_item_by_abbr(self, item_abbr):
        location = self.game_map[self.current_location]
        matching_items = [item for item in location.get("items", []) if item.lower().startswith(item_abbr.lower())]

        if len(matching_items) == 1:
            self.pick_up_item(matching_items[0])
        elif len(matching_items) > 1:
            self.ask_for_item_clarification(matching_items)
        else:
            print("That item is not here.")


    def ask_for_item_clarification(self, matching_items):
        print("Did you mean one of these items? " + ", ".join(matching_items))
        choice = input("> ").strip().lower()
        if choice in matching_items:
            self.pick_up_item(choice)
        else:
            print("Invalid item choice.")
            
    def pick_up_item(self, item_name):
        location = self.game_map[self.current_location]
        if item_name in location.get("items", []):
            location["items"].remove(item_name)
            self.player_inventory.append(item_name)
            print(f"You picked up the {item_name}.")
            if item_name == "One Piece" or item_name == "One":
                self.check_win_condition()
        else:
            print("That item is not here.")

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

        # Check if the player is in Syrup Village and there is a trader
        if current_location["name"] == "Syrup Village" and "trader" in current_location:
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
            print("You are carrying:", ", ".join(self.player_inventory))
            self.check_win_condition()
        else:
            print("Your inventory is empty.")

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
            print("Available exits:", ", ".join(exits.keys()))
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

    def check_win_condition(self):
        # Assuming the last location in your game map is where the player wins the game
        win_location_name = self.game_map[-1]["name"]

        if "One Piece" in self.player_inventory and self.game_map[self.current_location]["name"] == win_location_name:
            print("Congratulations! You have found the One Piece and won the game!")
            sys.exit(0)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 adventure.py [map_file]")
        return

    map_file = sys.argv[1]
    game = AdventureGame(map_file)
    game.start_game()

if __name__ == "__main__":
    main()
