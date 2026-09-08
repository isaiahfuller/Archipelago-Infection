from enum import Enum
from BaseClasses import ItemClassification
from ..locations.PlayStats import PlayStats


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
    RyuBookIV = []
    RyuBookV = []
    RyuBookVI = [PlayStats.GottOpened, PlayStats.ChestsOpened, PlayStats.BreakablesBroken]
    RyuBookVII = [PlayStats.SymbolsActivated]
    RyuBookVIII = [PlayStats.GoldenEgg, PlayStats.BloodyEgg, PlayStats.ImmatureEgg, PlayStats.InvisibleEgg, PlayStats.BearCatEgg, PlayStats.OhNoMelon, PlayStats.Cordyceps, PlayStats.LaPumpkin, PlayStats.WhiteCherry, PlayStats.TwilightOnion, PlayStats.SnakyCactus, PlayStats.PineyApple, PlayStats.Mushroom, PlayStats.Mandragora, PlayStats.GruntMints, PlayStats.RootVegetable]
