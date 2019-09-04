# Game
RADIANT_KEY = "radiant"
DIRE_KEY = "dire"
TEAM_KEY = "team"
ACTION_KEY = "action"
HERO_KEY = "hero"
PICK_KEY = "pick"
BAN_KEY = "ban"
PICK_RADIANT = {TEAM_KEY: RADIANT_KEY, ACTION_KEY: PICK_KEY}
PICK_DIRE = {TEAM_KEY: DIRE_KEY, ACTION_KEY: PICK_KEY}
BAN_RADIANT = {TEAM_KEY: RADIANT_KEY, ACTION_KEY: BAN_KEY}
BAN_DIRE = {TEAM_KEY: DIRE_KEY, ACTION_KEY: BAN_KEY}
ALL_PICK_ORDER_RADIANT = [PICK_RADIANT, PICK_DIRE, PICK_DIRE, PICK_RADIANT, PICK_RADIANT, PICK_DIRE, PICK_DIRE,
                          PICK_RADIANT, PICK_RADIANT, PICK_DIRE]
ALL_PICK_ORDER_DIRE = [PICK_DIRE, PICK_RADIANT, PICK_RADIANT, PICK_DIRE, PICK_DIRE, PICK_RADIANT, PICK_RADIANT,
                       PICK_DIRE, PICK_DIRE, PICK_RADIANT]
CAPTAINS_MODE_ORDER = [
    BAN_RADIANT, BAN_DIRE, BAN_RADIANT, BAN_DIRE, BAN_RADIANT, BAN_DIRE,
    PICK_RADIANT, PICK_DIRE, PICK_DIRE, PICK_RADIANT,
    BAN_RADIANT, BAN_DIRE, BAN_RADIANT, BAN_DIRE,
    PICK_DIRE, PICK_RADIANT, PICK_DIRE, PICK_RADIANT,
    BAN_DIRE, BAN_RADIANT,
    PICK_RADIANT, PICK_DIRE
]
BANNED_KEY = "banned"
WINNER_KEY = "winner"
WINS_KEY = "wins"
LOSSES_KEY = "losses"
WINS_SUFFIX = " wins"
WINRATE_SUFFIX = " winrate"
ADVANTAGE_SUFFIX = " advantage"
VALUE_SUFFIX = " value"
TEAM_SIZE = 5

# MongoDB
DOTA2_DATABASE = "dota2"
HEROES_TABLE = "heroes"
MATCH_DETAILS_TABLE = "match_details"
STEAM_API_KEY = "E5E97D6166ADB1F6D5DB97D2F1284988"
MONGO_HOST = "localhost"
MONGO_PORT = 27017

# API
API_PLAYERS = "players"
API_HERO_ID = "hero_id"
API_RADIANT_WIN = "radiant_win"
API_LAST_HITS = "last_hits"
API_GPM = "gold_per_min"

# Model
MONTE_CARLO_DEPTH = 1
TURN_KEY = "turn"
TURN_TO_PICK_FALSE = False
TURN_TO_PICK_TRUE = True
HEROES_KEY = "heroes"
COMBOS_KEY = "combos"
MATCHUPS_KEY = "matchups"
FACTIONS_KEY = "factions"
MATCHUP_INFIX = " vs "
COMBO_INFIX = " + "
PREDICTION_HEROES_COEFFICIENT = 1.0115966796875
PREDICTION_MATCHUP_COEFFICIENT = 0.90625
PREDICTION_COMBO_COEFFICIENT = 1.81414794921875
PREDICTION_FACTION_COEFFICIENT = 0.90625
PREDICTION_DIFFERENCE_SCALE = 53.922027458141194
PERCENTAGE_MAX = 100
PERCENTAGE_MIN = 0
POSITIVE_INFINITY = float("inf")
NEGATIVE_INFINITY = float("-inf")
SCORE_KEY = "score"
RANK_KEY = "rank"
VALUE_WITH_RADIANT_KEY = "Value With Radiant"
VALUE_AGAINST_RADIANT_KEY = "Value Against Radiant"
TOTAL_VALUE_TO_RADIANT_KEY = "Total Value To Radiant"
VALUE_WITH_DIRE_KEY = "Value With Dire"
VALUE_AGAINST_DIRE_KEY = "Value Against Dire"
TOTAL_VALUE_TO_DIRE_KEY = "Total Value To Dire"
TOTAL_VALUE_KEY = "Total Value"
GAMES_KEY = "games"

