# Project2
This repository contains the implementation of a game engine that loads and lets the player play text horror game using a map file in JSON format. 

```
Name: Surya Teja Koritala, Paul John Maddala
Stevens Login: skorital1@stevens.edu, pmaddala@stevens.edu 
Hours spent on the project: 16 hours
```
GitHub Repo: ["https://github.com/Pauljohn-Maddala/Adventure.git"]
## Testing
I combined automated and manual testing to test the code. I created unit tests for every module's essential functionality using the pytest and other comparable frameworks for automated testing. I manually tested the game by playing it through various scenarios and maps to make sure everything works properly and there are no bugs. In order to make sure the three extensions function as intended, I also thoroughly tested each of them.
* Eg: Command parsing
    * Incorrect and extra spacing between and around command text. eg: go   south    
    * Incorrect case. eg: GO   SOUTH
    * Incorrect verbs. eg: RHGLH
    * Incorrect commands: eg: $%#@% 4534    4%$%#

## Bugs or Issues
1. Command parsing - 
   * Running into an infinite loop due to recursion - resolved
2. Winning and losing condition not triggering - resolved
3. Separation of classes based upon the use-case of the game
   * Coming up with the states of those classes and behaviours affecting the state to represent it well - resolved
    
## Difficult issue or bug
The extension that adds winning and losing conditions to the game was one of the trickiest problems I ran into. The problem stemmed from the implementation of the key checks (**win_condition** and (**lose_condition**) to initiate winning and losing logic, which necessitated the interaction of several functions to alter the game state. Upon implementing the feature and making it function as intended, I was able to do some debugging and reworking.
```
Eg: 
if 'lose_condition' in self.room:
    # Do run the losing logic
    
if 'win_condition' in self.room:
    # Do run the winning logic
```

## Known Issues
While working on the project, we came across a number of bugs and problems. The JSON map file parsing was one of the problems. Due to certain edge cases, the code occasionally failed to parse a map file in a valid JSON format. Additionally, there were a few glitches in the inventory system that occasionally led to strange behaviour when moving or dropping things. However, in our testing, we were unable to locate any bugs in this game.

# Extensions

## 1. Help Command

**Description:**
The `help` command provides players with a list of available commands and a brief description of each. It serves as a quick reference for players to understand the actions they can take within the game.

**Usage:**
```plaintext
help - Display a list of available commands and their descriptions.
```



## 2. Drop and Inventory System

**Description:**
The game includes an inventory system where players can carry and manage items. The `drop` command allows players to remove items from their inventory and place them in the current location.

**Usage:**
```plaintext
drop [item] - Drop an item from your inventory into the current location.
inventory - Show the items you are carrying.
```

## 3. Lock and Unlock Mechanism

**Description:**
Locations within the game can now be locked, requiring specific items (keys) to unlock them. This adds an extra layer of complexity to the game, as players must find and manage keys to access certain areas.

**Usage:**
```plaintext
lock - Some locations may be locked, requiring a key to unlock.
unlock - Use a key to unlock a locked location and proceed.
```


## 4. Winning and Losing Conditions

**Description:**
Certain locations have conditions for winning or losing the game. Winning conditions may involve having a specific item in the player's inventory, while losing conditions could be triggered by specific events or lack of necessary items.

**Usage:**
```
"locations": {
    "0": {
        "name": "End",
        "desc": "Congratulations! You've reached the end of the game.",
        "items": [],
        "exits": {},
        "conditions": {
            "win": {"item": "treasure", "message": "You found the treasure! You win the game!"},
            "lose": {"message": "Oh no! You failed to find the treasure. Game over."}
        }
    },
    // ... other locations ...
}

```
```plaintext
> End

Congratulations! You've reached the end of the game.

What would you like to do? get treasure
You pick up the treasure.

Conditions are checked after each action, affecting the outcome of the game.

Congratulations! You found the treasure! You win the game!

```
```
Conditions are checked after each action, affecting the outcome of the game.
Oh no! You entered the dragon's lair without the protective shield. The dragon devours you, and your adventure comes to a tragic end.

```


## 5. Direction Verbs

**Description:**
The game supports both full directions (north, south, east, west) and their abbreviations. This extension allows players to use shorter commands for movement, enhancing the convenience and fluidity of gameplay.

**Usage:**
```plaintext
go [direction] - Move in the specified direction (north, south, east, west).
```
## Map File
```
[
    {
        "name": "Foosha Village",
        "desc": "A small, peaceful village where your adventure begins.",
        "items": ["straw hat"],
        "exits": { "east": 1 },
        "locked": false
    },
    {
        "name": "Orange Town",
        "desc": "A once vibrant town, now quiet. A locked door leads to the north.",
        "items": ["key"],
        "exits": { "west": 0, "north": 2 },
        "locked": false
    },
    {
        "name": "Syrup Village",
        "desc": "A quaint village, known for its syrup production. A mysterious old sailor here offers a trade.",
        "items": ["spyglass"],
        "exits": { "south": 1, "east": 3 },
        "locked": {"north": true},
		"key": "key",
        "trader": {
            "wants": "spyglass",
            "offers": "treasure map"
        }
    },
    {
        "name": "Baratie",
        "desc": "A floating restaurant. The chef seems to be guarding a door leading east.",
        "items": [],
        "exits": { "west": 2, "east": 4 },
        "locked": true,
        "key": "treasure map"
    },
    {
        "name": "Arlong Park",
        "desc": "Once a fearsome pirate's stronghold. Rumors say the One Piece is hidden here.",
        "items": ["one piece", "meat"],
        "exits": { "west": 3 },
        "locked": false,
        "conditions": {
        "win": {
            "item": "meat",
            "message": "Congratulations! You've won the game!"
        },
        "lose": {
            "item": "one piece",
            "message": "Oh no! You've lost the game."
        }
    	}
    }
]
```





