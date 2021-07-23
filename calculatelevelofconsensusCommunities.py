import networkx as nx
from pylab import *
from statistics import mean
from community import community_louvain

def level_of_consensus(partition, statessims):
    # Calculate level of consensus for every simulation
    comminfo = {}
    for comm, commnodes in partition.items():
        levelofconsensuslist = []
        for sim, stepstates in statessims.items():
            commstates = []
            for node in commnodes:
                state = stepstates[node]
                commstates.append(state)
            averageopinion = mean(commstates)
            levelofconsensus = 2 * abs(averageopinion - 0.5)
            levelofconsensuslist.append(levelofconsensus)
        comminfo[comm] = levelofconsensuslist
    return comminfo


G = #networkX graph
pos = nx.spring_layout(G)
partition = community_louvain.best_partition(G)
print(partition)

s = set(partition.values())
print(s)

turnedpartition = {}
for node, comm in partition.items():
    if comm in turnedpartition:
        turnedpartition[comm].append(node)
    else:
        turnedpartition[comm] = [node]
print(turnedpartition)

statessims = #dict with opinion for each node per step, for n simulations

level_of_consensus = level_of_consensus(turnedpartition, statessims)
print(level_of_consensus)

locperComm = []
for comm in level_of_consensus:
    print(comm)
    levelofconsensuslist = level_of_consensus[comm]
    print(levelofconsensuslist)
    print("Average level of consensus: " + str(mean(levelofconsensuslist)) + "\n")
    locperComm.append(mean(levelofconsensuslist))

print(locperComm)
print("Average level of consensus over communities: " + str(mean(locperComm)) + "\n")

locperComm = [0.99999999999999 if x==1.0 else x for x in locperComm]

plt.figure(figsize=(20, 8.7))
binwidth = 0.05
bincalc = np.arange((round(min(locperComm) * 20) / 20)-binwidth, (round(max(locperComm) * 20) / 20) + binwidth, binwidth)
print(bincalc)
arr=plt.hist(locperComm, bins=bincalc, color = '#b669a2')
for i in range(len(bincalc)-1): #add bar count
    plt.text(arr[1][i],arr[0][i],str(round(arr[0][i])))
plt.title("Distribution of level of consensus over communities")
plt.xlabel('Level of consensus')
plt.ylabel('Frequency')
plt.show()

