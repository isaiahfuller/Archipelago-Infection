from worlds.generic.Rules import add_rule
from .data.Strings import EventNames as Ev, PlayStatNames, ServerNames, CharacterNames, ItemNames
from .data.locations.WordList import InfectionDeltaWordList as DeltaWordList, InfectionThetaWordList as ThetaWordList, get_wordlist_name
from .data.items.RyuBooks import RyuBooks
from .data.locations.Events import MonsterHunt1, MonsterHunt2

def set_list_rules(world, event_location, wordlist):
    add_rule(world.multiworld.get_location(event_location, world.player),
             lambda state: state.has(get_wordlist_name(wordlist), world.player))

    if wordlist in ThetaWordList:
        add_rule(world.multiworld.get_location(event_location, world.player),
                 lambda state: state.has(ServerNames.Theta.value, world.player))
        add_rule(world.multiworld.get_location(get_wordlist_name(wordlist), world.player),
                 lambda state: state.has(ServerNames.Theta.value, world.player))


    if lambda state: state.has(ServerNames.Theta.value, world.player):
        add_rule(world.multiworld.get_location(MonsterHunt2), world.player)

def set_stats_rules(world, stats):
    for i in range(len(stats)):
        book = RyuBooks.get_by_stat(stats[i].stat)
        if book:
            add_rule(world.multiworld.get_location(stats[i].name, world.player),
                     lambda state, book_item=ItemNames[book.name].value: state.has(book_item, world.player))

        if i < len(stats) - 1:
            if stats[i].name.split('-')[0] != stats[i+1].name.split('-')[0]:
                continue
            add_rule(world.multiworld.get_location(stats[i+1].name, world.player),
                     lambda state, i=i: state.can_reach_location(stats[i].name, world.player))


