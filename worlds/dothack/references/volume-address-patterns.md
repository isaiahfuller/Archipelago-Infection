# Address patterns between .hack volumes

Comparison recorded on 2026-09-27 using `data/Addresses.py` and the bundled
RetroAchievements HTML code notes. Verification status below incorporates
subsequent user testing; addresses without confirmation remain inferred.

## Shared player-data offset

All 155 compared player-data addresses follow a fixed offset from Infection:
28 items, 10 play stats, 115 monsters, party unlocks, and server unlocks.

| Volume | Offset from Infection |
| --- | ---: |
| Mutation | `+0xDC400` |
| Outbreak | `+0x43100` |
| Quarantine | `-0xC0380` |

For these fields, `volume_address = infection_address + volume_offset`.
This suggests that the corresponding player-data layouts retain their relative
positions across volumes. It does not establish a universal offset for all game
memory.

## Candidate addresses and verification status

These addresses result from applying the player-data offsets to Infection's
existing fields. All Outbreak and Quarantine candidates
in this table remain unverified.

| Field | Infection reference | Mutation confirmed | Outbreak candidate | Quarantine candidate |
| --- | --- | --- | --- | --- |
| `Storage` | `0xA40540` | `0xB1C940` | `0xA83640` | `0x9801C0` |
| `AreaWords` | `0xA44C0C` | `0xB2100C` | `0xA87D0C` | `0x98488C` |
| `WordLists` | `0xA44C47` | `0xB21047` | `0xA87D47` | `0x9848C7` |
| `LastItemIdx` | `0xA44EC8` | `0xB212C8` | `0xA87FC8` | `0x984B48` |


## Exceptions and limits

- `IngameStatus` does not follow the player-data offset. Runtime state and
  overlay addresses need separate searches.
- `LastItemIdx` is client-written bookkeeping. A corresponding offset does not
  establish that those bytes are unused by the game or safe to reuse.
- Event flags and shop/trade mappings require verification of their meanings
  and layouts, even if surrounding memory follows the same offset.
- These patterns do not establish complete support for the later volumes.

## Suggested verification

1. Inspect memory around a candidate address before a controlled action.
2. Perform one action, such as storing an item, unlocking one area word, or
   receiving one word list.
3. Compare memory afterward and confirm the expected byte or bit changed.
4. Check the data width and layout against the client's reads and writes.
   For example, the existing storage code uses four-byte entries with quantity
   at offset `+3`; word unlocks use individual bits.
5. Repeat across relevant save/load and game-state transitions to establish
   whether the address remains valid.

## Client follow-up

At the time of comparison, `DotHackInterface.modify_word()` hardcodes
Infection's `0xA44C0C`. Once later-volume `AreaWords` addresses are verified,
this method must use the selected volume's address rather than that literal.

## Local sources

- [Address classes](../data/Addresses.py)
- [Client memory interface](../DotHackInterface.py)
- [Mutation code notes](../Code%20Notes%20-%20.hack__Mutation%20%C2%B7%20RetroAchievements.html)
- [Outbreak code notes](../Code%20Notes%20-%20.hack__Outbreak%20%C2%B7%20RetroAchievements.html)
- [Quarantine code notes](../Code%20Notes%20-%20.hack__Quarantine%20%C2%B7%20RetroAchievements.html)
