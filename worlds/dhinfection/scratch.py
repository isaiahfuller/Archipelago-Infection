import time
import asyncio
import math
from enum import Enum
from typing import Any
from asyncio import sleep
from pcsx2_interface.pine import Pine
from data.GameState import InfectionGameState as GameState
# from data.items.PartyMembers import InfectionPartyMembers as PartyMembers
# from data.items.AreaWords import InfectionAreaWords as AreaWords
# from data.items.Servers import InfectionServers as Servers
# from data.items.WordList import InfectionDeltaWordList as DeltaWordList, InfectionThetaWordList as ThetaWordList
# from data.GameState import InfectionGameState as GameState
# from data.Names import InfectionAreaWordNames as AreaWordNames
# from data.locations.CharacterStats import InfectionCharacterStats as CharacterStats
# from data.locations.Events import InfectionStoryEvents as StoryEvents
# from worlds.AutoWorld import World, WebWorld
# from worlds.LauncherComponents import Component, components, launch_subprocess, Type

class PartyMemberBase(Enum):
    @classmethod
    def from_id(self, id: int):
        for member in self:
            if member.value["id"] == id:
                return member
        return None


class PartyMembers(PartyMemberBase):
    Mia = {"id": 1}
    Orca = {"id": 2}
    Marlo = {"id": 3}
    Sanjuro = {"id": 4}
    NukeUsagimaru = {"id": 5}
    Balmung = {"id": 6}
    Moonstone = {"id": 7}
    Piros = {"id": 8}
    Wiseman = {"id": 9}
    Elk = {"id": 10}
    Natsume = {"id": 11}
    Rachel = {"id": 12}
    Gardenia = {"id": 13}
    TerajimaRyoko = {"id": 14}
    BlackRose = {"id": 15}
    Mistral = {"id": 16}
    Helba = {"id": 17}

class AreaWordListBase(Enum):
    def from_id(self, id: int):
        for member in self:
            if member.value["id"] == id:
                return member
        return None

    # def from_importance(self, importance: ItemClassification):
    #     return [member for member in self if member.value["importance"] == importance]


