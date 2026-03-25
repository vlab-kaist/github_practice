import random


class NumberGuessingGame:
    def __init__(self, min_val=1, max_val=100):
        self.min_val = min_val
        self.max_val = max_val
        self.secret = random.randint(min_val, max_val)
        self.attempts = 0
        self.max_attempts = 7
        self.guesses = []

    def guess(self, number):
        self.attempts += 1
        self.guesses.append(number)

        if number == self.secret:
            return "correct"
        elif number < self.secret:
            return "higher"
        else:
            return "lower"

    def is_game_over(self):
        return self.attempts >= self.max_attempts or self.secret in self.guesses

    def get_hint(self):
        diff = abs(self.secret - (self.guesses[-1] if self.guesses else 50))
        if diff <= 5:
            return "뜨거워! 아주 가까워요!"
        elif diff <= 15:
            return "따뜻해요~ 거의 다 왔어요"
        elif diff <= 30:
            return "미지근해요..."
        else:
            return "차가워요 ㅠㅠ 멀어요"


class RockPaperScissors:
    CHOICES = ["가위", "바위", "보"]

    def __init__(self):
        self.wins = 0
        self.losses = 0
        self.draws = 0

    def play(self, player_choice):
        computer_choice = random.choice(self.CHOICES)
        result = self._determine_winner(player_choice, computer_choice)

        if result == "win":
            self.wins += 1
        elif result == "lose":
            self.losses += 1
        else:
            self.draws += 1

        return {
            "player": player_choice,
            "computer": computer_choice,
            "result": result,
        }

    def _determine_winner(self, player, computer):
        if player == computer:
            return "draw"
        winning = {"가위": "보", "바위": "가위", "보": "바위"}
        return "win" if winning[player] == computer else "lose"

    def get_record(self):
        total = self.wins + self.losses + self.draws
        return {
            "total": total,
            "wins": self.wins,
            "losses": self.losses,
            "draws": self.draws,
            "win_rate": f"{(self.wins / total * 100):.1f}%" if total > 0 else "0%",
        }


class DiceGame:
    def __init__(self, num_dice=2):
        self.num_dice = num_dice
        self.rolls = []

    def roll(self):
        result = [random.randint(1, 6) for _ in range(self.num_dice)]
        self.rolls.append(result)
        return result

    def get_total(self, roll=None):
        if roll is None:
            roll = self.rolls[-1] if self.rolls else []
        return sum(roll)

    def get_stats(self):
        if not self.rolls:
            return {}
        totals = [sum(r) for r in self.rolls]
        return {
            "rolls": len(self.rolls),
            "average": sum(totals) / len(totals),
            "max": max(totals),
            "min": min(totals),
        }


if __name__ == "__main__":
    print("=== 주사위 게임 ===")
    dice = DiceGame()
    for i in range(10):
        result = dice.roll()
        print(f"  {i+1}번째: {result} = {dice.get_total(result)}")
    print(f"  통계: {dice.get_stats()}")

    print("\n=== 가위바위보 ===")
    rps = RockPaperScissors()
    for _ in range(5):
        choice = random.choice(RockPaperScissors.CHOICES)
        result = rps.play(choice)
        print(f"  {result['player']} vs {result['computer']} -> {result['result']}")
    print(f"  전적: {rps.get_record()}")
