"""
0xB215F1 - 0x20 : skip first cutscene
BlackRose doesn't stop us from going to non-story areas
"""

import asyncio
from asyncio import sleep
from pcsx2_interface.pine import Pine
from enum import Enum
from typing import TypedDict, NotRequired

class InfectionEventBase(Enum):
    # _value_: InfectionEventAttributes

    @classmethod
    def from_address(self, address: int):
        for member in self:
            if member.value["address"] == address:
                return member
        return None

class Servers(Enum):
    """placeholder for server enum"""
    Delta = 1
    Theta = 2

class InfectionStoryEvents(InfectionEventBase):
    FirstDataBug = {"address": 0xa44f39, "bits": 0b00000100, "volumes": [1], "server": Servers.Delta}
    LearnGateHacking = {"address": 0xa44f52, "bits": 0b00000010, "volumes": [1], "server": Servers.Delta}
    SavedPiros = {"address": 0xa44f41, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    BoardProtected = {"address": 0xa44f5a, "bits": 0b00010000, "volumes": [1], "server": Servers.Delta}
    BlackRoseDungeon = {"address": 0xa44f6a, "bits": 0b00000100, "volumes": [1], "server": Servers.Theta}
    ElkMiaFavorite = {"address": 0xa44f71, "bits": 0b10000000, "volumes": [1], "server": Servers.Delta}
    PirosDiary = {"address": 0xa44f7b, "bits": 0b00100000, "volumes": [1], "server": Servers.Delta}
    MistralMeetUp = {"address": 0xa44f90, "bits": 0b00000001, "volumes": [1], "server": Servers.Theta}
    Epitaph00 = {"address": 0xa44f92, "bits": 0b00000001, "volumes": [1], "server": Servers.Theta}
    DescendentsOfFianna = {"address": 0xa44fa8, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    EpitaphQ = {"address": 0xa44fb0, "bits": 0b00000001, "volumes": [1], "server": Servers.Delta}
    MetMeg = {"address": 0xa44fb8, "bits": 0b00000001, "volumes": [1], "server": Servers.Theta}


class MutationStoryEvents(InfectionEventBase):
    DeadEndFirstDungeon = {"address": 0xb215f3, "bits": 0b00000001, "volumes": [2]}
    MiaElkEventsStart = {"address": 0xb21609, "bits": 0b00000010, "volumes": [2]}
    EncounteringDataBugBoss = {"address": 0xb21609, "bits": 0b00000100, "volumes": [2]}
    DataBugBossStart = {"address": 0xb21609, "bits": 0b00001000, "volumes": [2]}
    DataBugBossEndCutscene = {"address": 0xb21609, "bits": 0b00010000, "volumes": [2]}
    DataBugBossWarpingBackToTown = {"address": 0xb21609, "bits": 0b00100000, "volumes": [2]}
    MiaElkMissionEnd = {"address": 0xb21609, "bits": 0b01000000, "volumes": [2]}
    SheratonDataBugBossEncountered = {"address": 0xb21610, "bits": 0b00001000, "volumes": [2]}
    HelpSheratonKillDataBugBossStart = {"address": 0xb21610, "bits": 0b00010000, "volumes": [2]}
    HelpSheratonKillDataBugBossEnd = {"address": 0xb21611, "bits": 0b10000000, "volumes": [2]}
    SheratonDataBugBossMissionComplete = {"address": 0xb21617, "bits": 0b10000000, "volumes": [2]}
    ReportingToLios = {"address": 0xb21618, "bits": 0b00010000, "volumes": [2]}
    LiosLogsOut = {"address": 0xb21618, "bits": 0b00100000, "volumes": [2]}
    LiosInvestigationEmail = {"address": 0xb21620, "bits": 0b00010000, "volumes": [2]}
    LiosEmailConversationWithBlackRoseReplied = {"address": 0xb21620, "bits": 0b00100000, "volumes": [2]}
    ReceivedLiosCoreFromBlackRose = {"address": 0xb21620, "bits": 0b10000000, "volumes": [2]}
    ArrivedAtInfectedMap = {"address": 0xb21621, "bits": 0b00001000, "volumes": [2]}
    EnteredInfectedMapDungeon = {"address": 0xb21621, "bits": 0b00010000, "volumes": [2]}
    StrangeObjectDisappears = {"address": 0xb21621, "bits": 0b00100000, "volumes": [2]}
    StrangeObjectDisappearsAgain = {"address": 0xb21621, "bits": 0b10000000, "volumes": [2]}
    EnteredStrangeObjectDungeonFinalRoom = {"address": 0xb21622, "bits": 0b00000010, "volumes": [2]}
    StrangeObjectCutscene = {"address": 0xb21622, "bits": 0b00000100, "volumes": [2]}
    StrangeObjectFightStarts = {"address": 0xb21622, "bits": 0b00001000, "volumes": [2]}
    DataDrainedInnis = {"address": 0xb21622, "bits": 0b00010000, "volumes": [2]}
    InnisDefeated = {"address": 0xb21622, "bits": 0b00100000, "volumes": [2]}
    InnisDefeatCutscene = {"address": 0xb21622, "bits": 0b01000000, "volumes": [2]}
    InnisWarpedBackToTown = {"address": 0xb21622, "bits": 0b10000000, "volumes": [2]}
    ForcedShutdown = {"address": 0xb21623, "bits": 0b00000001, "volumes": [2]}
    LoggedOutAfterShutdown = {"address": 0xb21623, "bits": 0b00000100, "volumes": [2]}
    BraceletCutsceneAfterLogout = {"address": 0xb21623, "bits": 0b00100000, "volumes": [2]}
    StrongestPlayMistralCutscene = {"address": 0xb2162a, "bits": 0b00001000, "volumes": [2]}
    EnteringMistralDungeonFinalRoom = {"address": 0xb2162a, "bits": 0b00100000, "volumes": [2]}
    CubiaFightStart = {"address": 0xb2162a, "bits": 0b01000000, "volumes": [2]}
    CubiaFightEnd = {"address": 0xb2162b, "bits": 0b00000010, "volumes": [2]}
    CubiaDungeonOver = {"address": 0xb2162b, "bits": 0b00001000, "volumes": [2]}
    StartedDungeonWithPiros = {"address": 0xb21630, "bits": 0b00100000, "volumes": [2]}
    EncounteredMia = {"address": 0xb21630, "bits": 0b01000000, "volumes": [2]}
    PirosWarpBackToTown = {"address": 0xb21630, "bits": 0b10000000, "volumes": [2]}
    PirosVsCatComplete = {"address": 0xb21637, "bits": 0b10000000, "volumes": [2]}
    BlackRoseMentionsEpitaphOfTwilightThread = {"address": 0xb21638, "bits": 0b00100000, "volumes": [2]}
    EnteredEpitaph01Room = {"address": 0xb21640, "bits": 0b00100000, "volumes": [2]}
    LeavingEpitaph01Dungeon = {"address": 0xb21640, "bits": 0b01000000, "volumes": [2]}
    ReceivedEpitaph01 = {"address": 0xb21647, "bits": 0b10000000, "volumes": [2]}
    ArrivedAtWisemanScene = {"address": 0xb21649, "bits": 0b00000001, "volumes": [2]}
    WisemanLogsOut = {"address": 0xb21649, "bits": 0b00000010, "volumes": [2]}
    WisemanEpitaphOfTwilightQuestOver = {"address": 0xb2164f, "bits": 0b10000000, "volumes": [2]}
    DataBugMonsterWithWisemanItem = {"address": 0xb21651, "bits": 0b00000100, "volumes": [2]}
    ReturningToTownWithWisemanItem = {"address": 0xb21651, "bits": 0b00001000, "volumes": [2]}
    BalmungLiosCutscene = {"address": 0xb21651, "bits": 0b00100000, "volumes": [2]}
    GaveWisemanSparkSword = {"address": 0xb21652, "bits": 0b00000100, "volumes": [2]}
    LeavingWisemanDungeon = {"address": 0xb21652, "bits": 0b00001000, "volumes": [2]}
    WisemanMemberAddress = {"address": 0xb21657, "bits": 0b10000000, "volumes": [2]}
    WeirdGuyOnBoardCutscene = {"address": 0xb21659, "bits": 0b00000001, "volumes": [2]}
    PlairdRoomEntered = {"address": 0xb21659, "bits": 0b00000100, "volumes": [2]}
    LearnedNetSlumWhereabouts = {"address": 0xb2165f, "bits": 0b10000000, "volumes": [2]}
    ArrivedAtPulsatingWorstCore = {"address": 0xb21660, "bits": 0b01000000, "volumes": [2]}
    EnteredPulsatingWorstCoreDungeon = {"address": 0xb21660, "bits": 0b10000000, "volumes": [2]}
    NetSlumDungeonStartScene = {"address": 0xb21661, "bits": 0b00000001, "volumes": [2]}
    NetSlumEntrance = {"address": 0xb21661, "bits": 0b00001000, "volumes": [2]}
    WarpedToNetSlum = {"address": 0xb21661, "bits": 0b00010000, "volumes": [2]}
    ArrivedInNetSlum = {"address": 0xb21661, "bits": 0b00100000, "volumes": [2]}
    SpokeWithEveryoneAtNetSlumEntrance = {"address": 0xb21662, "bits": 0b00100000, "volumes": [2]}
    Phase3MasusFightStart = {"address": 0xb21662, "bits": 0b10000000, "volumes": [2]}
    Phase3Defeated = {"address": 0xb21667, "bits": 0b10000000, "volumes": [2]}
    MutationWin = {"address": 0xb2166f, "bits": 0b10000000, "volumes": [2]}


async def initial_state():
    pine = Pine()
    pine.connect()
    # pine.write_int8(0xB215F1, 0x20)
    pine.disconnect()

seen_events = set()

async def track_mutation_events():
    for event in MutationStoryEvents:
        address = event.value["address"]
        bits = event.value["bits"]
        current_value = pine.read_int8(address)
        if current_value & bits == 0:
            if event not in seen_events:
                print(f"Event {event.name} triggered at address {hex(address)} with bits {bin(bits)}")
                seen_events.add(event)

async def pcsx2_sync_task(ctx):
    game_state = 0x01
    print(pine.get_game_id())
    while True:
        game_curr = pine.read_int8(0xA83C80)
        if game_curr != game_state:
            game_state = game_curr
        await initial_state()
        await track_mutation_events()
        await sleep(0.5)

pine = Pine()
pine.connect()
if __name__ == "__main__":
    asyncio.run(pcsx2_sync_task(None))
