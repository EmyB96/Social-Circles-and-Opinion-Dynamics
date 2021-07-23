import networkx as nx
from pylab import *
from statistics import mean
from itertools import groupby
from tqdm import tqdm
from os.path import isfile, join

# reading files
G = #networkX graph
#pos = nx.spring_layout(G)

def initialize():
    global G, nextG, pos, stepaverageopinion
    for node in G.nodes():
        G.nodes[node]['state'] = 1 if random() < 0.5 else 0
    nextG = G.copy()
    stepaverageopinion = {}

def observe():
    global G, nextG
    cla()
    ##it takes too long to plot this for the directed graphs
    # nx.draw(nextG, cmap = cm.binary, vmin = 0, vmax = 1,
    #         node_color = [G.nodes[node]['state'] for node in G.nodes()], edgecolors='black',
    #         pos = pos)

def observeOpinion(currentstep):
    global G, nextG, statesdict
    cla()
    print(currentstep)

    statesdict = dict(G.nodes(data='state'))
    #print(statesdict)
    averageopinion = mean(statesdict[node] for node in statesdict)
    print(averageopinion)

    stepaverageopinion[currentstep] = averageopinion
    ##it takes too long to plot this for the directed graphs
    # liststepaverageopinion = sorted(stepaverageopinion.items())
    # x, y = zip(*liststepaverageopinion)
    # plt.plot(x, y)
    # for x, y in liststepaverageopinion:
    #     plt.annotate(str(round(y,4)), xy=(x,y), xytext=(10,10), textcoords='offset points')
    # plt.title('Average opinion per step')
    # plt.xlabel('Step')
    # plt.ylabel('Average opinion')

def stopping(currentstep): #Steady-state is reached when the average opinion is the same for 4 steps long or (i)&(i+2) and (i+1)&(i+3) are the same
    steadystatelist = []

    def all_equal(list):
        g = groupby(list)
        return next(g, True) and not next(g, False)

    def two_times_same(list):
        if list[0] == list[2] and list[1] == list[3]:
            return True
        else:
            return False

    if len(stepaverageopinion) > 3:
        steadystatelist.append(stepaverageopinion[currentstep-3])
        steadystatelist.append(stepaverageopinion[currentstep-2])
        steadystatelist.append(stepaverageopinion[currentstep-1])
        steadystatelist.append(stepaverageopinion[currentstep])

        if all_equal(steadystatelist) or two_times_same(steadystatelist):
            return True
        elif currentstep == 50: #with 50 steps, we can assume that it is in some kind of loop
            return True
        else:
            return False

def update():
    global G, nextG
    for node in G.nodes():
        weigthedopinioncount = 0
        weightcount = 0
        for neighbor in G.neighbors(node):
            weightedopinion = pow(G[node][neighbor]['weight'], 0.5) * G.nodes[neighbor]['state'] #adjust influence parameter rho here
            weigthedopinioncount += weightedopinion
            weightcount += pow(G[node][neighbor]['weight'], 0.5) #adjust influence parameter rho here
        if weightcount == 0:
            continue #if there are no neighbors that are in the any of the matching circles, there will be no impact on the node
        else:
            ratio = weigthedopinioncount / weightcount

        nextG.nodes[node]['state'] = 1 if ratio > 0.5 \
            else 0 if ratio < 0.5 \
            else G.nodes[node]['state'] #1 if random() < 0.5 else 0 #Flipping the coin if it's exactly 0.5
    G, nextG = nextG, G

import pycxsimulator

stepaverageopinionsims = {}
# statessims = {}
print('Running simulations:')
for i in tqdm(range(35)):
    pycxsimulator.GUI().start(func=[initialize, observe, observeOpinion, stopping, update])
    stepaverageopinionsims[i+1] = stepaverageopinion

mypath = #path were files should be saved
# print(stepaverageopinionsims)
averageopinionfile = #file name
with open(join(mypath, (averageopinionfile + ".txt")), 'w') as file:
    file.write(str(stepaverageopinionsims))