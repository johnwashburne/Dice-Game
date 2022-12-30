from prediction_engine import DistributionLoader, Predictor
import random

if __name__ == "__main__":
    p = Predictor(DistributionLoader.load("default"))
    dice = [random.randint(1, 6) for _ in range(5)]
    print(dice)
    input()
    print(p.optimize_turn(0, 100, 3, dice))