class AreaWords(AreaWordListBase):
    Bursting = {"id": 0}
    Hidden = {"id": 1}
    Expansive = {"id": 2}
    Boundless = {"id": 3}
    Closed = {"id": 4}
    Quiet = {"id": 5}
    Plenteous = {"id": 6}
    Collapsed = {"id": 7}
    Cursed = {"id": 8}
    Buried = {"id": 9}
    Lonely = {"id": 10}
    Great = {"id": 11}
    Chosen = {"id": 12}
    PassedOver = {"id": 13}
    Forbidden = {"id": 14}
    Haunted = {"id": 15}
    Corrupted = {"id": 16}
    Oblivious = {"id": 17}
    Eternal = {"id": 18}
    Smiling = {"id": 19}
    Momentary = {"id": 20}
    Despaired = {"id": 21}
    Pagan = {"id": 22}
    Silent = {"id": 23}
    Distant = {"id": 24}
    Hopeless = {"id": 25}
    AquaField = {"id": 26}
    HolyGround = {"id": 27}
    SeaOfSand = {"id": 28}
    FortWalls = {"id": 29}
    TwinHills = {"id": 30}
    WhiteDevil = {"id": 31}
    Hypha = {"id": 32}
    Spiral = {"id": 33}
    Paradise = {"id": 34}
    FierySands = {"id": 35}
    GreatSeal = {"id": 36}
    FertileLand = {"id": 37}
    Nothingness = {"id": 38}
    SoaringSky = {"id": 39}
    Dolorous = {"id": 40}
    Nameless = {"id": 41}
    Resurrecting = {"id": 42}
    Merciless = {"id": 43}
    Dying = {"id": 44}
    Dazzling = {"id": 45}
    Blooming = {"id": 46}
    Scattering = {"id": 47}
    Pulsating = {"id": 48}
    Bounded = {"id": 49}
    EvilEyed = {"id": 50}
    Seekers = {"id": 51}
    Confused = {"id": 52}
    Grieving = {"id": 53}
    Madness = {"id": 54}
    Sages = {"id": 55}
    Promised = {"id": 56}
    Fossils = {"id": 57}
    Worst = {"id": 58}
    Widow = {"id": 59}
    Prairie = {"id": 60}
    Judgment = {"id": 61}
    Furnace = {"id": 62}
    HauntedLand = {"id": 63}
    Arctic = {"id": 64}
    Walkway = {"id": 65}
    Milestone = {"id": 66}
    Core = {"id": 67}
    Chatting = {"id": 68}
    Tested = {"id": 69}
    Turbulent = {"id": 70}
    Rising = {"id": 71}
    Sorrowful = {"id": 72}
    Fleeting = {"id": 73}
    Resonating = {"id": 74}
    Snaring = {"id": 75}
    Quicksilver = {"id": 76}
    Distrusting = {"id": 77}
    Implacable = {"id": 78}
    Sweltering = {"id": 79}
    Fallow = {"id": 80}
    FalseWord = {"id": 81}
    Twins = {"id": 82}
    Valkyrie = {"id": 83}
    IceWall = {"id": 84}
    SippingBug = {"id": 85}
    Arena = {"id": 86}
    Chaos = {"id": 87}
    Grasslands = {"id": 88}
    Bigoted = {"id": 89}
    Screaming = {"id": 90}
    Cruel = {"id": 91}
    Splendid = {"id": 92}
    Dreaming = {"id": 93}
    Muted = {"id": 94}
    Rotting = {"id": 95}
    Graceful = {"id": 96}
    Reincarnated = {"id": 97}
    Snowflakes = {"id": 98}
    WindSands = {"id": 99}
    VengefulOne = {"id": 100}
    Emerald = {"id": 101}
    Moonlit = {"id": 102}
    Starving = {"id": 103}
    Countless = {"id": 104}
    Tempting = {"id": 105}
    Purgatorial = {"id": 106}
    Capsule = {"id": 107}
    FateCastle = {"id": 108}
    Scars = {"id": 109}
    Nobleman = {"id": 110}
    Gravestone = {"id": 111}
    DrySea = {"id": 112}
    Sacrifice = {"id": 113}
    FallenAngel = {"id": 114}
    Altar = {"id": 115}
    Discovered = {"id": 116}
    Indiscreet = {"id": 117}
    Putrid = {"id": 118}
    Hideous = {"id": 119}
    Soft = {"id": 120}
    Beautiful = {"id": 121}
    Raging = {"id": 122}
    Noisy = {"id": 123}
    DogDancing = {"id": 124}
    Rejecting = {"id": 125}
    Sleepy = {"id": 126}
    Sinking = {"id": 127}
    Greedy = {"id": 128}
    Voluptuous = {"id": 129}
    Detestable = {"id": 130}
    Chronicling = {"id": 131}
    Primitive = {"id": 132}
    Gluttonous = {"id": 133}
    HotBlooded = {"id": 134}
    Destroyers = {"id": 135}
    Solitary = {"id": 136}
    Someones = {"id": 137}
    Her = {"id": 138}
    Laws = {"id": 139}
    Talisman = {"id": 140}
    Orange = {"id": 141}
    OrganMarket = {"id": 142}
    Agonizing = {"id": 143}
    Geothermal = {"id": 144}
    Golden = {"id": 145}
    Melody = {"id": 146}
    Remnant = {"id": 147}
    March = {"id": 148}
    Giant = {"id": 149}
    Touchstone = {"id": 150}
    SunnyDemon = {"id": 151}
    Messenger = {"id": 152}
    Scent = {"id": 153}
    NewTruth = {"id": 154}
    Gate = {"id": 155}
    Pilgrimage = {"id": 156}
    Scaffold = {"id": 157}
    FarThunder = {"id": 158}
    TriPansy = {"id": 159}
    TreasureGem = {"id": 160}
    Passionate = {"id": 296}

    
