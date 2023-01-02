from prediction_engine import DistributionLoader, Predictor

if __name__ == "__main__":
    p = Predictor(DistributionLoader.load("default"))
    print(p.optimize_turn(
        current_points=0,
        score_to_beat=7,
        opponents_left=4,
        dice=[4, 3, 1, 1, 2]
    ))
