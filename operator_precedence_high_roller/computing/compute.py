from operator_precedence_high_roller.parsing.stacknode import StackNode
from operator_precedence_high_roller.parsing.enums.token_type import TokenType
from operator_precedence_high_roller.computing.computed_value import ComputedValue
import random

class Compute:
    def __init__(self):
        self.i = 0
        self.cocked_rolls = []
        self.all_lists_of_rolls = []
        self.list_of_dice = []
        self.error = False
        self.strict_twists = True
        self.cocked_odds = 0.025

    def find_max_rolls(self, list_of_rolls, num_cuts, num_keeps):
        b = list_of_rolls[:]
        final_list = []
        minimum = min(b) - 1
        for i in range(num_cuts):
            b.remove(max(b))
        for i in range(num_keeps):
            maxIndex = b.index(max(b))
            maxVal = max(b)
            final_list.append(maxVal)
            b[maxIndex] = minimum
        return final_list
    
    def find_min_rolls(self, list_of_rolls, num_keeps):
        b = list_of_rolls[:]
        final_list = []
        maximum = max(b) + 1
        for i in range(num_keeps):
            minIndex = b.index(min(b))
            minVal = min(b)
            final_list.append(minVal)
            b[minIndex] = maximum
        return final_list
    
    def find_max_duplicate(self, list_of_rolls):
        newlist = [] # empty list to hold unique elements from the list
        duplicates = [] # empty list to hold the duplicate elements from the list
        for i in list_of_rolls:
            if i not in newlist:
                newlist.append(i)
            elif i not in duplicates:
                duplicates.append(i)
        return max(duplicates, default=None)
    
    def check_for_twists(self, list_of_rolls, num_cuts):
        max_duplicate = self.find_max_duplicate(list_of_rolls)
        if self.strict_twists:
            max_roll = self.find_max_rolls(list_of_rolls, num_cuts, num_keeps=1)[0]
            if max_duplicate == max_roll:
                return True
        else:
            if max_duplicate != None:
                return True
        return False

    def roll_regular_die(self, to_roll: str):
        try:
            num_rolls = int(to_roll[:to_roll.index('d')]) if to_roll[:to_roll.index('d')] != '' else 1
            num_sides = int(to_roll[to_roll.index('d')+1:])
        except:
            return None
        if (
            num_rolls > 100 or 
            num_sides > 10000 or
            num_rolls < 1 or
            num_sides < 1
        ):
            self.error = True
            return None
        rolled_total = 0
        list_of_rolls = []
        for i in range(num_rolls):
            self.i += 1
            if random.random() < self.cocked_odds:
                self.cocked_rolls.append((random.randint(1, num_sides), self.i))
            roll = random.randint(1, num_sides)
            list_of_rolls.append(roll)
            rolled_total += roll
        self.all_lists_of_rolls.append(list_of_rolls)
        roll_avg = int((1+num_sides)/2*num_rolls)
        self.list_of_dice.append(('' if num_rolls == 1 else str(num_rolls)) + 'd' + str(num_sides))
        return ComputedValue(rolled_total, roll_avg, False)

    def roll_exploding_die(self, to_roll: str):
        try:
            num_rolls = int(to_roll[:to_roll.index('e')]) if to_roll[:to_roll.index('e')] != '' else 1
            num_sides = int(to_roll[to_roll.index('e')+1:])
        except:
            return None
        if (
            num_rolls > 1000 or 
            num_sides > 10000 or
            num_rolls < 1 or
            num_sides < 1
        ):
            self.error = True
            return None
        rolled_total = 0
        list_of_rolls = []
        for i in range(num_rolls):
            roll = 0
            while(True):
                self.i += 1
                if random.random() < self.cocked_odds:
                    self.cocked_rolls.append((random.randint(1, num_sides), self.i))
                roll = random.randint(1, num_sides)
                rolled_total += roll
                list_of_rolls.append(roll)
                if roll != num_sides or num_sides == 1:
                    break
        roll_avg = 0
        for i in range(num_sides):
            roll_avg += (i + 1)
        if num_sides > 1:
            roll_avg = int(roll_avg/(num_sides-1)*num_rolls)
        else:
            roll_avg = 1
        self.all_lists_of_rolls.append(list_of_rolls)
        self.list_of_dice.append(('' if num_rolls == 1 else str(num_rolls)) + 'e' + str(num_sides))
        return ComputedValue(rolled_total, roll_avg, False)

    def roll_kh_die(self, to_roll: str):
        try:
            num_rolls = int(to_roll[:to_roll.index('d')]) if to_roll[:to_roll.index('d')] != '' else 1
            num_cuts = 0
            num_keeps = 0
            if('c' in to_roll):
                num_sides = int(to_roll[to_roll.index('d')+1:to_roll.index('c')])
                num_cuts = int(to_roll[to_roll.index('c')+1:to_roll.index('kh')])
            else:
                num_sides = int(to_roll[to_roll.index('d')+1:to_roll.index('kh')])
            if 't' in to_roll:
                num_keeps = int(to_roll[to_roll.index('kh')+2:-1]) if to_roll[to_roll.index('kh')+2:-1] != '' else 1
            else:
                num_keeps = int(to_roll[to_roll.index('kh')+2:]) if to_roll[to_roll.index('kh')+2:] != '' else 1
            twists_enabled = ('t' in to_roll)
            roll_twisted = False
        except:
            return None
        if (
            num_rolls > 1000 or 
            num_sides > 10000 or 
            num_rolls == num_keeps or 
            num_rolls < 1 or
            num_sides < 1 or
            num_cuts < 0 or
            num_keeps < 1 or
            num_rolls < num_cuts + num_keeps
        ):
            self.error = True
            return None
        list_of_rolls = []
        for i in range(num_rolls):
            self.i += 1
            if random.random() < self.cocked_odds:
                self.cocked_rolls.append((random.randint(1, num_sides), self.i))
            roll = random.randint(1, num_sides)
            list_of_rolls.append(roll)
        if twists_enabled:
            roll_twisted = self.check_for_twists(list_of_rolls, num_cuts)
        self.all_lists_of_rolls.append(list_of_rolls)
        #there's probably a formula/process to accurately calculate the average for any of these, but idk what it is yet
        roll_avg = 0
        self.list_of_dice.append(('' if num_rolls == 1 else str(num_rolls)) + 'd' + str(num_sides))
        #return (sum(self.find_max_rolls(list_of_rolls, num_cuts, num_keeps)), roll_avg, roll_twisted)
        return ComputedValue(sum(self.find_max_rolls(list_of_rolls, num_cuts, num_keeps)), roll_avg, roll_twisted)

    def roll_kl_die(self, to_roll: str):
        try:
            num_rolls = int(to_roll[:to_roll.index('d')]) if to_roll[:to_roll.index('d')] != '' else 1
            num_sides = int(to_roll[to_roll.index('d')+1:to_roll.index('kl')])
            num_keeps = int(to_roll[to_roll.index('kl')+2:]) if to_roll[to_roll.index('kl')+2:] != '' else 1
        except:
            return None
        if (
            num_rolls > 1000 or 
            num_sides > 10000 or 
            num_rolls == num_keeps or 
            num_rolls < 1 or
            num_sides < 1 or
            num_keeps < 1 
        ):
            self.error = True
            return None
        list_of_rolls = []
        for i in range(num_rolls):
            self.i += 1
            if random.random() < self.cocked_odds:
                self.cocked_rolls.append((random.randint(1, num_sides), self.i))
            roll = random.randint(1, num_sides)
            list_of_rolls.append(roll)
        self.all_lists_of_rolls.append(list_of_rolls)
        roll_avg = 0
        self.list_of_dice.append(('' if num_rolls == 1 else str(num_rolls)) + 'd' + str(num_sides))
        return ComputedValue(sum(self.find_min_rolls(list_of_rolls, num_keeps)), roll_avg, False)
    
    def roll_die(self, to_roll: str):
        if 'kh' in to_roll:
            return self.roll_kh_die(to_roll)
        elif 'kl' in to_roll:
            return self.roll_kl_die(to_roll)
        elif 'd' in to_roll:
            return self.roll_regular_die(to_roll)
        elif 'e' in to_roll:
            return self.roll_exploding_die(to_roll)
        else:
            return None
    
    def compute_expr(self, reduced_expr: StackNode):
        try:
            res_left = self.compute_expr(reduced_expr.left)
            left_expr = ComputedValue(res_left.value, res_left.average, res_left.twisted)
            res_right = self.compute_expr(reduced_expr.right)
            right_expr = ComputedValue(res_right.value, res_right.average, res_right.twisted)
            if reduced_expr.oper == TokenType.PLUS:
                return ComputedValue(left_expr.value + right_expr.value, left_expr.average + right_expr.average, left_expr.twisted or right_expr.twisted)
            elif reduced_expr.oper == TokenType.MINUS:
                return ComputedValue(left_expr.value - right_expr.value, left_expr.average - right_expr.average, left_expr.twisted or right_expr.twisted)
            elif reduced_expr.oper == TokenType.MULT:
                return ComputedValue(left_expr.value * right_expr.value, left_expr.average * right_expr.average, left_expr.twisted or right_expr.twisted)
            elif reduced_expr.oper == TokenType.DIV:
                if right_expr.value == 0:
                    self.error = True
                    return ComputedValue(0, 0, False)
                return ComputedValue(int(left_expr.value / right_expr.value), int(left_expr.average / right_expr.average), (left_expr.twist or right_expr.twist))
        except:
            if reduced_expr.token_info.TokenType == TokenType.ERROR:
                self.error = True
                return ComputedValue(0, 0, False)
            elif 'd' in reduced_expr.token_info.lexeme:
                to_roll = reduced_expr.token_info.lexeme
                res = self.roll_die(to_roll)
                return ComputedValue(res.value, res.average, res.twisted)
            elif 'e' in reduced_expr.token_info.lexeme:
                to_roll = reduced_expr.token_info.lexeme
                res = self.roll_exploding_die(to_roll)
                return ComputedValue(res.value, res.average, False)
            else:
                num = int(reduced_expr.token_info.lexeme)
                return ComputedValue(num, num, False)