class ExtraAreaWords(AreaWordListBase):
    Stalking = {"id": 161}
    Bitter = {"id": 162}
    Barking = {"id": 163}
    Reckless = {"id": 164}
    Perceived = {"id": 165}
    Generous = {"id": 166}
    Obedient = {"id": 167}
    Outpouring = {"id": 168}
    Capricious = {"id": 169}
    Predatory = {"id": 170}
    Entwined = {"id": 171}
    Abrasive = {"id": 172}
    Lightless = {"id": 173}
    Shapeless = {"id": 174}
    Bottomless = {"id": 175}
    Guffawing = {"id": 176}
    LightTrap = {"id": 177}
    Soul = {"id": 178}
    Dusk = {"id": 179}
    Bemused = {"id": 180}
    Astigmatic = {"id": 181}
    Fatal = {"id": 182}
    Unending = {"id": 183}
    Survivors = {"id": 184}
    Sacred = {"id": 185}
    Miracle = {"id": 186}
    His = {"id": 187}
    Ghostly = {"id": 188}
    VengefulTwo = {"id": 189}
    Fantasy = {"id": 190}
    DeadLands = {"id": 191}
    Limit = {"id": 192}
    Kaleidoscope = {"id": 193}
    Impulse = {"id": 194}
    Feeling = {"id": 195}
    Corridor = {"id": 196}
    Drift = {"id": 197}
    CatMarket = {"id": 198}
    Sanctum = {"id": 199}
    Footstep = {"id": 200}
    Remains = {"id": 201}
    Cabbage = {"id": 202}
    SandTrap = {"id": 203}
    RawOre = {"id": 204}
    MirrorWorld = {"id": 205}
    Attracting = {"id": 206}
    Spun = {"id": 207}
    Lost = {"id": 208}
    Incessant = {"id": 209}
    Seeding = {"id": 210}
    Clean = {"id": 211}
    Solemn = {"id": 212}
    Unusual = {"id": 213}
    Dripping = {"id": 214}
    Ancient = {"id": 215}
    Billowing = {"id": 216}
    Jealous = {"id": 217}
    Mimic = {"id": 218}
    Corroded = {"id": 219}
    Cracked = {"id": 220}
    Fated = {"id": 221}
    SeaofCloud = {"id": 222}
    Morphean = {"id": 223}
    HardRoe = {"id": 224}
    Prejudiced = {"id": 225}
    Loose = {"id": 226}
    Lifeless = {"id": 227}
    SunColored = {"id": 228}
    Your = {"id": 229}
    Relativistic = {"id": 230}
    HalfBoiled = {"id": 231}
    Festive = {"id": 232}
    Gamblers = {"id": 233}
    Bloody = {"id": 234}
    Windmills = {"id": 235}
    Neigh = {"id": 236}
    FiveHundredLohan = {"id": 237}
    Trajectory = {"id": 238}
    Projection = {"id": 239}
    Alchemy = {"id": 240}
    Crossroad = {"id": 241}
    RingingEars = {"id": 242}
    HogsRun = {"id": 243}
    EbbandFlow = {"id": 244}
    Tragedy = {"id": 245}
    Ridgeline = {"id": 246}
    Clavicle = {"id": 247}
    Compass = {"id": 248}
    Battlefield = {"id": 249}
    Whale = {"id": 250}
    Intimidating = {"id": 251}
    Sickened = {"id": 252}
    Plundered = {"id": 253}
    Excessive = {"id": 254}
    Strayed = {"id": 255}
    Vaguely = {"id": 256}
    Secretive = {"id": 257}
    Sleepless = {"id": 258}
    Mysterious = {"id": 259}
    Writhing = {"id": 260}
    Unspeakable = {"id": 261}
    Strange = {"id": 262}
    Unenduring = {"id": 263}
    Breezing = {"id": 264}
    Unmatched = {"id": 265}
    Imprisoned = {"id": 266}
    Disgraced = {"id": 267}
    ForestGreen = {"id": 268}
    AbyssPossessive = {"id": 269}
    Desperate = {"id": 270}
    Farewell = {"id": 271}
    Mythical = {"id": 272}
    Satisfying = {"id": 273}
    My = {"id": 274}
    Illusionary = {"id": 275}
    BirdGrammar = {"id": 276}
    Reborn = {"id": 277}
    Elusive = {"id": 278}
    Travelers = {"id": 279}
    Pseudo = {"id": 280}
    Fort = {"id": 281}
    StrayBull = {"id": 282}
    Excavation = {"id": 283}
    Duel = {"id": 284}
    SecretTower = {"id": 285}
    PureDefense = {"id": 286}
    DownyGrowth = {"id": 287}
    SafeHaven = {"id": 288}
    LyricPoet = {"id": 289}
    Code = {"id": 290}
    Treasury = {"id": 291}
    NightGrass = {"id": 292}
    Crack = {"id": 293}
    Frontline = {"id": 294}
    Den = {"id": 295}
    Abyss = {"id": 297}
    Truths = {"id": 298}
    Wavemaster = {"id": 299}
    Betrayed = {"id": 300}
    Knights = {"id": 301}
    Virgin = {"id": 302}
    FacingMirrors = {"id": 303}

    # Note: Does not unlock properly, seems to be replaced with "Beginning" in Infection
    Darkside = {"id": 304}

