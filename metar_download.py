#Ogimet.com latest metar scraper
#Made by: SvenAzari

import requests
import sys
import re
import os
import datetime
from datetime import timezone

#How to set up:
#  1. Use https://ogimet.com/umetars.phtml.en to choose country 
#  2. Choose tekst format.
#  3. After opening query, copy url.
#  4. Do not forget to uncomment 3 lines if you wanna write scraped lines into file!

url = "https://ogimet.com/ultimos_metars2.php?lang=en&estado=Croa&fmt=txt&iord=yes&Send=Send" #paste url here (current url is for Croatia)
r = requests.get(url, allow_redirects=True)
open('latest_metar.txt', 'wb').write(r.content) #writing content of webpage into file

synop = open ("latest_metar.txt") #openning file where content of webpage is saved

#search for <pre> and </pre> tags
lookup1 = "<pre>"
lookup2 = "</pre>"

#look for line of beginning tag
with open("latest_metar.txt") as myFile:
    for numx, line in enumerate(myFile, 1):
        if lookup1 in line:
            x = numx
            
#look for line of ending tag
with open("latest_metar.txt") as myFile:
    for numy, line in enumerate(myFile, 1):
        if lookup2 in line:
            y = numy

lines_to_read = range (x+7, y-1) #lines to scrap

dt = datetime.datetime.now(timezone.utc) #utc time
hourutc = str(dt.hour) #utc hour

linesx = [] #list where lines are saved

for position, line in enumerate(synop):
    if position in lines_to_read:
        linesx.append(line) #add lines to list
        
linesy = "".join(linesx) #all lines in one giant string
linesnew = linesy.split("=\n") #split linesy

met = open("/home/azari/scripts/metar.txt", "w+") #creating and opening file to write scraped lines into (uncomment to use - 1/4)

c = 0

while True:
    try:
        metar = linesnew[0+c] #new string for each report
        metarx = re.split(' |\n', metar) #split last line string to list
        while("" in metarx): #remove unnecessary spaces
            metarx.remove("")
        if metarx[2] == "COR":
            timex = metarx[4]
        else:
            timex = metarx[3]
        del metarx[0]
        time = timex[2:4]
        if float(hourutc) == float(time):
            metarprint = " ".join(metarx)
#            print(metarprint) #print scraped lines on screen - put under comment if you won't use this
            met.write(metarprint.replace("=",'')) #write scraped lines to file - uncomment this to use (2/4)
#            print('\n')
            met.write('==\n') #(3/4)
            metarx.clear()
            d = len(linesnew)
            if float(c+1) == float(d-1):
                metarx.clear()
                break
            else:
                c += 1
                continue
        else:
            metarx.clear()
            continue
    except IndexError:
        metarx.clear()
        break

met.close() #closing file where lines are written - uncomment this to use (4/4)
       
os.remove("latest_metar.txt") #removing file where web page content is written

sys.exit (0)
