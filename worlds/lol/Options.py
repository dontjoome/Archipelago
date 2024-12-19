from dataclasses import dataclass, asdict

from Options import Choice, Range, Option, Toggle, DeathLink, DefaultOnToggle, OptionSet, PerGameCommonOptions

from .Data import champions

class LPGoal(Choice):
    """
    How would you prefer to goal?

    LP Galore: Varying amount of LP dependent on how many/what games are involved since LP is filler and progression.

    LP Hunt: Set amount of LP, similar to other "macguffin" type options and could have 50LP in a 1k person seed. Good luck. 
    """
    option_galore = 0
    option_hunt = 1
    default = 0
    display_name = "Required LP Goal"

class AvailableLPAmount(Range):
    """
    Amount of LP available in the seed. This is purely for the Hunt goal option above.

    Lower amount of LP means more Coupons for Free Surgery from Dr. Mundo, you've been warned.
    """
    default = 50
    range_start = 10
    range_end = 100
    display_name = "Available LP Amount"

class RequiredLPPercentage(Range):
    """
    Percentage of LP required to goal. This affects both goals above.
    """
    default = 50
    range_start = 30
    range_end = 100
    display_name = "Required LP Percentage"

class Champions(OptionSet):
    """
    Which champions are possibly included in the item pool?
    """
    display_name = "Champions"
    valid_keys = [champions[champion_id]["name"] for champion_id in champions]
    default = sorted(set([champions[champion_id]["name"] for champion_id in champions]))

class RequiredCreepScore(Range):
    """
    Required CS to complete CS checks
    """
    default = 100
    range_start = 50
    range_end = 400
    display_name = "Required Creep Score"

class RequiredVisionScore(Range):
    """
    Required VS to complete VS checks
    """
    default = 30
    range_start = 10
    range_end = 100
    display_name = "Required Vision Score"

class RequiredKills(Range):
    """
    Required Kills to complete Kill checks
    """
    default = 3
    range_start = 1
    range_end = 15
    display_name = "Required Kills"

class RequiredAssists(Range):
    """
    Required Assists to complete Assist checks
    """
    default = 5
    range_start = 3
    range_end = 30
    display_name = "Required Assists"

class StartingChampions(Range):
    """
    Number of champions in your starting inventory
    """
    default = 3
    range_start = 1
    range_end = 5
    display_name = "Starting Champions"

class ChampionSubsetCount(Range):
    """
    Number of champions to randomly select for the item pool of those listed provided.
    """
    default = 20
    range_start = 1
    range_end = 200
    display_name = "Champion Subset Count"

@dataclass
class LOLOptions(PerGameCommonOptions):
    champions: Champions
    required_creep_score: RequiredCreepScore
    required_vision_score: RequiredVisionScore
    required_kills: RequiredKills
    required_assists: RequiredAssists
    lp_goal: LPGoal
    available_lp: AvailableLPAmount
    required_lp: RequiredLPPercentage
    starting_champions: StartingChampions
    champion_subset_count: ChampionSubsetCount