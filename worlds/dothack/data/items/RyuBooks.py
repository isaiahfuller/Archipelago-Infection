from enum import Enum
from BaseClasses import ItemClassification
from ..locations.PlayStats import PlayStats, MonsterHuntInfection


class RyuBooks(Enum):
    """
    Present in all volumes.
    Unlocks playstats associated with them in-game.
    """
    @classmethod
    def from_id(cls, id: int):
        for book in cls:
            if book.value["id"] == id:
                return book
        return None

    @classmethod
    def get_by_stat(cls, stat: PlayStats):
        for book in cls:
            if isinstance(book.value, list) and stat in book.value:
                return book
        return None

    RyuBookI = [PlayStats.AreasVisited]
    RyuBookII = [PlayStats.PortalsOpened, PlayStats.AllFieldPortalsOpened, PlayStats.AllDungeonPortalsOpened]
    RyuBookIII = []
    RyuBookIV = [MonsterHuntInfection]
    RyuBookV = []
    RyuBookVI = [PlayStats.GottOpened, PlayStats.ChestsOpened, PlayStats.BreakablesBroken]
    RyuBookVII = [PlayStats.SymbolsActivated]
    RyuBookVIII = []
