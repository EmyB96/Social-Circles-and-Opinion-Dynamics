import matplotlib.pyplot as plt

stepaverageopinionsims = #dict with average opinion per step, for n simulations


plt.figure(figsize=(20, 8.7))
for sim, dictstepaverageopinion in stepaverageopinionsims.items():
    liststepaverageopinion = sorted(dictstepaverageopinion.items())
    x, y = zip(*liststepaverageopinion)

    plt.plot(x, y, label=sim)
plt.title('Average opinion per step')
plt.xlabel('Step')
plt.ylabel('Average opinion')
plt.legend(title='Simulation')
plt.show()