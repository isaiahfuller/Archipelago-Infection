import time
import asyncio
import math
from typing import Any
from asyncio import sleep
from .pcsx2_interface.pine import Pine
from .data.items.PartyMembers import InfectionPartyMembers as PartyMembers
from .data.items.AreaWords import InfectionAreaWords as AreaWords
from .data.items.Servers import InfectionServers as Servers
from .data.items.WordList import InfectionDeltaWordList as DeltaWordList, InfectionThetaWordList as ThetaWordList
from .data.GameState import InfectionGameState as GameState
from .data.Names import InfectionAreaWordNames as AreaWordNames
from .data.locations.CharacterStats import InfectionCharacterStats as CharacterStats
from .data.locations.Events import InfectionStoryEvents as StoryEvents
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components, launch_subprocess, Type

current_word_list: set[DeltaWordList | ThetaWordList] = set()
unlocked_word_list: set[DeltaWordList | ThetaWordList] = set()
pine = Pine()

# Basically everything except keywords comes from RetroAchievements
# https://retroachievements.org/codenotes.php?g=19021


def initial_state() -> None:
    # Unlock Orca & BlackRose, keywords, and set flags
    modify_party_member(PartyMembers.Orca)
    modify_party_member(PartyMembers.BlackRose)
    modify_word(AreaWords.Bursting)
    modify_word(AreaWords.PassedOver)
    modify_word(AreaWords.AquaField)
    modify_word(AreaWords.Hidden)
    modify_word(AreaWords.Forbidden)
    modify_word(AreaWords.HolyGround)
    current_word_list.add(DeltaWordList.BurstingPassedOverAquaField)
    current_word_list.add(DeltaWordList.HiddenForbiddenHolyGround)
    unlocked_word_list.add(DeltaWordList.BurstingPassedOverAquaField)
    unlocked_word_list.add(DeltaWordList.HiddenForbiddenHolyGround)
    modify_server(Servers.Delta)
    pine.write_int8(StoryEvents.FirstLogin, pine.read_int8(
        StoryEvents.FirstLogin) | 0b11111111)  # 0b00000111
    pine.write_int8(StoryEvents.BattleTutorial,
                    pine.read_int8(StoryEvents.BattleTutorial) | 0b00100101)
    pine.write_int8(StoryEvents.Coma, pine.read_int8(
        StoryEvents.Coma) | 0b01000000)
    pine.write_int8(StoryEvents.DungeonTutorial,
                    pine.read_int8(StoryEvents.DungeonTutorial) | 0b11110100)
    pine.write_int8(StoryEvents.FirstAura,
                    pine.read_int8(StoryEvents.FirstAura) | 0b00000011)
    pine.write_int8(StoryEvents.FirstAuraScene2,
                    pine.read_int8(StoryEvents.FirstAuraScene2) | 0b10000000)
    pine.write_int8(StoryEvents.MetBlackRose,
                    pine.read_int8(StoryEvents.MetBlackRose) | 0b00010101)
    pine.write_int8(StoryEvents.Cathedral,
                    pine.read_int8(StoryEvents.Cathedral) | 0b00010100)


def modify_server(server: Servers, lock: bool = False) -> None:
    addr: int = 0xa41c04
    unlocked_servers: int = pine.read_int8(addr)
    if lock:
        pine.write_int8(addr, unlocked_servers & ~(2**server))
    else:
        pine.write_int8(addr, unlocked_servers | 2**server)

# Unlocking individual words
# Starting address: 0xA44C0C
# bitflags follow ids as listed here
# https://docs.google.com/spreadsheets/d/1IdsxywkwXuPe8qpa78Mv2pltIfw41fSOHPYw_3bGdGk/edit?gid=642441784#gid=642441784


def modify_word(word: AreaWords, lock: bool = False) -> None:
    offset: int = math.floor(word / 8)
    unlocked_words: int = pine.read_int8(offset + 0xa44c0c)
    if lock:
        pine.write_int8(offset + 0xa44c0c, unlocked_words & ~(2 ** (word % 8)))
    else:
        pine.write_int8(offset + 0xa44c0c, unlocked_words | 2 ** (word % 8))


def modify_party_member(member: PartyMembers, lock: bool = False) -> None:
    addr: int = 0xa41bf0
    offset: int = math.floor(member / 8)
    unlocked_members: int = pine.read_int8(offset + addr)
    if lock:
        pine.write_int8(offset + addr, unlocked_members & ~(2 ** (member % 8)))
    else:
        pine.write_int8(offset + addr, unlocked_members | 2 ** (member % 8))


# Dealing with word list
# Word list starts at 0x00A44C48
# Values are 16 bit, first byte can be set to 0xff to hide entry or 0x00 to show
# Second byte is the word id
# First world (Bursting Passed Over Aqua Field) is 0F, second (Hidden Forbidden Holy Ground) is 0E
# delta addr: 0xa44c47 - 0xa44cc6
# theta addr: 0xa44cc9 - 0xa44d46
def scan_word_list() -> None:
    starting_addr: int = 0xa44d46
    ending_addr: int = 0xa44c47

    for i in range(starting_addr, ending_addr, -1):
        current_addr: int = pine.read_int8(i)
        delta_member: DeltaWordList | None = DeltaWordList.from_address(
            current_addr)
        if delta_member:
            if delta_member in current_word_list:
                if delta_member not in unlocked_word_list:
                    pine.write_int8(i + 1, 0xff)
                    for word in delta_member.value["words"]:
                        modify_word(word, True)
                else:
                    pine.write_int8(i + 1, 0x00)
                    for word in delta_member.value["words"]:
                        modify_word(word, False)
            else:
                current_word_list.add(delta_member)
                pine.write_int8(i + 1, 0x00)
                words = []
                for word in delta_member.value["words"]:
                    modify_word(word, False)
                    words.append(AreaWordNames[word.name].value)
                print(
                    f"New Delta Word: {words[0]} {words[1]} {words[2]}")
            continue
        theta_member: ThetaWordList | None = ThetaWordList.from_address(
            current_addr)
        if theta_member:
            if theta_member in current_word_list:
                if theta_member not in unlocked_word_list:
                    pine.write_int8(i + 1, 0xff)
                    for word in theta_member.value["words"]:
                        modify_word(word, True)
                else:
                    pine.write_int8(i + 1, 0x00)
                    for word in theta_member.value["words"]:
                        modify_word(word, False)
            else:
                current_word_list.add(theta_member)
                pine.write_int8(i + 1, 0x00)
                words = []
                for word in theta_member.value["words"]:
                    modify_word(word, False)
                    words.append(AreaWordNames[word.name].value)
                print(f"New Theta Word: {words[0]} {words[1]} {words[2]}")


async def pcsx2_sync_task(ctx):
    game_state = 0x01
    pine.connect()
    print(pine.get_game_id())
    while True:
        if pine.read_int8(0xa3f5f0) != game_state:
            game_state = pine.read_int8(0xa3f5f0)
            print('Game state: ' + GameState(game_state).name)
            initial_state()
        if GameState(pine.read_int8(0xa3f5f0)) == GameState.TitleScreen:
            current_word_list.clear()
        scan_word_list()
        await sleep(0.5)
    pine.disconnect()

if __name__ == "__main__":
    asyncio.run(pcsx2_sync_task(None))
