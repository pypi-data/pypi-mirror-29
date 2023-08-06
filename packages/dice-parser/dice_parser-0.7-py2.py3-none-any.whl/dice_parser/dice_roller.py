from random import randrange


class DiceRoller:
    def __init__(self, count, size, modifier=None):
        self._count = count
        self._size = size
        self._modifier = modifier

    def roll(self):
        rolled = [self._roll_die(self._size) for _ in range(self._count)]
        actual, ignored = self._modifier.get_actual_dice(rolled)

        return sum(actual), rolled

    @classmethod
    def _roll_die(cls, size):
        return 1 + randrange(0, size)


class DiceModifier:
    def __init__(self, count=0):
        self._count = count

    def _safe_count(self, dice):
        return min(max(0, self._count), len(dice))


class NullDiceModifier(DiceModifier):
    def get_actual_dice(self, dice):
        return dice, []


class HighestDiceModifier(DiceModifier):
    def get_actual_dice(self, dice):
        sorted_dice = sorted(dice)
        count = self._safe_count(dice)
        n = len(sorted_dice)

        return sorted_dice[n - count:], sorted_dice[:n - count]


class LowestDiceModifier(DiceModifier):
    def get_actual_dice(self, dice):
        sorted_dice = sorted(dice)
        count = self._safe_count(dice)

        return sorted_dice[:count], sorted_dice[count:]

