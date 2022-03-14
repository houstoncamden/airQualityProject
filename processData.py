#This program is designed to process data from the Ohio Univeristy 'AirWall Project' 
#It takes the average of a handful of selected cells in the provided data, but could easily be modified to average more cells or the entire table
#Written in 3/2022 by Camden Houston | ch948118@ohio.edu
#Please feel free to use or modify this code as needed, I've made an effort to document it for future contributors.

import csv
import glob

failCnt = 0
sucessCnt = 0
avgs2D = []

filenames = glob.glob("rawData/*.csv")

#filenames = csv.reader(open("problemFilenames.txt"))
print("Begin")

for file in filenames:
        try:
            outFileName = file[8:]
            print("Processing file: %s",file )

            #This block removes the null bytes characters that the sensor outputs. 
            #These are particularly problematic for the code and causes many files that are otherwise fine to fail
            data_initial = open(file, "r")
            data = list(csv.reader((line.replace('\0','0') for line in data_initial), delimiter=","))


            #Delete the headers so that we can process data, this will be written again later
            del data[0]

            #Average col M (12), N (13), O (14), AA (26), AB(27), AC (28)
            zeros = 0
            sum = 0
            rowNums = [12,13,14,26,27,28]
            avgs = []

            bottom = 0
            for rowNum in rowNums:
                zeros = 0
                sum = 0
                rowCnt = 0
                bottom = 0
                for row in data:
                    rowCnt = rowCnt + 1
                    try:
                        sum += float(row[rowNum])
                        bottom += 1
                    except:
                        pass

                avgs.append(sum/(bottom))

            #Here we take the averages we just calculated, and put them into a format that we can later print into a single row of a csv file
            avgs1D = [file[8:-4],str(avgs[0]),str(avgs[1]),str(avgs[2]),str(avgs[3]),str(avgs[4]),str(avgs[5])]
            avgs2D.append(avgs1D)

            print("Processing of", file, "Successful")

            sucessCnt = sucessCnt + 1
        except:
            print("Failed to process: ", file)
            failCnt = failCnt + 1

print("Successful File Processes: ", sucessCnt)
print("Failed File Processes: ", failCnt)

header = ['File Name', 'pm1_0_atm', 'pm2_5_atm', 'pm10_0_atm', 'pm1__atm_b','pm2_5_atm_b','pm1__atm_b'] 
    
# name of csv file 
filename = "plantWallAverages.csv"
    
# writing to csv file 
with open(filename, 'w',newline='') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile) 
        
    # writing the fields 
    csvwriter.writerow(header) 
        
    # writing the data rows 
    csvwriter.writerows(avgs2D)