# current_word_list: set[DeltaWordList | ThetaWordList] = set()
# unlocked_word_list: set[DeltaWordList | ThetaWordList] = set()
pine = Pine()

# Basically everything except keywords comes from RetroAchievements
# https://retroachievements.org/codenotes.php?g=19021

# 0x00 = not received, 0x02 = read, 0x04 = read
def email_state(offset: int, value: int | None = None) -> int | None:
    BASE_ADDR: int = 0xa41c34
    # print(f"Email state: {hex(BASE_ADDR + offset)}: {bin(pine.read_int8(BASE_ADDR + offset))}")
    if value is None:
        return pine.read_int8(BASE_ADDR + offset)
    pine.write_int8(BASE_ADDR + offset, value)

def watch_emails() -> None:
    """Reads all received emails"""
    BASE_ADDR: int = 0xa41c34
    for i in range(0, 0x140):
        curr = email_state(i)
        if curr == 2:
            email_state(i, 4)

def initial_state() -> None:
    """"""
    # # Read emails before meeting Orca
    # email_state(0x04, 4) # Registered yet?
    # email_state(0x05, 4) # Thank You
    # email_state(0x140, 4) # Version update

    # Unlock Orca, Mia, BlackRose
    pine.write_int8(0xa41bf0, pine.read_int8(0xa41bf0) | 0b00000100)
    pine.write_int8(0xa41bf1, pine.read_int8(0xa41bf1) | 0b10000000)
    # pine.write_int8(0xa44ed7, pine.read_int8(
    #     0xa44ed7) | 0b00000111)  # Not needed when setting emails read

    # Unlock Data Drain
    pine.write_int8(0xA46141, 1) # Unlock Data Drain skill category
    pine.write_int8(0xA41894, 2) # Unlock Data Drain, use red dye

    modify_party_member(PartyMembers.Orca, False)
    # modify_party_member(PartyMembers.BlackRose, False)
    modify_word(AreaWords.Bursting, False)
    modify_word(AreaWords.PassedOver, False)
    modify_word(AreaWords.AquaField, False)
    modify_word(AreaWords.Hidden, False)
    modify_word(AreaWords.Forbidden, False)
    modify_word(AreaWords.HolyGround, False)

    # Give Ryu Books
    pine.write_int8(0xA407DD , 1)
    pine.write_int8(0xA407DE , 1)
    pine.write_int8(0xA407DF , 1)
    pine.write_int8(0xA407E0 , 1)
    pine.write_int8(0xA407E1 , 1)
    pine.write_int8(0xA407E2 , 1)
    pine.write_int8(0xA407E3 , 1)
    pine.write_int8(0xA407E4 , 1)
    

    # Skip meeting Orca
    pine.write_int8(0xa44ed7, pine.read_int8(
        0xa44ed7) | 0b11000000)
    pine.write_int8(0xa44ed8, pine.read_int8(
        0xa44ed8) | 0b00000111)
    pine.write_int8(0xa44edf, pine.read_int8(
        0xa44edf) | 0b11000000)
    pine.write_int8(0xa44ee0,
                    pine.read_int8(0xa44ee0) | 0b00100101)
    pine.write_int8(0xa44ee7, pine.read_int8(
        0xa44ee7) | 0b01000000)
    pine.write_int8(0xa44ee8,
                    pine.read_int8(0xa44ee8) | 0b11110100)
    pine.write_int8(0xa44ee9,
                    pine.read_int8(0xa44ee9) | 0b00000011)
    pine.write_int8(0xa44eef,
                    pine.read_int8(0xa44eef) | 0b10000000)
    
    # Skip BlackRose cutscene and Hidden Forbidden Holy Ground
    pine.write_int8(0xa44f20,
                    pine.read_int8(0xa44f20) | 0xff) # 0b11010101, b5 blocks gate w/o cutscene
    pine.write_int8(0xa44f22,
                    pine.read_int8(0xa44f22) | 0xff)
    pine.write_int8(0xa44f23,
                    pine.read_int8(0xa44f23) | 0b00000001)
    pine.write_int8(0xa44f27,
                    pine.read_int8(0xa44f27) | 0b10000000)

    # Get Mia and Elk out of your way
    pine.write_int8(0xa44f58, pine.read_int8(0xa44f58) | 0xff)


