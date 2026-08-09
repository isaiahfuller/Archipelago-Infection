from collections import defaultdict
from enum import member

from rule_builder.rules import Has, HasAll, CanReachLocation, Rule, True_
from .data.Strings import EventNames as Ev, PlayStatNames, ServerNames, CharacterNames, ItemNames, TradesanityNames, ShopsanityNames
from .data.locations.WordList import InfectionDeltaWordList as DeltaWordList, InfectionThetaWordList as ThetaWordList, get_wordlist_name
from .data.items.RyuBooks import RyuBooks
from .data.locations.Sanity import InfectionShopsanity, InfectionTradesanity

def set_list_rules(location_rules, event_location, wordlist):
    location_rules[event_location] &= Has(get_wordlist_name(wordlist))

    if wordlist in ThetaWordList:
        location_rules[event_location] &= Has(ServerNames.Theta.value)
        location_rules[get_wordlist_name(wordlist)] &= Has(ServerNames.Theta.value)


def set_stats_rules(location_rules, stats):
    for i in range(len(stats)):
        book = RyuBooks.get_by_stat(stats[i].stat)
        if book:
            location_rules[stats[i].name] &= Has(ItemNames[book.name].value)

        if i < len(stats) - 1:
            if stats[i].name.split('-')[0] != stats[i+1].name.split('-')[0]:
                continue
            location_rules[stats[i+1].name] &= CanReachLocation(stats[i].name)


