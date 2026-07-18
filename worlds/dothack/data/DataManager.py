from dataclasses import dataclass, field
from typing import List, Dict, Any, Type
from .Addresses import VolumeAddresses, InfectionAddresses, MutationAddresses, OutbreakAddresses, QuarantineAddresses


@dataclass
class VolumeData:
    volume: int
    addresses: Type[VolumeAddresses]
    event_locations: List[Any] = field(default_factory=list)
    wordlist_locations: List[Any] = field(default_factory=list)
    wordlist_items: List[Any] = field(default_factory=list)
    party_member_items: List[Any] = field(default_factory=list)
    server_items: List[Any] = field(default_factory=list)
    items: List[Any] = field(default_factory=list)
    monster_locations: List[Any] = field(default_factory=list)


VOLUME_DATA: Dict[int, VolumeData] = {
    1: VolumeData(volume=1, addresses=InfectionAddresses),
    2: VolumeData(volume=2, addresses=MutationAddresses),
    3: VolumeData(volume=3, addresses=OutbreakAddresses),
    4: VolumeData(volume=4, addresses=QuarantineAddresses),
}
