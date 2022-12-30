from prediction_engine.distribution_loader import DistributionLoader
import matplotlib.pyplot as plt

if __name__ == "__main__":
    d = DistributionLoader.load("default")

    for i in range(len(d.distributions)):
        plt.hist(d.distributions[i], bins=[-0.5 + j for j in range(max(d.distributions[i])+2)])
        plt.title(f"{i} Dice")
        plt.yticks([])
        plt.xlabel("Points Added")
        plt.savefig(f"visualizations/{i}.png")
        plt.show()

    # all plot
    rows = 2
    cols = 3
    fig, axs = plt.subplots(rows, cols)
    
    for i in range(len(d.distributions)):
        axs[i // cols, i % cols].hist(d.distributions[i], bins=[-0.5 + j for j in range(max(d.distributions[i])+2)])
        axs[i // cols, i % cols].set_title(f"{i} Dice")
        axs[i // cols, i % cols].set(yticks=[])
        
    
    plt.show()