def infection_rules(world):
    location_rules: defaultdict[str, Rule] = defaultdict(True_)
    set_stats_rules(location_rules, world.playstat_locations)

    # Set completion condition
    goal_loc = Ev.SkeithDefeated.value
    if world.options.completion_condition == 1:
        goal_loc = Ev.ParasiteDragonDefeated.value

    location_rules["Victory"] &= CanReachLocation(goal_loc)

    world.set_completion_rule(Has("Victory"))

    if world.options.completion_condition == 1:
        location_rules[Ev.ParasiteDragonDefeated.value] &= CanReachLocation(Ev.SkeithDefeated.value)

    # Story missions
    set_list_rules(location_rules, Ev.FirstDataBug.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
    location_rules[Ev.FirstDataBug.value] &= CanReachLocation(PlayStatNames.KiteLevel.value + "1")

    set_list_rules(location_rules, Ev.LearnGateHacking.value, DeltaWordList.BoundlessCorruptedFortWalls)
    location_rules[get_wordlist_name(DeltaWordList.BoundlessCorruptedFortWalls)] &= CanReachLocation(Ev.FirstDataBug.value)
    location_rules[Ev.LearnGateHacking.value] &= CanReachLocation(Ev.FirstDataBug.value)
    location_rules[Ev.LearnGateHacking.value] &= CanReachLocation(PlayStatNames.KiteLevel.value + "7")

    set_list_rules(location_rules, Ev.SavedPiros.value, DeltaWordList.IndiscreetGluttonousPilgrimage)
    location_rules[get_wordlist_name(DeltaWordList.IndiscreetGluttonousPilgrimage)] &= CanReachLocation(Ev.LearnGateHacking.value)
    location_rules[Ev.SavedPiros.value] &= CanReachLocation(Ev.LearnGateHacking.value)

    set_list_rules(location_rules, Ev.BoardProtected.value, DeltaWordList.ClosedObliviousTwinHills)
    location_rules[get_wordlist_name(DeltaWordList.ClosedObliviousTwinHills)] &= CanReachLocation(Ev.SavedPiros.value)
    location_rules[Ev.BoardProtected.value] &= HasAll(CharacterNames.Elk.value, CharacterNames.Mia.value)
    location_rules[Ev.BoardProtected.value] &= CanReachLocation(Ev.SavedPiros.value)
    location_rules[Ev.BoardProtected.value] &= CanReachLocation(PlayStatNames.KiteLevel.value + "5")

    set_list_rules(location_rules, Ev.BlackRoseDungeon.value, ThetaWordList.QuietEternalWhiteDevil)
    location_rules[get_wordlist_name(ThetaWordList.QuietEternalWhiteDevil)] &= CanReachLocation(Ev.BoardProtected.value)
    location_rules[Ev.BlackRoseDungeon.value] &= HasAll(CharacterNames.BlackRose.value, ServerNames.Theta.value)
    location_rules[Ev.BlackRoseDungeon.value] &= CanReachLocation(Ev.BoardProtected.value)
    location_rules[Ev.BlackRoseDungeon.value] &= CanReachLocation(PlayStatNames.KiteLevel.value + "15")

    set_list_rules(location_rules, Ev.ElkMiaFavorite.value, DeltaWordList.PlenteousSmilingHypha)
    location_rules[get_wordlist_name(DeltaWordList.PlenteousSmilingHypha)] &= CanReachLocation(Ev.BlackRoseDungeon.value)
    location_rules[Ev.ElkMiaFavorite.value] &= HasAll(CharacterNames.Elk.value, CharacterNames.Mia.value)
    location_rules[Ev.ElkMiaFavorite.value] &= CanReachLocation(Ev.BlackRoseDungeon.value)

    set_list_rules(location_rules, Ev.PirosDiary.value, DeltaWordList.PutridHotbloodedScaffold)
    location_rules[get_wordlist_name(DeltaWordList.PutridHotbloodedScaffold)] &= CanReachLocation(Ev.ElkMiaFavorite.value)
    location_rules[Ev.PirosDiary.value] &= Has(CharacterNames.Piros.value)
    location_rules[Ev.PirosDiary.value] &= CanReachLocation(Ev.ElkMiaFavorite.value)

    set_list_rules(location_rules, Ev.MistralMeetUp.value, ThetaWordList.CollapsedMomentarySpiral)
    set_list_rules(location_rules, Ev.MistralMeetUp.value, DeltaWordList.BurstingPassedOverAquaField)
    location_rules[get_wordlist_name(ThetaWordList.CollapsedMomentarySpiral)] &= CanReachLocation(Ev.PirosDiary.value)
    location_rules[Ev.MistralMeetUp.value] &= HasAll(CharacterNames.Mistral.value, ServerNames.Theta.value)
    location_rules[Ev.MistralMeetUp.value] &= CanReachLocation(Ev.PirosDiary.value)

    set_list_rules(location_rules, Ev.Epitaph00.value, ThetaWordList.CursedDespairedParadise)
    location_rules[get_wordlist_name(ThetaWordList.CursedDespairedParadise)] &= CanReachLocation(Ev.MistralMeetUp.value)
    location_rules[Ev.Epitaph00.value] &= CanReachLocation(Ev.MistralMeetUp.value)

    set_list_rules(location_rules, Ev.DescendentsOfFianna.value, DeltaWordList.BuriedPaganFierySands)
    location_rules[get_wordlist_name(DeltaWordList.BuriedPaganFierySands)] &= CanReachLocation(Ev.Epitaph00.value)
    location_rules[Ev.DescendentsOfFianna.value] &= CanReachLocation(Ev.Epitaph00.value)

    set_list_rules(location_rules, Ev.EpitaphQ.value, DeltaWordList.LonelySilentGreatSeal)
    location_rules[get_wordlist_name(DeltaWordList.LonelySilentGreatSeal)] &= CanReachLocation(Ev.DescendentsOfFianna.value)
    location_rules[Ev.EpitaphQ.value] &= CanReachLocation(Ev.DescendentsOfFianna.value)

    set_list_rules(location_rules, Ev.MetMeg.value, ThetaWordList.GreatDistantFertileLand)
    location_rules[get_wordlist_name(ThetaWordList.GreatDistantFertileLand)] &= CanReachLocation(Ev.EpitaphQ.value)
    location_rules[Ev.MetMeg.value] &= CanReachLocation(Ev.EpitaphQ.value)

    set_list_rules(location_rules, Ev.SkeithDefeated.value, ThetaWordList.ChosenHopelessNothingness)
    location_rules[get_wordlist_name(ThetaWordList.ChosenHopelessNothingness)] &= CanReachLocation(Ev.MetMeg.value)
    location_rules[Ev.SkeithDefeated.value] &= CanReachLocation(Ev.MetMeg.value)
    location_rules[Ev.SkeithDefeated.value] &= CanReachLocation(PlayStatNames.KiteLevel.value + "20")

    # Optional Party Members
    if world.options.optional_party_members:
        set_list_rules(location_rules, Ev.Natsume.value, DeltaWordList.RagingPassionateMelody)
        location_rules[get_wordlist_name(DeltaWordList.RagingPassionateMelody)] &= CanReachLocation(Ev.BoardProtected.value)
        location_rules[Ev.Natsume.value] &= CanReachLocation(Ev.BoardProtected.value)

        set_list_rules(location_rules, Ev.Gardenia.value, ThetaWordList.SoftSolitaryTriPansy)
        location_rules[get_wordlist_name(ThetaWordList.SoftSolitaryTriPansy)] &= CanReachLocation(Ev.ElkMiaFavorite.value)
        location_rules[Ev.Gardenia.value] &= CanReachLocation(Ev.ElkMiaFavorite.value)

        set_list_rules(location_rules, Ev.Sanjuro.value, DeltaWordList.HideousDestroyersFarThunder)
        location_rules[get_wordlist_name(DeltaWordList.HideousDestroyersFarThunder)] &= CanReachLocation(Ev.ElkMiaFavorite.value)
        location_rules[Ev.Sanjuro.value] &= CanReachLocation(Ev.ElkMiaFavorite.value)

        # Gardenia's quest
        set_list_rules(location_rules, Ev.GracefulBook.value, ThetaWordList.BeautifulSomeonesTreasureGem)
        location_rules[get_wordlist_name(ThetaWordList.BeautifulSomeonesTreasureGem)] &= Has(CharacterNames.Gardenia.value)
        location_rules[get_wordlist_name(ThetaWordList.BeautifulSomeonesTreasureGem)] &= CanReachLocation(Ev.MistralMeetUp.value)
        location_rules[Ev.GracefulBook.value] &= Has(CharacterNames.Gardenia.value)
        location_rules[Ev.GracefulBook.value] &= CanReachLocation(Ev.MistralMeetUp.value)
        location_rules[Ev.GracefulBook.value] &= CanReachLocation(Ev.Gardenia.value)

    # Golden Goblin quest
    if world.options.golden_goblins:
        set_list_rules(location_rules, Ev.Stehony.value, DeltaWordList.DetestableGoldenSunnyDemon)

        set_list_rules(location_rules, Ev.Jonue.value, DeltaWordList.DetestableGoldenMessenger)
        location_rules[get_wordlist_name(DeltaWordList.DetestableGoldenMessenger)] &= CanReachLocation(Ev.Stehony.value)
        location_rules[Ev.Jonue.value] &= CanReachLocation(Ev.Stehony.value)
        location_rules[Ev.Jonue.value] &= CanReachLocation(Ev.BoardProtected.value)

        set_list_rules(location_rules, Ev.Zyan.value, DeltaWordList.DetestableGoldenScent)
        location_rules[get_wordlist_name(DeltaWordList.DetestableGoldenScent)] &= CanReachLocation(Ev.Jonue.value)
        location_rules[Ev.Zyan.value] &= CanReachLocation(Ev.Jonue.value)
        location_rules[Ev.Zyan.value] &= CanReachLocation(Ev.ElkMiaFavorite.value)

        set_list_rules(location_rules, Ev.Albert.value, DeltaWordList.DetestableGoldenNewTruth)
        location_rules[get_wordlist_name(DeltaWordList.DetestableGoldenNewTruth)] &= CanReachLocation(Ev.Zyan.value)
        location_rules[Ev.Albert.value] &= CanReachLocation(Ev.Zyan.value)
        location_rules[Ev.Albert.value] &= CanReachLocation(Ev.MistralMeetUp.value)

        set_list_rules(location_rules, Ev.Martina.value, DeltaWordList.DetestableGoldenGate)
        location_rules[get_wordlist_name(DeltaWordList.DetestableGoldenGate)] &= CanReachLocation(Ev.Albert.value)
        location_rules[Ev.Martina.value] &= CanReachLocation(Ev.Albert.value)
        location_rules[Ev.Martina.value] &= CanReachLocation(Ev.SkeithDefeated.value)

        # Shopsanity Server Requirement Logic - Something here doesn't work, and I'm not sure what.
    if world.options.shopsanity:
        set_list_rules(location_rules, ShopsanityNames.DLWS1.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Mia1.value] &= Has(ServerNames.Theta.value)
        set_list_rules(location_rules, ShopsanityNames.DLIS1.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Mia1.value] &= Has(ServerNames.Theta.value)
        set_list_rules(location_rules, ShopsanityNames.DLMS1.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Mia1.value] &= Has(ServerNames.Theta.value)
        set_list_rules(location_rules, ShopsanityNames.DLWS2.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Mia1.value] &= Has(ServerNames.Theta.value)
        set_list_rules(location_rules, ShopsanityNames.DLIS2.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Mia1.value] &= Has(ServerNames.Theta.value)
        set_list_rules(location_rules, ShopsanityNames.DLMS2.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Mia1.value] &= Has(ServerNames.Theta.value)
        set_list_rules(location_rules, ShopsanityNames.DLWS3.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Mia1.value] &= Has(ServerNames.Theta.value)
        set_list_rules(location_rules, ShopsanityNames.DLIS3.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Mia1.value] &= Has(ServerNames.Theta.value)
        set_list_rules(location_rules, ShopsanityNames.DLMS3.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Mia1.value] &= Has(ServerNames.Theta.value)
        set_list_rules(location_rules, ShopsanityNames.DLWS4.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Mia1.value] &= Has(ServerNames.Theta.value)
        set_list_rules(location_rules, ShopsanityNames.DLIS4.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Mia1.value] &= Has(ServerNames.Theta.value)
        set_list_rules(location_rules, ShopsanityNames.DLMS4.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Mia1.value] &= Has(ServerNames.Theta.value)
        set_list_rules(location_rules, ShopsanityNames.DLWS5.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Mia1.value] &= Has(ServerNames.Theta.value)
        set_list_rules(location_rules, ShopsanityNames.DLIS5.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Mia1.value] &= Has(ServerNames.Theta.value)
        set_list_rules(location_rules, ShopsanityNames.DLMS5.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Mia1.value] &= Has(ServerNames.Theta.value)

        #Tradesanity Party Member Requirement Logic
    if world.options.tradesanity:
        # Mia
        set_list_rules(location_rules, TradesanityNames.Mia1.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Mia1.value] &= Has(CharacterNames.Mia.value)
        set_list_rules(location_rules, TradesanityNames.Mia2.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Mia2.value] &= Has(CharacterNames.Mia.value)
        set_list_rules(location_rules, TradesanityNames.Mia3.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Mia3.value] &= Has(CharacterNames.Mia.value)

        # Orca
        set_list_rules(location_rules, TradesanityNames.Orca1.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Orca1.value] &= Has(CharacterNames.Orca.value)
        set_list_rules(location_rules, TradesanityNames.Orca2.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Orca2.value] &= Has(CharacterNames.Orca.value)
        set_list_rules(location_rules, TradesanityNames.Orca3.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Orca3.value] &= Has(CharacterNames.Orca.value)

        # Marlo
        set_list_rules(location_rules, TradesanityNames.Marlo1.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Marlo1.value] &= Has(CharacterNames.Marlo.value)
        set_list_rules(location_rules, TradesanityNames.Marlo2.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Marlo2.value] &= Has(CharacterNames.Marlo.value)
        set_list_rules(location_rules, TradesanityNames.Marlo3.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Marlo3.value] &= Has(CharacterNames.Marlo.value)

        # Sanjuro
        set_list_rules(location_rules, TradesanityNames.Sanjuro1.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Sanjuro1.value] &= Has(CharacterNames.Sanjuro.value)
        set_list_rules(location_rules, TradesanityNames.Sanjuro2.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Sanjuro2.value] &= Has(CharacterNames.Sanjuro.value)
        set_list_rules(location_rules, TradesanityNames.Sanjuro3.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Sanjuro3.value] &= Has(CharacterNames.Sanjuro.value)

        # NukeUsagimaru
        set_list_rules(location_rules, TradesanityNames.NukeUsagimaru1.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.NukeUsagimaru1.value] &= Has(CharacterNames.NukeUsagimaru.value)
        set_list_rules(location_rules, TradesanityNames.NukeUsagimaru2.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.NukeUsagimaru2.value] &= Has(CharacterNames.NukeUsagimaru.value)
        set_list_rules(location_rules, TradesanityNames.NukeUsagimaru3.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.NukeUsagimaru3.value] &= Has(CharacterNames.NukeUsagimaru.value)

        # Balmung
        set_list_rules(location_rules, TradesanityNames.Balmung1.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Balmung1.value] &= Has(CharacterNames.Balmung.value)
        set_list_rules(location_rules, TradesanityNames.Balmung2.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Balmung2.value] &= Has(CharacterNames.Balmung.value)
        set_list_rules(location_rules, TradesanityNames.Balmung3.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Balmung3.value] &= Has(CharacterNames.Balmung.value)

        # Moonstone
        set_list_rules(location_rules, TradesanityNames.Moonstone1.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Moonstone1.value] &= Has(CharacterNames.Moonstone.value)
        set_list_rules(location_rules, TradesanityNames.Moonstone2.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Moonstone2.value] &= Has(CharacterNames.Moonstone.value)
        set_list_rules(location_rules, TradesanityNames.Moonstone3.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Moonstone3.value] &= Has(CharacterNames.Moonstone.value)

        # Piros
        set_list_rules(location_rules, TradesanityNames.Piros1.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Piros1.value] &= Has(CharacterNames.Piros.value)
        set_list_rules(location_rules, TradesanityNames.Piros2.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Piros2.value] &= Has(CharacterNames.Piros.value)
        set_list_rules(location_rules, TradesanityNames.Piros3.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Piros3.value] &= Has(CharacterNames.Piros.value)

        # Wiseman
        set_list_rules(location_rules, TradesanityNames.Wiseman1.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Wiseman1.value] &= Has(CharacterNames.Wiseman.value)
        set_list_rules(location_rules, TradesanityNames.Wiseman2.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Wiseman2.value] &= Has(CharacterNames.Wiseman.value)
        set_list_rules(location_rules, TradesanityNames.Wiseman3.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Wiseman3.value] &= Has(CharacterNames.Wiseman.value)

        # Elk
        set_list_rules(location_rules, TradesanityNames.Elk1.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Elk1.value] &= Has(CharacterNames.Elk.value)
        set_list_rules(location_rules, TradesanityNames.Elk2.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Elk2.value] &= Has(CharacterNames.Elk.value)
        set_list_rules(location_rules, TradesanityNames.Elk3.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Elk3.value] &= Has(CharacterNames.Elk.value)

        # Natsume
        set_list_rules(location_rules, TradesanityNames.Natsume1.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Natsume1.value] &= Has(CharacterNames.Natsume.value)
        set_list_rules(location_rules, TradesanityNames.Natsume2.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Natsume2.value] &= Has(CharacterNames.Natsume.value)
        set_list_rules(location_rules, TradesanityNames.Natsume3.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Natsume3.value] &= Has(CharacterNames.Natsume.value)

        # Rachel
        set_list_rules(location_rules, TradesanityNames.Rachel1.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Rachel1.value] &= Has(CharacterNames.Rachel.value)
        set_list_rules(location_rules, TradesanityNames.Rachel2.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Rachel2.value] &= Has(CharacterNames.Rachel.value)
        set_list_rules(location_rules, TradesanityNames.Rachel3.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Rachel3.value] &= Has(CharacterNames.Rachel.value)

        # Gardenia
        set_list_rules(location_rules, TradesanityNames.Gardenia1.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Gardenia1.value] &= Has(CharacterNames.Gardenia.value)
        set_list_rules(location_rules, TradesanityNames.Gardenia2.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Gardenia2.value] &= Has(CharacterNames.Gardenia.value)
        set_list_rules(location_rules, TradesanityNames.Gardenia3.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Gardenia3.value] &= Has(CharacterNames.Gardenia.value)

        # TerajimaRyoko
        set_list_rules(location_rules, TradesanityNames.TerajimaRyoko1.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.TerajimaRyoko1.value] &= Has(CharacterNames.TerajimaRyoko.value)
        set_list_rules(location_rules, TradesanityNames.TerajimaRyoko2.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.TerajimaRyoko2.value] &= Has(CharacterNames.TerajimaRyoko.value)
        set_list_rules(location_rules, TradesanityNames.TerajimaRyoko3.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.TerajimaRyoko3.value] &= Has(CharacterNames.TerajimaRyoko.value)

        # BlackRose
        set_list_rules(location_rules, TradesanityNames.BlackRose1.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.BlackRose1.value] &= Has(CharacterNames.BlackRose.value)
        set_list_rules(location_rules, TradesanityNames.BlackRose2.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.BlackRose2.value] &= Has(CharacterNames.BlackRose.value)
        set_list_rules(location_rules, TradesanityNames.BlackRose3.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.BlackRose3.value] &= Has(CharacterNames.BlackRose.value)

        # Mistral
        set_list_rules(location_rules, TradesanityNames.Mistral1.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Mistral1.value] &= Has(CharacterNames.Mistral.value)
        set_list_rules(location_rules, TradesanityNames.Mistral2.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Mistral2.value] &= Has(CharacterNames.Mistral.value)
        set_list_rules(location_rules, TradesanityNames.Mistral3.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Mistral3.value] &= Has(CharacterNames.Mistral.value)

        # Helba
        set_list_rules(location_rules, TradesanityNames.Helba1.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Helba1.value] &= Has(CharacterNames.Helba.value)
        set_list_rules(location_rules, TradesanityNames.Helba2.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Helba2.value] &= Has(CharacterNames.Helba.value)
        set_list_rules(location_rules, TradesanityNames.Helba3.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Helba3.value] &= Has(CharacterNames.Helba.value)

        #Grunties
        set_list_rules(location_rules, TradesanityNames.NobleGrunty.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Mia1.value] &= Has(ServerNames.Theta.value)
        set_list_rules(location_rules, TradesanityNames.IronGrunty.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Mia1.value] &= Has(ServerNames.Theta.value)
        set_list_rules(location_rules, TradesanityNames.PoisonGrunty.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
        location_rules[TradesanityNames.Mia1.value] &= Has(ServerNames.Theta.value)


    for name, rule in location_rules.items():
        try:
            location = world.get_location(name)
        except KeyError:
            continue
        world.set_rule(location, rule)