# def modify_server(server: Servers, lock: bool = False) -> None:
#     addr: int = 0xa41c04
#     unlocked_servers: int = pine.read_int8(addr)
#     if lock:
#         pine.write_int8(addr, unlocked_servers & ~(2**server))
#     else:
#         pine.write_int8(addr, unlocked_servers | 2**server)

# Unlocking individual words
# Starting address: 0xA44C0C
# bitflags follow ids as listed here
# https://docs.google.com/spreadsheets/d/1IdsxywkwXuPe8qpa78Mv2pltIfw41fSOHPYw_3bGdGk/edit?gid=642441784#gid=642441784


def modify_word(word: AreaWords, lock: bool = False) -> None:
    offset: int = math.floor(word.value["id"] / 8)
    unlocked_words: int = pine.read_int8(offset + 0xa44c0c)
    if lock:
        pine.write_int8(offset + 0xa44c0c, unlocked_words & ~(2 ** (word.value["id"] % 8)))
    else:
        pine.write_int8(offset + 0xa44c0c, unlocked_words | 2 ** (word.value["id"] % 8))


def modify_party_member(member: PartyMembers, lock: bool = False) -> None:
    addr: int = 0xa41bf0
    offset: int = math.floor(member.value["id"] / 8)
    unlocked_members: int = pine.read_int8(offset + addr)
    if lock:
        pine.write_int8(offset + addr, unlocked_members & ~(2 ** (member.value["id"] % 8)))
    else:
        pine.write_int8(offset + addr, unlocked_members | 2 ** (member.value["id"] % 8))


# Dealing with word list
# Word list starts at 0x00A44C48
# Values are 16 bit, first byte can be set to 0xff to hide entry or 0x00 to show
# Second byte is the word id
# First world (Bursting Passed Over Aqua Field) is 0F, second (Hidden Forbidden Holy Ground) is 0E
# delta addr: 0xa44c47 - 0xa44cc6
# theta addr: 0xa44cc9 - 0xa44d46
# def scan_word_list() -> None:
#     starting_addr: int = 0xa44d46
#     ending_addr: int = 0xa44c47

#     for i in range(starting_addr, ending_addr, -1):
#         current_addr: int = pine.read_int8(i)
#         delta_member: DeltaWordList | None = DeltaWordList.from_address(
#             current_addr)
#         if delta_member:
#             if delta_member in current_word_list:
#                 if delta_member not in unlocked_word_list:
#                     pine.write_int8(i + 1, 0xff)
#                     for word in delta_member.value["words"]:
#                         modify_word(word, True)
#                 else:
#                     pine.write_int8(i + 1, 0x00)
#                     for word in delta_member.value["words"]:
#                         modify_word(word, False)
#             else:
#                 current_word_list.add(delta_member)
#                 pine.write_int8(i + 1, 0x00)
#                 words = []
#                 for word in delta_member.value["words"]:
#                     modify_word(word, False)
#                     words.append(AreaWordNames[word.name].value)
#                 print(
#                     f"New Delta Word: {words[0]} {words[1]} {words[2]}")
#             continue
#         theta_member: ThetaWordList | None = ThetaWordList.from_address(
#             current_addr)
#         if theta_member:
#             if theta_member in current_word_list:
#                 if theta_member not in unlocked_word_list:
#                     pine.write_int8(i + 1, 0xff)
#                     for word in theta_member.value["words"]:
#                         modify_word(word, True)
#                 else:
#                     pine.write_int8(i + 1, 0x00)
#                     for word in theta_member.value["words"]:
#                         modify_word(word, False)
#             else:
#                 current_word_list.add(theta_member)
#                 pine.write_int8(i + 1, 0x00)
#                 words = []
#                 for word in theta_member.value["words"]:
#                     modify_word(word, False)
#                     words.append(AreaWordNames[word.name].value)
#                 print(f"New Theta Word: {words[0]} {words[1]} {words[2]}")