# Neural Network
ROSTERS_KEY = "rosters"
LABELS_KEY = "labels"
ALLY_NN_OFFSET = 0
ENEMY_NN_OFFSET = 0
BANNED_NN_OFFSET = 0
NN_OFFSETS = [ALLY_NN_OFFSET, ENEMY_NN_OFFSET, BANNED_NN_OFFSET]

# Files
DATA_DIR = "./data/"
HERO_INDEX_FILE = DATA_DIR + "hero_indexes.dict"
VALUES_FILE = DATA_DIR + "values.dict"
EXPERIMENTAL_VALUES_FILE = DATA_DIR + "experimental_values.dict"
GAMES_FILE = DATA_DIR + "games.arr"
DRAFTING_MODEL_FILE = DATA_DIR + "drafting_model.h5"
ALL_FILES = [HERO_INDEX_FILE, VALUES_FILE, GAMES_FILE, DRAFTING_MODEL_FILE]

# DraftMaster 5
APP_NAME = "DraftMaster"
VERSION = "5.1.3"
PATCH_NOTE = "Trained on 184,933 games of 7.22f! Accuracy at 65%!"
APP_FULL_NAME = APP_NAME + " " + VERSION
DECIMAL_ROUND = 2
PLATFORM_WINDOWS = "Windows"
WIN_MAXIMIZE = 3
WIN_DLL = 'user32'
DEFAULT_OPTIONS_COUNT = 20
PROMPT = "> "
ALIGN_CENTER = 'c'
ALIGN_LEFT = 'l'
ALIGN_RIGHT = 'r'

CMD_SELECT = "select"
CMD_BACK = "back"
CMD_HISTORY = "history"
CMD_EXPLAIN = "explain"
CMD_COUNTERS = "counters"
CMD_COMBOS = "combos"
CMD_DONE = "done"
CMD_NEW = "new"
CMD_OPTIONS = "options"
CMD_SEARCH = "search"
CMD_HELP = "help"
CMD_QUIT = "quit"
CMD_EMPTY = ""

CONTEXT_MAIN = "main"
CONTEXT_ALL_PICK_BANNING = "all pick banning"
CONTEXT_PICK_BAN = "pick/ban"

CONTEXT_MAIN_COMMANDS = [CMD_NEW, CMD_HELP, CMD_QUIT]
CONTEXT_ALL_PICK_BANNING_COMMANDS = [CMD_SELECT, CMD_BACK, CMD_HISTORY, CMD_DONE, CMD_SEARCH, CMD_NEW, CMD_HELP,
                                     CMD_DONE, CMD_QUIT]
CONTEXT_PICK_BAN_COMMANDS = [CMD_SELECT, CMD_BACK, CMD_OPTIONS, CMD_HISTORY, CMD_EXPLAIN, CMD_COUNTERS, CMD_COMBOS,
                             CMD_SEARCH, CMD_NEW, CMD_HELP, CMD_QUIT]

CONTEXT_IMPLICIT_SEARCH = {
    CONTEXT_MAIN: False,
    CONTEXT_ALL_PICK_BANNING: True,
    CONTEXT_PICK_BAN: True
}

ARG_RADIANT = RADIANT_KEY
ARG_DIRE = DIRE_KEY
ARG_BANNED = BANNED_KEY
ARG_ALL_PICK = "allpick"
ARG_CAPTAINS_MODE = "captains"
ARG_BEST_CASE = "best"
ARG_WORST_CASE = "worst"
ARG_OPTIMAL_CASE = "optimal"
ARG_PESSIMAL_CASE = "pessimal"
CASE_ARGS = [ARG_BEST_CASE, ARG_WORST_CASE, ARG_OPTIMAL_CASE, ARG_PESSIMAL_CASE]

