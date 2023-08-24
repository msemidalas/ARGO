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
#from myutils import prnt

#Reads the Gaussian output file (.out)
print("Enter the full name of your Gaussian output file")
name = input(' ')
f = open('%s' % name, 'r')

start_string = 'Summary of Optimized Potential Surface Scan'
end_string = 'Z-MATRIX (ANGSTROMS AND DEGREES'
start_line_number = None
end_line_number = None

with open('%s' % name, 'r') as output_file:
    for line_num, line in enumerate(output_file, start=1):
        if start_string in line:
            start_line_number = line_num
        elif end_string in line and start_line_number is not None:
            end_line_number = line_num
            break

if start_line_number is not None and end_line_number is not None:
    print(f"Start line: {start_line_number}, End line: {end_line_number}")
else:
    print(f"'{start_string}' or '{end_string}' not found.")

#Extracts data the Gaussian output file (.out)
with open('fileA.txt','w') as fp:
    for i,line in enumerate(f):
        if i >= start_line_number and i <= end_line_number :
            fp.write(line)
f.close()
#The following function creates a new .csv file which contains the two selected Dihedral Angles and the corresponding
#Eigenvalues from the Gaussian output file 

# The following function extracts specific data from input files and generates a corresponding output CSV file.
def extract(var1, i):
    input_filename = f'input{i}.out'
    output_filename = f'input{i}_{i}.csv'

    with open(input_filename, 'w') as out:
        with open('fileA.txt', 'r') as f:
            for line in f:
                if var1 in line:
                    out.write(line)

    with open(input_filename, 'r') as inputfile, open(output_filename, 'w') as outputfile:

    #The following part is neccesary and it adds a space between consecutive negative Dihedral Angles and negative
    #Eigenvalues extracted from the Gaussian output file   
        for line in inputfile:
            line = line.replace('--', '')
            if '-' in line:
                line = line.replace('-', ' -')
                outputfile.write(line)
            else: 
                outputfile.write(line)

def transpose(var1):
    with open('input%i_%i.csv' %(i,i), 'r') as infile, open('out%i.csv' %i, 'w') as outfile:
        print(var1,file=outfile)
        for line in infile:
            for var1 in line.split()[1:]:
                print(var1, file=outfile)
    infile.close()
    outfile.close()

i = 1
print("Enter dihedral angle %d:" %i)
var1 = input(' ')
extract(var1,i)
transpose(var1)

#Instructions for 3d-PES plots in Gnuplot 
with open('3dPES.txt','w') as gnu1:
    print('#x axis',file=gnu1)
    print('set xlabel "Dihedral angle %s (deg)" font ", 17" rotate parallel offset 0,-1,0\n' %var1,file=gnu1)
    print('set xtics font ", 17" border out scale 2,0.75 nomirror offset character 0, -0.3, 0 autojustify',file=gnu1)
    print('#set xrange [-1:375]',file=gnu1)
    print('set mxtics 5' "\n",file=gnu1)
    
#Instructions for 2d-PES plots in Gnuplot 
with open('2dPES.txt', 'w') as gnu2:
    print('#x axis', file=gnu2)
    print('splot "final.dat" with lines', file=gnu2)
    print('set samples 25, 25', file=gnu2)
    print('set isosamples 50, 50', file=gnu2)
    print('set xlabel "Dihedral angle %s (deg)" font ", 15" offset 0,-2,0\n' % var1, file=gnu2)
    print('set xtics font ", 14" border out scale 1.1,0.5 nomirror offset character 0, -0.5, 0 autojustify', file=gnu2)
    print('set mxtics 2', file=gnu2)
    print('set xrange [93:274]', file=gnu2)
    print('', file=gnu2)

i = i + 1
print("Enter dihedral angle %d:" %i)
var1 = input(' ')   
extract(var1,i)
transpose(var1)

# Instructions for 3d-PES in Gnuplot continue here
with open('3dPES.txt', 'a') as gnu1:
    # y axis options
    print('#y axis', file=gnu1)
    gnu1.write('set ylabel "Dihedral angle %s (deg)" font ", 17" rotate parallel offset 1,0,0\n' % var1)
    print('set ytics font ", 17" border out scale 3,0.75 nomirror norotate offset character 2.5, -0.5, 0 autojustify', file=gnu1)
    print('set mxtics 5', file=gnu1)
    print('#set yrange [-1:375]', file=gnu1)
    print('', file=gnu1)
  
    # z axis
    print('#z axis', file=gnu1)
    print('set zlabel "Energy (Ha)" font ", 17" rotate by 90 offset -16,0,0', file=gnu1)
    print('set ztics font ", 17" border out scale 2,0.75', file=gnu1)
    print('set format z "%6.3f"', file=gnu1)
    print('#set zrange [-570.092:-570.07]', file=gnu1)
    print('#set ztics -570.092,0.004,-533.07', file=gnu1)
    print('#set mztics 2.5', file=gnu1)
    print('', file=gnu1)
     
    # cb
    print('#cb', file=gnu1)
    print('set cblabel "Energy (Ha)" font ", 14" norotate offset character -6.6, 11.4, 0', file=gnu1)
    print('set pm3d implicit at s', file=gnu1)
    print('set format cb "%6.3f"', file=gnu1)
    # print('#set cblabel "Energy (Ha)" font ", 14 " nomirror rotate by 90', file=gnu1)
    # print('#set cbrange [-570.092:-570.07]', file=gnu1)
    # print('#set cbtics -570.092,0.004,-533.07  font ", 12"', file=gnu1)
    print('', file=gnu1)
    
    # contour
    print('#contour', file=gnu1)
    print('set key at screen 0.2, 0.95', file=gnu1)
    print('set contour base', file=gnu1)
    print('set cntrlabel format "%7.4f" font ", 7" start 5 interval 10', file=gnu1)
    print('set cntrparam levels 20', file=gnu1)
    print('set cntrparam bspline', file=gnu1)
    print('', file=gnu1)
                            
    # grid
    print('#grid', file=gnu1)
    print('set dgrid3d 19,19', file=gnu1)
    # set dgrid3d 35,35 qnorm 3
    print('set style data lines', file=gnu1)
    print('set pm3d interpolate 0,0', file=gnu1)
    print('set palette rgbformulae 22,13,-31', file=gnu1)
    print('set ticslevel 0.1', file=gnu1)
    print('', file=gnu1)

    # plot
    print('#plot', file=gnu1)
    print('splot "final.dat" with lines', file=gnu1)
    print('replot', file=gnu1)
    print('pause -1', file=gnu1)

