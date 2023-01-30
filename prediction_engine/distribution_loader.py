# Utilize a bottom-up strategy to build sampling distributions of
#   expected points added by number dice rolled.

import numpy as np
from typing import Dict, Optional, Any
import os
import json


class Distribution:

    """
    Class to hold distributions and metadata
    """

    def __init__(
            self,
            distributions: np.ndarray,
            point_mapping: Dict[int, int],
            num_dice: int
            ) -> None:
        self.distributions = distributions
        self.point_mapping = point_mapping
        self.num_dice = num_dice


class DistributionLoader:

    @staticmethod
    def build(
            num_dice: int,
            point_mapping: Dict[int, int],
            num_samples: int = 1000,
            name: Optional[str] = None
            ) -> Distribution:
        """
        Build sampling distributions for expected additional points by number
            of dice rolled
        Args:
            num_dice(int): build distributions for each number of dice rolled
                up to and including num_dice
            point_mapping(dict): a mapping from dice face values to game
                points
            num_samples(int): the number of samples to take for each possible
                number of dice rolled
            name(None, str): if specified, write the distribution to disk with
                specified name. If not specified, distributions will not
                be saved
        Returns:
            sampling distributions
        """

        base_path = os.path.dirname(os.path.realpath(__file__))

        # needs to be of length num_samples to make array conversion possible
        distribution_list = [np.array([0] * num_samples)]
        face_values = list(point_mapping.keys())

        for i in range(1, num_dice+1):
            samples = []
            for _ in range(num_samples):

                # roll i dice and convert to sorted point values
                roll = [point_mapping[np.random.choice(face_values)] for _ in range(i)]
                roll.sort()

                # begin with keeping all dice
                min_points = sum(roll)
                for j in range(len(roll) - 1):

                    # keep the lowest j+1 points
                    kept_points = roll[:j+1]

                    # reroll the remaining dice, using the previously
                    #   built sampling distribution
                    num_remaining_dice = len(roll) - len(kept_points)
                    points = sum(kept_points) + np.random.choice(
                        distribution_list[num_remaining_dice])

                    # Play optimally, keep the minimum possible number
                    #   of points. Note: this knowledge would not be
                    #   available to the player at time of game, but this
                    #   step is taken to simplify sampling, since we
                    #   assume the player is rational and will attempt
                    #   to play optimally
                    min_points = min(min_points, points)
                samples.append(min_points)

            distribution_list.append(np.array(samples))

        distributions = np.array(distribution_list)

        # store distribution and metadata
        if name is not None:
            info: Dict[str, Any] = {}
            binary_path = os.path.join(base_path, "distributions\\binaries", f"{name}.npy")
            info["bin"] = binary_path
            info["point_mapping"] = point_mapping
            info["num_dice"] = num_dice

            np.save(binary_path, distributions)
            with open(os.path.join(base_path, "distributions", f"{name}.json"), 'w') as f:
                json.dump(info, f)

        result = Distribution(distributions, point_mapping, num_dice)
        return result

    @staticmethod
    def load(name: str) -> Distribution:
        """
        Load distribution and metadata
        Args:
            name(str): name of stored distribution
        Returns:
            Distribution: object containing distribution and metadata
        """

        base_path = os.path.dirname(os.path.realpath(__file__))

        path = os.path.join(base_path, "distributions", f"{name}.json")
        print(path)
        if not os.path.exists(path):
            raise ValueError("Name could not be found")

        with open(path, 'r') as f:
            info = json.load(f)

        binary_path = info["bin"]
        distributions = np.load(binary_path)
        point_mapping = {int(k): v for k, v in info["point_mapping"].items()}
        num_dice = info["num_dice"]
        return Distribution(distributions, point_mapping, num_dice)


if __name__ == "__main__":

    # example of building a sampling distribution
    point_mapping = {
        1: 1,
        2: 2,
        3: 0,
        4: 4,
        5: 5,
        6: 6
    }
    DistributionLoader.build(5, point_mapping, 1000000, "default")
