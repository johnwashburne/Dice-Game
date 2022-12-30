# Threes Solver
Threes is a fairly simple dice game (you can read the rules [here](http://www.dice-play.com/Games/Threes.htm)). But, when playing with my family, I realized that calculating the optimal action on a given turn would be a very interesting problem to consider. 

## The Process
Because of the ability to select a non-predetermined number of dice, there is a very large number of potential outcomes. I found that modeling this large outcome space with conditional probabilities would be very complex, so a Monte Carlo approach made more sense. Rather than assigning an exact probability to each event, I could take a large number of samples from predefinied sampling distributions and receive an answer that approaches the ground truth. But, how would these distributions be built?
When I first began on this project, I used a very naive strategy of backtracking through every potential action, i.e. simulating each dice roll and keeping every combination of dice at every tier. This led to very large and impractical runtimes. \
One consideration that led to a large speedup in runtime is the observation that there are some decisions of dice to keep that simply make no sense. It really only makes sense to keep the dice with the lowest point values. So, now the program could sort the dice by point value and at each tier only had to consider at most 5 possibilities.
