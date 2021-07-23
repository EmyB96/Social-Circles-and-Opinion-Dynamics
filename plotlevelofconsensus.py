import matplotlib.pyplot as plt

stepaverageopinionsims = #dict with average opinion per step, for n simulations

plt.figure(figsize=(20, 8.7))
for sim, dictstepaverageopinion in stepaverageopinionsims.items():
    dictsteplevelofconsensus = {}
    for step, stepaverageopinion in dictstepaverageopinion.items():
        levelofconsensus = 2 * abs(stepaverageopinion - 0.5)
        dictsteplevelofconsensus[step] = levelofconsensus

    liststeplevelofconsensus = sorted(dictsteplevelofconsensus.items())
    x, y = zip(*liststeplevelofconsensus)

    plt.plot(x, y, label=sim)
plt.title('Level of consensus per step')
plt.xlabel('Step')
plt.ylabel('Level of consensus')
plt.legend(title='Simulation')
plt.show()
