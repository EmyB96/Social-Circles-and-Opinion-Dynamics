from statistics import mean
import scipy.stats as stats
from os.path import join


# two models which will be compared
stepaverageopinionsimsa = #dict with average opinion per step, for n simulations
stepaverageopinionsimsb = #dict with average opinion per step, for n simulations

finallevelofconsensuslista = []
for sim, stepaverageopinion in stepaverageopinionsimsa.items():
    finalaverageopinionstep = len(stepaverageopinion)-1
    #print(stepaverageopinion[finalaverageopinionstep])
    meanaverageopinion = (stepaverageopinion[finalaverageopinionstep] + stepaverageopinion[finalaverageopinionstep -1]) /2 #mean of last two steps for the oscillations case
    levelofconsensus = 2 * abs(meanaverageopinion - 0.5)
    #levelofconsensus = 2 * abs(stepaverageopinion[finalaverageopinionstep] - 0.5)
    #print(levelofconsensus)
    finallevelofconsensuslista.append(levelofconsensus)
print("Average level of consensus a: " + str(mean(finallevelofconsensuslista)))

finallevelofconsensuslistb = []
for sim, stepaverageopinion in stepaverageopinionsimsb.items():
    finalaverageopinionstep = len(stepaverageopinion)-1
    #print(stepaverageopinion[finalaverageopinionstep])
    meanaverageopinion = (stepaverageopinion[finalaverageopinionstep] + stepaverageopinion[finalaverageopinionstep -1]) /2  #mean of last two steps for the oscillations case
    levelofconsensus = 2 * abs(meanaverageopinion - 0.5)
    #levelofconsensus = 2 * abs(stepaverageopinion[finalaverageopinionstep] - 0.5)
    #print(levelofconsensus)
    finallevelofconsensuslistb.append(levelofconsensus)
print("Average level of consensus b: " + str(mean(finallevelofconsensuslistb)))

bartlettstat, bartlettp = stats.bartlett(finallevelofconsensuslista, finallevelofconsensuslistb)
print("p-value Bartlett’s test for equal variances: " + str(bartlettp)) #test for equal variances

if bartlettp > 0.05:
    tteststat, ttestp = stats.ttest_ind(finallevelofconsensuslista, finallevelofconsensuslistb, equal_var=True)
    print("p-value Two Sample t-Test: " + str(ttestp))
else:
    tteststat, ttestp = stats.ttest_ind(finallevelofconsensuslista, finallevelofconsensuslistb, equal_var=False)
    print("p-value Two Sample t-Test: " + str(ttestp))
##Greater than alpha = 0.05, we fail to reject the null hypothesis of the test. We do not have sufficient evidence to say that the mean between the two populations is different.