seen_events: set[int] = set()

class Events(Enum):
    # EmailsReadEvent001 = {"addr": 0xa44ed7, "mask": 0b11000000}
    # FirstLoginEvent002 = {"addr": 0xa44ed8, "mask": 0b00100000}
    # LoadedBPOAFieldEvent003 = {"addr": 0xa44edf, "mask": 0b11000000}
    ComaEvent007 = {"addr": 0xa44eef, "mask": 0b10000000}
    BookTwilightEvent012 = {"addr": 0xa44f23, "mask": 0b00000001}
    # Expansive Haunted Sea of Sand - Dungeon Entrance
    AdminBlockingPathEvent015 = {"addr": 0xa44f38, "mask": 0b01000000}
    # Triggers at the start of the fight? - Only use defeat bit
    EHSoSEvent015 = {"addr": 0xa44f39, "mask": 0b00000100}
    # Given list before: Indiscreet Gluttonous Pilgrimage
    PirosEvent016 = {"addr": 0xa44f41, "mask": 0b00000001}
    # Boundless Corrupted Fort Walls - Solo
    GateHackingEvent018 = {"addr": 0xa44f52, "mask": 0b00000010}
    # Closed Oblivious Twin Hills - Mia and Elk
    GateHackingEvent019 = {"addr": 0xa44f5a, "mask": 0b00010000}
    # Quiet Eternal White Devil - Not as shown on RA
    BlackRoseDungeonEvent020 = {"addr": 0xa44f6a, "mask": 0b00000101}
    # Plenteous Smiling Hypha - Elk
    ElkMiaFavEvent021 = {"addr": 0xa44f71, "mask": 0b10000000}
    # Putrid Hot-blooded Scaffold - Piros
    PirosDiaryEvent022 = {"addr": 0xa44f7b, "mask": 0b00100000}
    # Collapsed Momentary Spiral - Mistral
    MistralEvent023 = {"addr": 0xa44f90, "mask": 0b00000001}
    # Cursed Despaired Paradise - BlackRose
    EpitaphEvent024 = {"addr": 0xa44f92, "mask": 0b00000001}
    # Buried Pagan Fiery Sands
    FiannaEvent025 = {"addr": 0xa44fa8, "mask": 0b00000001}
    # Lonely Silent Great Seal
    EpitaphEvent026 = {"addr": 0xa44fb0, "mask": 0b00000001}
    # Great Distant Fertile Land - BlackRose
    MeetAlfEventUnl = {"addr": 0xa44fb8, "mask": 0b00000001}
    # Chosen Hopeless Nothingness
    FinishedGameEvent027 = {"addr": 0xa44fc0, "mask": 0b00000001}

    # Ones I didn't track
    # Natsume's event - Raging Passionate Melody

async def pcsx2_sync_task(ctx):
    # pine = Pine()
    game_state = 0x01
    pine.connect()
    print(pine.get_game_id())
    email_state = 0b00000000
    while True:
        watch_emails()
        game_curr = pine.read_int8(0xa3f5f0)
        if game_curr not in GameState:
            continue
        if game_curr != game_state:
            game_state = game_curr
            # print('Game state: ' + GameState(game_state).name)
        initial_state()
        # if GameState(pine.read_int8(0xa3f5f0)) == GameState.TitleScreen:
            # current_word_list.clear()
        # scan_word_list()
        email_curr = pine.read_int8(0xa41c38)
        if email_state != email_curr:
            email_state = email_curr
            print(bin(email_state))

        book_of_law = pine.read_int8(0xa40708)
        if book_of_law == 0:
            pine.write_int8(0xa40708, 1)
        await sleep(0.5)
        for event in Events:
            if pine.read_int8(event.value["addr"]) & event.value["mask"] and event not in seen_events:
                seen_events.add(event)
                print(f"Event {event.name} triggered")
        
    pine.disconnect()

if __name__ == "__main__":
    asyncio.run(pcsx2_sync_task(None))
