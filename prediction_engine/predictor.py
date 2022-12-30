from typing import List, Tuple
import random
import statistics
from prediction_engine.distribution_loader import Distribution


class Predictor:

    def __init__(self, dist: Distribution) -> None:
        """
            Initialize predictor with a sampling distribution object
        """
        self.distributions = dist.distributions
        self.point_mapping = dist.point_mapping
        self.total_dice = dist.num_dice

    def optimize_turn(
            self,
            current_points: int,
            score_to_beat: int,
            opponents_left: int,
            dice: List[int],
            num_trials: int = 10000) -> Tuple[List[int], float]:
        """
        Determine which dice to keep
        Args:
            current_points(int): the number of points the player is carrying
                into the turn
            score_to_beat(int): the current leading score
            dice(List[int]): the player's current roll
            num_trials(int): number of times to sample the distribution
        Returns:
            tuple(list, float): dice to keep, percent of sampled games
                this action won
        """
        # pair each dice face value with its point value
        dice_points = [(i, self.point_mapping[i]) for i in dice]

        # sort and extract points for input to the internal optimize function
        dice_points.sort(key=lambda x: x[1])
        points = [i[1] for i in dice_points]
        result = self._optimize_turn(
            current_points, score_to_beat, opponents_left, points, num_trials)

        # use result to return which dice to keep
        idx = self.argmax(result)
        sorted_dice = [i[0] for i in dice_points]
        return sorted_dice[:idx+1], result[idx]

    def _optimize_turn(
            self,
            current_points: int,
            score_to_beat: int,
            opponents_left: int,
            points: List[int],
            num_trials: int) -> List[float]:
        """
        INTERNAL - Given a roll of the dice, determine the proportion of
            turns played by keeping the i dice with the lowest point value
            that beat the score_to_beat
        Args:
            current_points(int): the number of points the player is carrying
                into the turn
            score_to_beat(int): the current leading score
            points(List[int]): the player's current roll point representation,
                sorted
            num_trials(int): number of times to sample the distribution
        """
        results = []
        num_dice = len(points)

        # sample each possible dice roll
        # i.e. keeping 1 die, 2 dice, 3 dice, etc.
        for i in range(1, num_dice + 1):
            samples = []
            for _ in range(num_trials):

                # keep the i smallest point values
                kept_points = points[:i]
                dice_to_roll = num_dice - i

                # sample the point distributions to calculate point projection
                future_points = random.choice(self.distributions[dice_to_roll])
                projection = current_points + sum(kept_points) + future_points

                # determine if sampled score projection is good enough
                #   to take the lead over current score to beat,
                #   then sample future opponents to determine if sampled
                #   score projection will beat them as well
                if projection < score_to_beat:

                    # sample future opponents
                    min_val = float('inf')
                    for _ in range(opponents_left):
                        min_val = min(
                            min_val, random.choice(
                                self.distributions[self.total_dice]))

                    # check if score projection still wins
                    if projection < min_val:
                        samples.append(1)
                    else:
                        samples.append(0)
                else:
                    samples.append(0)

            results.append(statistics.mean(samples))
        return results

    @staticmethod
    def argmax(lst):
        """ Find the argmax of lst """
        return lst.index(max(lst))