#################################################################
# Instructions for plotting 2d-PES in Gnuplot continue here
with open('2dPES.txt', 'a') as gnu2:
    print('#y axis', file=gnu2)
    gnu2.write('set ylabel "Dihedral angle %s (deg)" font ", 17" rotate parallel offset -6,0,0\n' % var1)
    print('set ticslevel 0', file=gnu2)
    print('set ytics font ", 14" border out scale 1.1,0.5 nomirror offset character 0, -0.5, 0 autojustify', file=gnu2)
    print('set yrange [54.6:236]', file=gnu2)
    print('set mytics 2', file=gnu2)
    print('', file=gnu2)
    
    # grid
    print('#grid', file=gnu2)
    print('set pm3d implicit at s', file=gnu2)
    print('set dgrid3d 19,19', file=gnu2)
    print('set pm3d interpolate 0,0', file=gnu2)
    print('set pm3d map', file=gnu2)
    print('set palette rgbformulae 22,13,-31', file=gnu2)
    print('', file=gnu2)
    # The dgrid3d is set at 19,19 because those numbers correspond to the scan steps
    # set dgrid3d 35,35 qnorm 3
    
    # cb
    print('#cb', file=gnu2)
    print('set cblabel "Energy (Ha)" font ", 14" norotate offset character -6, 25, 0', file=gnu2)
    print('set cbtics font ", 12"', file=gnu2)
    print('set format cb "%6.3f"', file=gnu2)
    print('set key at screen 0.08, 0.95', file=gnu2)
    print('', file=gnu2)
    # print('#set cbrange [-533.351:-533.338]', file=gnu2)
    print('', file=gnu2)
    
    # contour
    print('#contour', file=gnu2)
    print('set contour base', file=gnu2)
    print('set cntrparam levels 20', file=gnu2)
    print('set cntrparam bspline', file=gnu2)
    print('set style data lines', file=gnu2)
    print('set cntrlabel format "%7.4f" font ", 7" start 5 interval 10', file=gnu2)
    print('', file=gnu2)
    
    # plot
    print('set colorbox vertical user origin .9, .1 size .04,.8', file=gnu2)
    print('splot "final.dat" with lines', file=gnu2)
    print('set ticslevel 0.1', file=gnu2)
    print('replot', file=gnu2)
    print('pause -1', file=gnu2)

i = i + 1
var1 = 'Eigenvalues'
extract(var1,i)
transpose(var1)

#The remaining section of the code merges the three columns of chosen Dihedral Angles and Eigenvalues into a single "final.dat" file. This file is utilized by Gnuplot for plotting the 3D and 2D Potential Energy Surfaces (PES).

def merge_and_process_csv(input1, input2, output):
    with open(input1, 'r') as f1, open(input2, 'r') as f2, open(output, 'w') as w:
        writer = csv.writer(w)
        for r1, r2 in zip(csv.reader(f1), csv.reader(f2)):
            writer.writerow(r1 + r2)

merge_and_process_csv('out1.csv', 'out2.csv', 'merged_1.csv')
merge_and_process_csv('merged_1.csv', 'out3.csv', 'merged_2.csv')

with open('merged_2.csv', 'r') as inputfile, open('merged_3.csv', 'w') as outputfile:
    for line in inputfile:
        outputfile.write(line.replace(',', ' '))

with open("merged_3.csv", 'r') as f:
    with open("final.dat", 'w') as f3:
        next(f)  # skip header line
        print('#X Y Z', file=f3)
        f3.writelines(f)
    
print('Do you want to delete intermediate files? (yes or no)')
question = input(' ')

if question == "yes":
    files_to_remove = [
        'fileA.txt', 'input1.out', 'input2.out', 'input3.out', 
        'input1_1.csv', 'input2_2.csv', 'input3_3.csv', 
        'out1.csv', 'out2.csv', 'out3.csv', 
        'merged_1.csv', 'merged_2.csv', 'merged_3.csv'
    ]
    
    for filename in files_to_remove:
        os.remove(filename)
elif question == 'no':
    pass