def infection_rules(world):
    set_stats_rules(world, world.playstat_locations)

    # Set completion condition
    goal_loc = Ev.SkeithDefeated.value
    if world.options.completion_condition == 1:
        goal_loc = Ev.ParasiteDragonDefeated.value

    add_rule(world.multiworld.get_location("Victory", world.player),
             lambda state: state.can_reach_location(goal_loc, world.player))

    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)

    if world.options.completion_condition == 1:
        add_rule(world.multiworld.get_location(Ev.ParasiteDragonDefeated.value, world.player),
                 lambda state: state.can_reach_location(Ev.SkeithDefeated.value, world.player))

    # Story missions
    set_list_rules(world, Ev.FirstDataBug.value, DeltaWordList.ExpansiveHauntedSeaOfSand)
    add_rule(world.multiworld.get_location(Ev.FirstDataBug.value, world.player),
             lambda state: state.can_reach_location(PlayStatNames.KiteLevel.value + "1", world.player))

    set_list_rules(world, Ev.LearnGateHacking.value, DeltaWordList.BoundlessCorruptedFortWalls)
    add_rule(world.multiworld.get_location(get_wordlist_name(DeltaWordList.BoundlessCorruptedFortWalls), world.player),
             lambda state: state.can_reach_location(Ev.FirstDataBug.value, world.player))
    add_rule(world.multiworld.get_location(Ev.LearnGateHacking.value, world.player),
             lambda state: state.can_reach_location(Ev.FirstDataBug.value, world.player))
    add_rule(world.multiworld.get_location(Ev.LearnGateHacking.value, world.player),
             lambda state: state.can_reach_location(PlayStatNames.KiteLevel.value + "7", world.player))

    set_list_rules(world, Ev.SavedPiros.value, DeltaWordList.IndiscreetGluttonousPilgrimage)
    add_rule(world.multiworld.get_location(get_wordlist_name(DeltaWordList.IndiscreetGluttonousPilgrimage), world.player),
             lambda state: state.can_reach_location(Ev.LearnGateHacking.value, world.player))
    add_rule(world.multiworld.get_location(Ev.SavedPiros.value, world.player),
             lambda state: state.can_reach_location(Ev.LearnGateHacking.value, world.player))

    set_list_rules(world, Ev.BoardProtected.value, DeltaWordList.ClosedObliviousTwinHills)
    add_rule(world.multiworld.get_location(get_wordlist_name(DeltaWordList.ClosedObliviousTwinHills), world.player),
             lambda state: state.can_reach_location(Ev.SavedPiros.value, world.player))
    add_rule(world.multiworld.get_location(Ev.BoardProtected.value, world.player), lambda state: state.has(
        CharacterNames.Mia.value, world.player) and state.has(CharacterNames.Elk.value, world.player))
    add_rule(world.multiworld.get_location(Ev.BoardProtected.value, world.player),
             lambda state: state.can_reach_location(Ev.SavedPiros.value, world.player))
    add_rule(world.multiworld.get_location(Ev.BoardProtected.value, world.player),
             lambda state: state.can_reach_location(PlayStatNames.KiteLevel.value + "5", world.player))

    set_list_rules(world, Ev.BlackRoseDungeon.value, ThetaWordList.QuietEternalWhiteDevil)
    add_rule(world.multiworld.get_location(get_wordlist_name(ThetaWordList.QuietEternalWhiteDevil), world.player),
             lambda state: state.can_reach_location(Ev.BoardProtected.value, world.player))
    add_rule(world.multiworld.get_location(Ev.BlackRoseDungeon.value, world.player),
             lambda state: state.has(CharacterNames.BlackRose.value, world.player))
    add_rule(world.multiworld.get_location(Ev.BlackRoseDungeon.value, world.player),
             lambda state: state.can_reach_location(Ev.BoardProtected.value, world.player))
    add_rule(world.multiworld.get_location(Ev.BlackRoseDungeon.value, world.player),
             lambda state: state.has(ServerNames.Theta.value, world.player))
    add_rule(world.multiworld.get_location(Ev.BlackRoseDungeon.value, world.player),
             lambda state: state.can_reach_location(PlayStatNames.KiteLevel.value + "15", world.player))

    set_list_rules(world, Ev.ElkMiaFavorite.value, DeltaWordList.PlenteousSmilingHypha)
    add_rule(world.multiworld.get_location(get_wordlist_name(DeltaWordList.PlenteousSmilingHypha), world.player),
             lambda state: state.can_reach_location(Ev.BlackRoseDungeon.value, world.player))
    add_rule(world.multiworld.get_location(Ev.ElkMiaFavorite.value, world.player), lambda state: state.has(
        CharacterNames.Elk.value, world.player) and state.has(CharacterNames.Mia.value, world.player))
    add_rule(world.multiworld.get_location(Ev.ElkMiaFavorite.value, world.player),
             lambda state: state.can_reach_location(Ev.BlackRoseDungeon.value, world.player))

    set_list_rules(world, Ev.PirosDiary.value, DeltaWordList.PutridHotbloodedScaffold)
    add_rule(world.multiworld.get_location(get_wordlist_name(DeltaWordList.PutridHotbloodedScaffold), world.player),
             lambda state: state.can_reach_location(Ev.ElkMiaFavorite.value, world.player))
    add_rule(world.multiworld.get_location(Ev.PirosDiary.value, world.player),
             lambda state: state.has(CharacterNames.Piros.value, world.player))
    add_rule(world.multiworld.get_location(Ev.PirosDiary.value, world.player),
             lambda state: state.can_reach_location(Ev.ElkMiaFavorite.value, world.player))

    set_list_rules(world, Ev.MistralMeetUp.value, ThetaWordList.CollapsedMomentarySpiral)
    set_list_rules(world, Ev.MistralMeetUp.value, DeltaWordList.BurstingPassedOverAquaField)
    add_rule(world.multiworld.get_location(get_wordlist_name(ThetaWordList.CollapsedMomentarySpiral), world.player),
             lambda state: state.can_reach_location(Ev.PirosDiary.value, world.player))
    add_rule(world.multiworld.get_location(Ev.MistralMeetUp.value, world.player),
             lambda state: state.has(CharacterNames.Mistral.value, world.player))
    add_rule(world.multiworld.get_location(Ev.MistralMeetUp.value, world.player),
             lambda state: state.can_reach_location(Ev.PirosDiary.value, world.player))
    add_rule(world.multiworld.get_location(Ev.MistralMeetUp.value, world.player),
             lambda state: state.has(ServerNames.Theta.value, world.player))

    set_list_rules(world, Ev.Epitaph00.value, ThetaWordList.CursedDespairedParadise)
    add_rule(world.multiworld.get_location(get_wordlist_name(ThetaWordList.CursedDespairedParadise), world.player),
             lambda state: state.can_reach_location(Ev.MistralMeetUp.value, world.player))
    add_rule(world.multiworld.get_location(Ev.Epitaph00.value, world.player),
             lambda state: state.can_reach_location(Ev.MistralMeetUp.value, world.player))

    set_list_rules(world, Ev.DescendentsOfFianna.value, DeltaWordList.BuriedPaganFierySands)
    add_rule(world.multiworld.get_location(get_wordlist_name(DeltaWordList.BuriedPaganFierySands), world.player),
             lambda state: state.can_reach_location(Ev.Epitaph00.value, world.player))
    add_rule(world.multiworld.get_location(Ev.DescendentsOfFianna.value, world.player),
             lambda state: state.can_reach_location(Ev.Epitaph00.value, world.player))

    set_list_rules(world, Ev.EpitaphQ.value, DeltaWordList.LonelySilentGreatSeal)
    add_rule(world.multiworld.get_location(get_wordlist_name(DeltaWordList.LonelySilentGreatSeal), world.player),
             lambda state: state.can_reach_location(Ev.DescendentsOfFianna.value, world.player))
    add_rule(world.multiworld.get_location(Ev.EpitaphQ.value, world.player),
             lambda state: state.can_reach_location(Ev.DescendentsOfFianna.value, world.player))

    set_list_rules(world, Ev.MetMeg.value, ThetaWordList.GreatDistantFertileLand)
    add_rule(world.multiworld.get_location(get_wordlist_name(ThetaWordList.GreatDistantFertileLand), world.player),
             lambda state: state.can_reach_location(Ev.EpitaphQ.value, world.player))
    add_rule(world.multiworld.get_location(Ev.MetMeg.value, world.player),
             lambda state: state.can_reach_location(Ev.EpitaphQ.value, world.player))

    set_list_rules(world, Ev.SkeithDefeated.value, ThetaWordList.ChosenHopelessNothingness)
    add_rule(world.multiworld.get_location(get_wordlist_name(ThetaWordList.ChosenHopelessNothingness), world.player),
             lambda state: state.can_reach_location(Ev.MetMeg.value, world.player))
    add_rule(world.multiworld.get_location(Ev.SkeithDefeated.value, world.player),
             lambda state: state.can_reach_location(Ev.MetMeg.value, world.player))
    add_rule(world.multiworld.get_location(Ev.SkeithDefeated.value, world.player),
             lambda state: state.can_reach_location(PlayStatNames.KiteLevel.value + "20", world.player))

    # Optional Party Members
    set_list_rules(world, Ev.Natsume.value, DeltaWordList.RagingPassionateMelody)
    add_rule(world.multiworld.get_location(get_wordlist_name(DeltaWordList.RagingPassionateMelody), world.player),
             lambda state: state.can_reach_location(Ev.BoardProtected.value, world.player))
    add_rule(world.multiworld.get_location(Ev.Natsume.value, world.player),
             lambda state: state.can_reach_location(Ev.BoardProtected.value, world.player))

    set_list_rules(world, Ev.Gardenia.value, ThetaWordList.SoftSolitaryTriPansy)
    add_rule(world.multiworld.get_location(get_wordlist_name(ThetaWordList.SoftSolitaryTriPansy), world.player),
             lambda state: state.can_reach_location(Ev.ElkMiaFavorite.value, world.player))
    add_rule(world.multiworld.get_location(Ev.Gardenia.value, world.player),
             lambda state: state.can_reach_location(Ev.ElkMiaFavorite.value, world.player))

    set_list_rules(world, Ev.Sanjuro.value, DeltaWordList.HideousDestroyersFarThunder)
    add_rule(world.multiworld.get_location(get_wordlist_name(DeltaWordList.HideousDestroyersFarThunder), world.player),
             lambda state: state.can_reach_location(Ev.ElkMiaFavorite.value, world.player))
    add_rule(world.multiworld.get_location(Ev.Sanjuro.value, world.player),
             lambda state: state.can_reach_location(Ev.ElkMiaFavorite.value, world.player))

    # Gardenia's quest
    set_list_rules(world, Ev.GracefulBook.value, ThetaWordList.BeautifulSomeonesTreasureGem)
    add_rule(world.multiworld.get_location(get_wordlist_name(ThetaWordList.BeautifulSomeonesTreasureGem), world.player),
             lambda state: state.has(CharacterNames.Gardenia.value, world.player))
    add_rule(world.multiworld.get_location(get_wordlist_name(ThetaWordList.BeautifulSomeonesTreasureGem), world.player),
             lambda state: state.can_reach_location(Ev.MistralMeetUp.value, world.player))
    add_rule(world.multiworld.get_location(Ev.GracefulBook.value, world.player),
             lambda state: state.has(CharacterNames.Gardenia.value, world.player))
    add_rule(world.multiworld.get_location(Ev.GracefulBook.value, world.player),
             lambda state: state.can_reach_location(Ev.MistralMeetUp.value, world.player))
    add_rule(world.multiworld.get_location(Ev.GracefulBook.value, world.player),
             lambda state: state.can_reach_location(Ev.Gardenia.value, world.player))

    # Golden Goblin quest
    set_list_rules(world, Ev.Stehony.value, DeltaWordList.DetestableGoldenSunnyDemon)

    set_list_rules(world, Ev.Jonue.value, DeltaWordList.DetestableGoldenMessenger)
    add_rule(world.multiworld.get_location(get_wordlist_name(DeltaWordList.DetestableGoldenMessenger), world.player),
             lambda state: state.can_reach_location(Ev.Stehony.value, world.player))
    add_rule(world.multiworld.get_location(Ev.Jonue.value, world.player),
             lambda state: state.can_reach_location(Ev.Stehony.value, world.player))
    add_rule(world.multiworld.get_location(Ev.Jonue.value, world.player),
             lambda state: state.can_reach_location(Ev.BoardProtected.value, world.player))

    set_list_rules(world, Ev.Zyan.value, DeltaWordList.DetestableGoldenScent)
    add_rule(world.multiworld.get_location(get_wordlist_name(DeltaWordList.DetestableGoldenScent), world.player),
             lambda state: state.can_reach_location(Ev.Jonue.value, world.player))
    add_rule(world.multiworld.get_location(Ev.Zyan.value, world.player),
             lambda state: state.can_reach_location(Ev.Jonue.value, world.player))
    add_rule(world.multiworld.get_location(Ev.Zyan.value, world.player),
             lambda state: state.can_reach_location(Ev.ElkMiaFavorite.value, world.player))

    set_list_rules(world, Ev.Albert.value, DeltaWordList.DetestableGoldenNewTruth)
    add_rule(world.multiworld.get_location(get_wordlist_name(DeltaWordList.DetestableGoldenNewTruth), world.player),
             lambda state: state.can_reach_location(Ev.Zyan.value, world.player))
    add_rule(world.multiworld.get_location(Ev.Albert.value, world.player),
             lambda state: state.can_reach_location(Ev.Zyan.value, world.player))
    add_rule(world.multiworld.get_location(Ev.Albert.value, world.player),
             lambda state: state.can_reach_location(Ev.MistralMeetUp.value, world.player))

    set_list_rules(world, Ev.Martina.value, DeltaWordList.DetestableGoldenGate)
    add_rule(world.multiworld.get_location(get_wordlist_name(DeltaWordList.DetestableGoldenGate), world.player),
             lambda state: state.can_reach_location(Ev.Albert.value, world.player))
    add_rule(world.multiworld.get_location(Ev.Martina.value, world.player),
             lambda state: state.can_reach_location(Ev.Albert.value, world.player))
    add_rule(world.multiworld.get_location(Ev.Martina.value, world.player),
             lambda state: state.can_reach_location(Ev.SkeithDefeated.value, world.player))
