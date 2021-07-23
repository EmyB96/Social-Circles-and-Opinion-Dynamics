import networkx as nx
from pylab import *
from statistics import mean
from itertools import groupby
from tqdm import tqdm
from os import listdir
from os.path import isfile, join

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

# update edge weight according to number of circles both endnodes belong to
print('Updating edge weights according to number of circles both endnodes belong to:')
for edge in tqdm(G.edges()):
    source = edge[0]
    target = edge[1]
    G.add_edge(source, target, weight = 0)

    for ego in egocircles:
        circledict = egocircles[ego]
        for circle in circledict:
            if all([x in circledict[circle] for x in [source, target]]):
                G.add_edge(source, target, weight = G[source][target]['weight'] + 1)
#print(nx.get_edge_attributes(G,'weight'))


def initialize():
    global G, nextG, pos, stepaverageopinion
    for node in G.nodes():
        G.nodes[node]['state'] = 1 if random() < 0.5 else 0
    nextG = G.copy()
    stepaverageopinion = {}

def observe():
    global G, nextG
    cla()
    nx.draw(nextG, cmap = cm.binary, vmin = 0, vmax = 1,
            node_color = [G.nodes[node]['state'] for node in G.nodes()], edgecolors='black',
            pos = pos)

def observeOpinion(currentstep):
    global G, nextG, statesdict
    cla()
    #print(currentstep)

    statesdict = dict(G.nodes(data='state'))
    #print(statesdict)
    averageopinion = mean(statesdict[node] for node in statesdict)
    #print(averageopinion)

    stepaverageopinion[currentstep] = averageopinion
    liststepaverageopinion = sorted(stepaverageopinion.items())
    x, y = zip(*liststepaverageopinion)
    plt.plot(x, y)
    for x, y in liststepaverageopinion:
        plt.annotate(str(round(y,4)), xy=(x,y), xytext=(10,10), textcoords='offset points')
    plt.title('Average opinion per step')
    plt.xlabel('Step')
    plt.ylabel('Average opinion')

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
        elif currentstep == 50:  # with 50 steps, we can assume that it is in some kind of loop
            return True
        else:
            return False

def update():
    global G, nextG
    for node in G.nodes():
        weigthedopinioncount = 0
        weightcount = 0
        for neighbor in G.neighbors(node):
            weightedopinion = pow(G[node][neighbor]['weight'], 0.5) * G.nodes[neighbor]['state']
            weigthedopinioncount += weightedopinion
            weightcount += pow(G[node][neighbor]['weight'], 0.5)
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
statessims = {}
print('Running simulations:')
for i in tqdm(range(35)):
    pycxsimulator.GUI().start(func=[initialize, observe, observeOpinion, stopping, update])
    stepaverageopinionsims[i+1] = stepaverageopinion
    statessims[i+1] = statesdict

mypath = #path were files should be saved
# print(stepaverageopinionsims)
averageopinionfile = #file name
with open(join(mypath, (averageopinionfile + ".txt")), 'w') as file:
    file.write(str(stepaverageopinionsims))

# print(statessims)
statesfile = #file name
with open(join(mypath, (statesfile + ".txt")), 'w') as file:
    file.write(str(statessims))