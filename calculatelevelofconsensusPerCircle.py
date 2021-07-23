import networkx as nx
from pylab import *
from statistics import mean
from os import listdir
from os.path import isfile, join
import scipy.stats as stats

# reading files
G = #networkX graph
pos = nx.spring_layout(G)
mypath = #path were circle files are saved
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f.endswith(".edges")]

# reading ego networks
egonets = {}
for f in onlyfiles:
    ego = ("ego" + f.strip('.edges'))
    egonets[ego] = nx.read_edgelist(join(mypath, f))

# reading circles
egos = [s.strip('.edges') for s in onlyfiles]
egocircles = {}
for ego in egos:
    circlefile = ego + ".circles"
    circledict = {}
    with open(join(mypath, circlefile), 'r') as infile:
        lis = [line.split() for line in infile]  # create a list of lists
        for x in lis:  # print the list items
            circlenodes = x[1:]  # add ego node to all its circles
            circlenodes.append(ego)
            circledict[x[0]] = circlenodes
    egocircles[ego] = circledict
print(egocircles)


def level_of_consensus(egocircles, statessims):
    # Calculate level of consensus for every simulation
    egocircleinfo = {}
    for ego in egocircles:
        circledict = egocircles[ego]
        circleinfo = {}
        for circle, circlenodes in circledict.items():
            levelofconsensuslist = []
            for sim, stepstates in statessims.items():
                circlestates = []
                for node in circlenodes:
                    state = stepstates[node]
                    circlestates.append(state)
                averageopinion = mean(circlestates)
                levelofconsensus = 2 * abs(averageopinion - 0.5)
                levelofconsensuslist.append(levelofconsensus)
            circleinfo[circle] = levelofconsensuslist
        egocircleinfo[ego] = circleinfo
    return egocircleinfo

# define node states of every simulation: two models which will be compared
statessimsa = #dict with opinion for each node per step, for n simulations
statessimsb = #dict with opinion for each node per step, for n simulations

level_of_consensusa = level_of_consensus(egocircles, statessimsa)
level_of_consensusb = level_of_consensus(egocircles, statessimsb)
print(level_of_consensusa)
print(level_of_consensusb)

significantchanges = []
for ego in egocircles:
    circledict = egocircles[ego]
    print(ego)
    circleinfoa = level_of_consensusa[ego]
    circleinfob = level_of_consensusb[ego]

    for circle in circledict:
        print(circle)
        levelofconsensuslista = circleinfoa[circle]
        levelofconsensuslistb = circleinfob[circle]
        print(levelofconsensuslista)
        print("Average level of consensus a: " + str(mean(levelofconsensuslista)))
        print(levelofconsensuslistb)
        print("Average level of consensus b: " + str(mean(levelofconsensuslistb)))

        if levelofconsensuslista != levelofconsensuslistb:
            bartlettstat, bartlettp = stats.bartlett(levelofconsensuslista, levelofconsensuslistb)
            #print("p-value Bartlett’s test for equal variances: " + str(bartlettp)) #test for equal variances

            if bartlettp > 0.05:
                tteststat, ttestp = stats.ttest_ind(levelofconsensuslista, levelofconsensuslistb, equal_var=True)
                print("p-value Two Sample t-Test: " + str(ttestp))
            else:
                tteststat, ttestp = stats.ttest_ind(levelofconsensuslista, levelofconsensuslistb, equal_var=False)
                print("p-value Two Sample t-Test: " + str(ttestp))
            ##Greater than alpha = 0.05, we fail to reject the null hypothesis of the test. We do not have sufficient evidence to say that the mean between the two populations is different.
            if ttestp > 0.05:
                print("Mean between the both models is different: No")
                significantchanges.append(0)
            else:
                print("Mean between the both models is different: Yes")
                significantchanges.append(1)
            print("\n")
        else:
            print("Level of consensus is exactly the same for both models in all simulations" + "\n")
            significantchanges.append(0)

print(significantchanges)
consensuschange = (sum(significantchanges)/len(significantchanges)) * 100
print(consensuschange)
