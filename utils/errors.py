from discord.ext.commands import CheckFailure

class SpaceCheckFailure(CheckFailure):
    pass

class UserNotVerified(SpaceCheckFailure):
    def __init__(self, member) -> None:
        self.member = member