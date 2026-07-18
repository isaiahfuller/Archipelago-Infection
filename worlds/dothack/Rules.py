from rule_builder.rules import HasAny
from rule_builder.rules import CanReachRegion
from collections import defaultdict
from rule_builder.rules import Has, HasAll, CanReachLocation, Rule, True_
from .data.Strings import EventNames as Ev, PlayStatNames, ServerNames, CharacterNames, ItemNames
from .data.locations.WordList import InfectionDeltaWordList as DeltaWordList, InfectionThetaWordList as ThetaWordList, get_wordlist_name
from .data.items.RyuBooks import RyuBooks


def set_list_rules(location_rules, event_location, wordlist):
    location_rules[event_location] &= Has(get_wordlist_name(wordlist))

    if wordlist in DeltaWordList:
        location_rules[event_location] &= CanReachRegion(ServerNames.Delta.value)
        location_rules[get_wordlist_name(wordlist)] &= CanReachRegion(ServerNames.Delta.value)

    if wordlist in ThetaWordList:
        location_rules[event_location] &= CanReachRegion(ServerNames.Theta.value)
        location_rules[get_wordlist_name(wordlist)] &= CanReachRegion(ServerNames.Theta.value)


def set_stats_rules(location_rules, stats):
    for i in range(len(stats)):
        location_rules[stats[i].name] &= HasAny(ServerNames.Delta.value,ServerNames.Theta.value)
        book = RyuBooks.get_by_stat(stats[i].stat)
        if book:
            location_rules[stats[i].name] &= CanReachRegion(ItemNames[book.name].value)

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
    location_rules[Ev.BlackRoseDungeon.value] &= CanReachRegion(ServerNames.Theta.value)
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
    location_rules[Ev.MistralMeetUp.value] &= Has(CharacterNames.Mistral.value)
    location_rules[Ev.MistralMeetUp.value] &= CanReachRegion(ServerNames.Theta.value)
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

    for name, rule in location_rules.items():
        try:
            location = world.get_location(name)
        except KeyError:
            continue
        world.set_rule(location, rule)
