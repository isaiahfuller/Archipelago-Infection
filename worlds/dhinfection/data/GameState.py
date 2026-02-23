from enum import IntFlag, auto


class InfectionGameState(IntFlag):
    _value_: int
    TitleScreen = 0x01
    Desktop = 0x02
    Login = 0x03
    LoggingIn = 0x04
    LoggedIn = 0x05
