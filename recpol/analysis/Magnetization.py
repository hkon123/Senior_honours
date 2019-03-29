import numpy as np
import matplotlib.pyplot as plt
import os

files = []
energy = []
avrgMagnetization =[]

for filename in os.listdir('resultsFolder'):
    if filename.endswith(".xyz"):
        files.append(os.path.join('resultsFolder', filename))
        continue
    else:
        continue

equilibration = 10
currentEqui = 0
new = []
magnetization = []
susceptibility =[]
currentMag = 0
for filename in files:
    with open(filename, 'r') as f:
        for line in f:
            test = line.split(' ')
            if test[0] == 'Atoms.':
                if currentEqui>= equilibration:
                    magnetization.append(currentMag)
                    currentMag=0
                else:
                    currentEqui+=1
            elif test[0] == 'C' and currentEqui>=equilibration:
                currentMag+=1
            elif test[0] == 'O' and currentEqui>=equilibration:
                currentMag -=1
        magnetization.append(currentMag)
    f.close()
    #print(magnetization)
    avrgMagnetization.append(np.mean(magnetization))
    susceptibility.append((1.0/500.0)*(np.mean(np.power(magnetization,2))-np.power(np.mean(magnetization),2)))

    x =np.arange(0,len(magnetization),1)
    for i in range(len(filename)):
        if filename[i] == 'E' and filename[i+3] == 'x':
            energy.append(float(filename[i+1]))
            break
        elif filename[i] == 'E' and filename[i+5] == 'x':
            en = filename[i+1]+filename[i+2]+filename[i+3]
            energy.append(float(en))
    #plt.plot(x,magnetization)
    #plt.show()
for i in range(20):
    for i in range(len(energy)-1):
        if energy[i] > energy[i+1]:
            temp = energy[i]
            energy[i] = energy[i+1]
            energy[i+1] = temp
            temp = avrgMagnetization[i]
            avrgMagnetization[i] = avrgMagnetization[i+1]
            avrgMagnetization[i+1] = temp
            temp = susceptibility[i]
            susceptibility[i] = susceptibility[i+1]
            susceptibility[i+1] = temp


newMag = []
newEnergy = []
newSus = []

for i in range(1,(len(energy))):
    if energy[i] == energy[i-1]:
            newEnergy.append(energy[i])
            newMag.append((avrgMagnetization[i]+avrgMagnetization[i-1])/2.0)
            newSus.append((susceptibility[i]+susceptibility[i-1])/2.0)
            test = False
    else:
        if test == False:
            test = True
            continue
        elif i == len(energy):
            newEnergy.append(energy[i])
            newMag.append((avrgMagnetization[i]))
            newSus.append((susceptibility[i]))
        else:
            newEnergy.append(energy[i-1])
            newMag.append((avrgMagnetization[i-1]))
            newSus.append((susceptibility[i-1]))



print(newEnergy)

f = open('magResults.txt', 'w')
f.write("E  avrgMagnetization  susceptibility")
for i in range(len(energy)):
    f.write(str(energy[i])+ ' ' + str(avrgMagnetization[i]) + ' ' + str(susceptibility[i]) + '\n')
f.close()
plt.style.use('seaborn')
plt.plot(newEnergy,newMag)
plt.title("magnetization")
plt.xlabel('a')
plt.ylabel('M')
plt.savefig('mag.png')
plt.show()
plt.plot(newEnergy,newSus)
plt.title("susceptibility")
plt.xlabel('a')
plt.ylabel('X')
plt.savefig('sus.png')
plt.show()
