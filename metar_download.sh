#!/bin/bash

#all file locatons need to be set for your case

python3 /home/$(whoami)/scripts/metar_download.py #run scrapper bot
wait #wait till all operations are done and then continue

folim=$(date -u +"%Y%m") #folder name for year and month
folim2=$(date -u +"%m%d") #folder name for month and day

#check if all folder exist - if do not, create them
[[ ! -d /home/$(whoami)/saved_metar/$folim ]] && mkdir /home/$(whoami)/saved_metar/$folim
[[ ! -d /home/$(whoami)/saved_metar/$folim/$folim2 ]] && mkdir /home/$(whoami)/saved_metar/$folim/$folim2

FILE=/home/$(whoami)/scripts/metar.txt #file which will be copied 

if (("$(date -u +"%M")" <= "30")); then #file name after copying
  dattim=$(date -u +"%Y%m%d%H"00)
elif (("$(date -u +"%M")" > "30")); then
  dattim=$(date -u +"%Y%m%d%H"30)
fi

if test -f "$FILE"; then #check if file which needs to be copied exist
  cp $FILE /home/$(whoami)/saved_metar/$folim/$folim2/metar_hr_$dattim.txt
  rm $FILE
else
  exit
fi
