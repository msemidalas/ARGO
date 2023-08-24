#Argo, an open-source data analysis software for quantum chemical calculations
#Copyright (C) 2016-2023 Emmanouil Semidalas, Charis Semidalas.
#E-mail:msemidalas@yahoo.com, chsemid@teiath.gr

#Argo is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with Argo; if not, see <https://www.gnu.org/licenses/>.

import os
import csv
from array import *
import scipy.constants as const
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

filename = input("Enter the filename (e.g., ch3oh.log): ")

# Read the input text
with open(filename, 'r') as f:
    lines = f.readlines()

frequencies = []

for line in lines:
    if 'Frequencies --' in line:
        values = line.strip().split()[2:]
        frequencies.extend(values)

with open('frequencies.csv', 'w') as f:
    for value in frequencies:
        f.write(value + '\n')

IR_intensities = []
for line in lines:                                                                                                                   
    if 'IR Inten    --' in line:                                                                                                     
        values = line.strip().split()[2:]                                                                                            
        cleaned_values = [value for value in values if '--' not in value]
        IR_intensities.extend(cleaned_values) 
                                                                                                                                     
with open('IR_intensities.csv', 'w') as f:                                                                                              
    for value in IR_intensities:                                                                                                    
        f.write(value + '\n')   

Raman_activities = []
for line in lines:
    if 'Raman Activ --' in line:
        values = line.strip().split()[2:]                                                                                            
        cleaned_values = [value for value in values if '--' not in value]
        Raman_activities.extend(cleaned_values)  
                                                                                                                                     
with open('Raman_activities.csv', 'w') as f:                                                                                              
    for value in Raman_activities:                                                                                                    
        f.write(value + '\n')    

header_row = ["Frequency", "IR_Intensity", "Raman_Activity"]
with open('frequencies.csv', 'r') as f1, \
     open('IR_intensities.csv', 'r') as f2, \
     open('Raman_activities.csv', 'r') as f3, \
     open('IR_Raman.csv', 'w') as outputfile:

    csv_writer = csv.writer(outputfile)
    csv_writer.writerow(header_row) 
    for r1, r2, r3 in zip(csv.reader(f1), csv.reader(f2), csv.reader(f3)):
        csv_writer.writerow(r1 + r2 + r3)

os.remove("frequencies.csv")
os.remove("IR_intensities.csv")
os.remove("Raman_activities.csv")

pi, k, c, h, n_a = const.pi, const.k, const.c, const.h, const.N_A

v0 = float(input('Insert frequency value of laser excitation (cm-1): (e.g., 18796.99 cm-1) \n'))
T = float(input('Insert temperature value (K): (e.g., 298.15 K)\n'))

df = pd.read_csv("IR_Raman.csv", sep=",", dtype=float)
df["Raman_Intensity"] = (n_a * (10**9) * (2*pi)**4 / 45) * ((v0 - df['Frequency'])**4) * ((h*df['Raman_Activity']) / (8*pi*pi*c*100*df['Frequency']*(1-np.exp(-((h*c*100*df['Frequency'])/(k*T))))))
print(df)
df.to_csv('IR_Raman.csv', encoding='utf-8', index=False)

# Plot bar charts:
data = pd.read_csv("IR_Raman.csv")
frequency = data['Frequency']
Raman_intensity = data['Raman_Intensity']
IR_intensity = data['IR_Intensity']

frequency = np.array(frequency)
Raman_intensity = np.array(Raman_intensity)

# Plot the data as a bar chart
plt.bar(frequency,IR_intensity, width=20, align='center', alpha=0.7)
plt.xlabel('Frequency')
plt.ylabel('IR Intensity')
plt.title('IR Intensity vs. Frequency')
plt.savefig("IR_Intensities.png", dpi=300, bbox_inches='tight')
plt.close()

plt.bar(frequency,Raman_intensity, width=20, align='center', alpha=0.7)
plt.xlabel('Frequency')
plt.ylabel('Raman Intensity')
plt.title('Raman Intensity vs. Frequency')
plt.savefig("Raman_Intensities.png", dpi=300, bbox_inches='tight')
