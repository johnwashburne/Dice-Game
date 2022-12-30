from prediction_engine.distribution_loader import DistributionLoader
import matplotlib.pyplot as plt

if __name__ == "__main__":
    d = DistributionLoader.load("default")
    for i in range(len(d.distributions)):
        plt.hist(d.distributions[i], bins=[-0.5 + j for j in range(max(d.distributions[i])+2)])
        plt.title(f"{i} Dice")
        plt.savefig(f"visualizations/{i}.png")
        plt.show()