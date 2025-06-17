from operator_precedence_high_roller.json_handling.json_handle import JsonHandle
from operator_precedence_high_roller.computing.compute import Compute
import discord

class Gamble:
    def __init__(self, message: discord.Message):
        self.message = message
        self.c = Compute()
        self.json_handler = JsonHandle(playername=message.author.name)
        self.even = False
        self.point_requirement = 5
        self.winnings = 10

    def enough_figglebucks(self):
        return int(self.json_handler.check_figglebucks(self.point_requirement)) >= self.point_requirement
    
    def subtract_figglebucks(self):
        return self.json_handler.update_figglebucks(-self.point_requirement)

    def update_gambling_state(self, gambling_state: bool):
        self.json_handler.update_json_gambling(gambling_state)

    def gambling(self):
        return self.json_handler.gambling()

    async def determine_bet(self, bet: str):
        if bet == 'evens':
            self.even = True
            return True
        elif bet == 'odds':
            self.even = False
            return True
        return False

    async def determine_result(self):
        res = self.c.roll_die('d20')
        roll_even = int(res[0]) % 2 == 0
        if (roll_even and self.even) or (not roll_even and not self.even):
            await self.message.channel.send(str(res[0]) + ' :money_mouth:')
            self.json_handler.update_figglebucks(self.winnings)
        else:
            await self.message.channel.send(str(res[0]) + ' :japanese_ogre:')