HELP_HINT = "Partial hero names work.  Word order does not matter.\n"
HELP_SELECT = "Selects a hero.  Select is the default command when available." + \
              "  Partial names, nicknames, and abbreviations work.  Example: '" + CMD_SELECT + " spectre' OR 'spectre'"
HELP_BACK = "Undoes the last selection.  Example: '" + CMD_BACK + "'"
HELP_HISTORY = "Shows pick/ban history.  Example: '" + CMD_HISTORY + "'"
HELP_EXPLAIN = "Explains the current hero/matchup/combo/faction values.  Example: '" + CMD_EXPLAIN + "'"
HELP_COUNTERS = "Lists a number of the best counters for a given hero.  Default is " + str(DEFAULT_OPTIONS_COUNT) + \
                ".  Example: '" + CMD_COUNTERS + " spectre'"
HELP_COMBOS = "Lists a number of the best combos for a given hero.  Default is " + str(DEFAULT_OPTIONS_COUNT) + \
              ".  Example: '" + CMD_COMBOS + " spectre'"
HELP_DONE = "Finishes the All Pick Banning Phase, starting the draft with the given team picking first." + \
            "  Cannot be undone with '" + CMD_BACK + "'.  Example: '" + CMD_DONE + " " + ARG_RADIANT + "'"
HELP_NEW = "Starts a new draft.  Example: '" + CMD_NEW + " " + ARG_ALL_PICK + "' OR '" + CMD_NEW + " " + \
           ARG_CAPTAINS_MODE + "'"
HELP_OPTIONS = "Gives a number of the best options for the current selection.  Default is " + \
               str(DEFAULT_OPTIONS_COUNT) + ".  Example: '" + CMD_OPTIONS + "' OR '" + CMD_OPTIONS + " 20'"
HELP_SEARCH = "Searches for a hero.  Example: '" + CMD_SEARCH + " spec'"
HELP_HELP = "Displays this help message.  Example: '" + CMD_HELP + "'"
HELP_QUIT = "Quit the program.  Example: '" + CMD_QUIT + "'"

HELP_MAP = {
    CMD_SELECT: HELP_SELECT,
    CMD_BACK: HELP_BACK,
    CMD_HISTORY: HELP_HISTORY,
    CMD_EXPLAIN: HELP_EXPLAIN,
    CMD_COUNTERS: HELP_COUNTERS,
    CMD_COMBOS: HELP_COMBOS,
    CMD_DONE: HELP_DONE,
    CMD_NEW: HELP_NEW,
    CMD_OPTIONS: HELP_OPTIONS,
    CMD_SEARCH: HELP_SEARCH,
    CMD_HELP: HELP_HELP,
    CMD_QUIT: HELP_QUIT
}

