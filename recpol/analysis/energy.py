import numpy as np
import matplotlib.pyplot as plt
import os



files = []
energy = []
avrgMagnetization =[]

for filename in os.listdir('logfolder'):
    if filename.endswith(".lammps"):
        files.append(os.path.join('logfolder', filename))
        continue
    else:
        continue

equilibration = 10
currentEqui = 0
new = []
energy = []
hCap =[]
currentEn = 0
startCount = 0
stopCount = 0
avrgEnergy = []
x = []
for filename in files:
    with open(filename, 'r') as f:
        energy= []
        startCount = 0
        stopCount = 0
        for line in f:
            test = line.split(' ')
            if startCount == 2 and test[0] == 'Loop':
                stopCount+=1
            if test[0] == 'Step':
                startCount +=1
                continue
            if startCount == 2 and stopCount == 0:
                count = 0
                #print(test)
                for i in test:
                    if count ==2 and i!= '':
                        energy.append(float(i))
                        break
                    elif i!= '':
                        count+=1
    avrgEnergy.append(np.mean(energy))
    hCap.append((1.0/1.0)*(np.mean(np.power(energy,2))-np.power(np.mean(energy),2)))

    for i in range(len(filename)):
        if filename[i] == 'a':
            en = filename[i-4]+filename[i-3]
            x.append(float(en)/10.0)

print(x)

f = open('energyResults.txt', 'w')
f.write("E  avrgEnergy  HeatCap\n")
for i in range(len(x)):
    f.write(str(x[i])+ ' ' + str(avrgEnergy[i]) + ' ' + str(hCap[i]) + '\n')
f.close()
plt.style.use('seaborn')
plt.plot(x,avrgEnergy)
plt.title("Average Energy per bead")
plt.xlabel('a')
plt.ylabel('(avrg E)/N')
plt.savefig('en.png')
plt.show()
plt.plot(x,hCap)
plt.title("Heat capacity")
plt.xlabel('a')
plt.ylabel('C/N')
plt.savefig('hc.png')
plt.show()
