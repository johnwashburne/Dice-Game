# Threes Solver
Threes is a fairly simple dice game (you can read the rules [here](http://www.dice-play.com/Games/Threes.htm)). But, when playing with my family, I realized that calculating the optimal action on a given turn would be a very interesting problem to consider. 

## The Process
Because of the ability to select a non-predetermined number of dice, there is a very large number of potential outcomes. I found that modeling this large outcome space with conditional probabilities would be very complex, so I decided that a Monte Carlo approach made more sense. Rather than assigning an exact probability to each event, I could take a large number of samples from predefinied sampling distributions and receive an answer that approaches the ground truth. 