MSG_RADIANT_TURN_TO_PICK = "Radiant's turn to pick."
MSG_DIRE_TURN_TO_PICK = "Dire's turn to pick."
MSG_RADIANT_TURN_TO_BAN = "Radiant's turn to ban."
MSG_DIRE_TURN_TO_BAN = "Dire's turn to ban."
MSG_RADIANT_PICK = "Radiant picked hero: "
MSG_DIRE_PICK = "Dire picked hero: "
MSG_RADIANT_BAN = "Radiant banned hero: "
MSG_DIRE_BAN = "Dire banned hero: "
MSG_BAN = "Banned hero: "
MSG_INDENT = "	"
MSG_BAD_COMMAND = "Invalid command or syntax.  Type '" + CMD_HELP + "' for a list of commands."
MSG_STARTUP = "Loading " + APP_FULL_NAME + "..."
MSG_WELCOME = "Welcome to " + APP_FULL_NAME + "!\nType '" + CMD_HELP + "' for a list of commands.\n" + PATCH_NOTE + "\n"
MSG_QUIT = "Quitting " + APP_FULL_NAME + "..."
MSG_RADIANT_WINRATE = "Radiant Winrate"
MSG_DIRE_WINRATE = "Dire Winrate"
MSG_COLON_INFIX = ": "
MSG_PLATFORM_INCOMPATIBLE = "OS does not support this function."
MSG_BAD_MONTE_CARLO_DEPTH = "Search depth must be greater than 0."
MSG_BAD_MONTE_CARLO_COMPLETE = "Draft is complete."
MSG_BAD_CONTEXT = "Command not compatible with this context.  Type '" + CMD_HELP + "' for a list of commands."
MSG_BAD_NEW = "Invalid argument.  Use '" + ARG_ALL_PICK + "' OR '" + ARG_CAPTAINS_MODE + "'."
MSG_BANNING_COMPLETE = "Banning phase complete."
MSG_CANNOT_SELECT_DRAFT_COMPLETE = "Cannot select hero.  Draft is complete."
MSG_DRAFT_COMPLETE = "Draft is complete."
MSG_HERO_NOT_FOUND = "Hero not found: "
MSG_HERO_UNAVAILABLE = "Hero already picked or banned: "
MSG_SPACE = " "
MSG_UNDONE = "Undone: "
MSG_CANNOT_UNDO = "Cannot undo nothing!"
MSG_HISTORY = "History"
MSG_COMMA_SEPARATOR = ", "
MSG_NEW_ALL_PICK = "New All Pick"
MSG_NEW_CAPTAINS = "New Captains Mode"
MSG_ALL_PICK_BANNING = "All Pick Banning Phase"
MSG_LINE_BREAK = "-"
MSG_MAIN_MENU = "Main Menu"
MSG_NEWLINE = "\n"
MSG_EMPTY = ""
MSG_THINKING = "Thinking..."
MSG_EXPLAIN_VALUES = "Explain Values\n"
MSG_SLASH_INFIX = " / "
MSG_DIFFERENCE = "Difference"
MSG_SEARCH_FOR = "Searching for: "
MSG_BAD_DONE = "Please specify the team that was assigned first pick."
MSG_COMMAND = "Command"
MSG_DESCRIPTION = "Description"
MSG_MATCHUPS_HINT = "(+) favors radiant, (-) favors dire"
MSG_PERCENT = "%"
MSG_AVERAGE_CASE = "Average Case"
MSG_BEST_CASE = "Best Case"
MSG_WORST_CASE = "Worst Case"
MSG_OPTIMAL_CASE = "Optimal Case"
MSG_PESSIMAL_CASE = "Pessimal Case"

HERO_NICKNAMES = {
    "ck": "Chaos Knight",
    "dk": "Dragon Knight",
    "et": "Elder Titan",
    "wisp": "Io",
    "lc": "Legion Commander",
    "ls": "Lifestealer",
    "naix": "Lifestealer",
    "sk": "Sand King",
    "sb": "Spirit Breaker",
    "ts": "Timbersaw",
    "tp": "Treant Protector",
    "tree": "Treant Protector",
    "wk": "Wraith King",
    "am": "Anti-Mage",
    "antimage": "Anti-Mage",
    "aw": "Arc Warden",
    "bs": "Bloodseeker",
    "bh": "Bounty Hunter",
    "dr": "Drow Ranger",
    "ld": "Lone Druid",
    "dusa": "Medusa",
    "potm": "Mirana",
    "mk": "Monkey King",
    "na": "Nyx Assassin",
    "pa": "Phantom Assassin",
    "pl": "Phantom Lancer",
    "sf": "Shadow Fiend",
    "ta": "Templar Assassin",
    "tb": "Terrorblade",
    "tw": "Troll Warlord",
    "vs": "Vengeful Spirit",
    "aa": "Ancient Apparition",
    "br": "Batrider",
    "cm": "Crystal Maiden",
    "ds": "Dark Seer",
    "dw": "Dark Willow",
    "dp": "Death Prophet",
    "carl": "Invoker",
    "kotl": "Keeper of the Light",
    "furion": "Nature's Prophet",
    "od": "Outworld Devourer",
    "qop": "Queen of Pain",
    "sd": "Shadow Demon",
    "rhasta": "Shadow Shaman",
    "sm": "Skywrath Mage",
    "wr": "Windranger",
    "ww": "Winter Wyvern",
    "wd": "Witch Doctor",
    "es": "Earthshaker",
    "kao": "Earth Spirit",
    "np": "Nature's Prophet",
    "fv": "Faceless Void",
    "gs": "Grimstroke"
}
