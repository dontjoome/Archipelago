from typing import List

from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld, World
from .Items import LOLItem, LOLItemData, event_item_table, get_items_by_category, item_table
from .Locations import LOLLocation, location_table, get_locations_by_category
from .Options import LOLOptions
from .Regions import create_regions
from .Rules import set_rules
from .Data import champions
from worlds.LauncherComponents import Component, components, Type, launch_subprocess



def launch_client():
    from .Client import launch
    launch_subprocess(launch, name="LOL Client")


components.append(Component("LOL Client", "LOLClient", func=launch_client, component_type=Type.CLIENT))

class LOLWeb(WebWorld):
    theme = "ocean"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the League of Legends AP Randomizer software on your computer. This guide covers single-player, "
        "multiworld, and related software.",
        "English",
        "lol_en.md",
        "LOL/en",
        ["Gicu"]
    )]

class LOLWorld(World):
    """
    League of Legends (LoL), commonly referred to as League, is a 2009 multiplayer online battle arena video game developed and published by Riot Games.
    """
    game = "League of Legends"
    options_dataclass = LOLOptions
    options: LOLOptions
    topology_present = True
    required_client_version = (0, 3, 5)
    web = LOLWeb()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.code for name, data in location_table.items()}
    
    def __init__(self, multiworld: "MultiWorld", player: int):
        super(LOLWorld, self).__init__(multiworld, player)
        self.possible_champions = []
        self.added_lp = 0

    def create_items(self):
        item_pool: List[LOLItem] = []
        self.choose_possible_champions()
        print(self.possible_champions)
        starting_champions = self.random.sample(self.possible_champions, min(self.options.starting_champions, len(self.possible_champions)))
        for i in range(len(starting_champions)):
            self.multiworld.get_location("Starting Champion " + str(i+1), self.player).place_locked_item(self.create_item(starting_champions[i]))
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))
        for name, data in item_table.items():
            if name in self.possible_champions and name not in starting_champions:
                item_pool += [self.create_item(name) for _ in range(0, 1)]
            
        if self.options.lp_goal == 'galore':

            while len(item_pool) < total_locations:
                item_pool.append(self.create_item("LP"))
                self.added_lp += 1

        elif self.options.lp_goal == 'hunt':
            for x in range(int(self.options.available_lp)):
                item_pool.append(self.create_item("LP"))
                self.added_lp += 1

            while len(item_pool) < total_locations:
                item_pool.append(self.create_item('Coupon for Free Surgery from Dr. Mundo'))

        self.multiworld.itempool += item_pool
        
    def create_item(self, name: str) -> LOLItem:
        data = item_table[name]
        return LOLItem(name, data.classification, data.code, self.player)
	
    def set_rules(self):
        self.choose_possible_champions()
        set_rules(self.multiworld, self.player, self.options, int(self.added_lp * (self.options.required_lp / 100)), self.possible_champions)

    def create_regions(self):
        self.choose_possible_champions()
        create_regions(self.multiworld, self.player, self.options, self.possible_champions)
    
    def fill_slot_data(self) -> dict:
        slot_data = {"Required CS":      int(self.options.required_creep_score)
                    ,"Required VS":      int(self.options.required_vision_score)
                    ,"Required Kills":   int(self.options.required_kills)
                    ,"Required Assists": int(self.options.required_assists)
                    ,"Required LP":      int(self.added_lp * (self.options.required_lp / 100))}
        return slot_data
    
    def choose_possible_champions(self):
        if len(self.possible_champions) == 0:
            print("Here")
            for champion_id in champions:
                champion_name = champions[champion_id]["name"]
                if champion_name in self.options.champions.value:
                    self.possible_champions.append(champion_name)
            if len(self.possible_champions) > self.options.champion_subset_count:
                self.possible_champions = self.random.sample(self.possible_champions, self.options.champion_subset_count)