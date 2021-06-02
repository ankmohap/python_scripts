import requests
import parse
import re
import json
from pprint import pprint
import csv

invalid_escape = re.compile(r'\\[0-7]{1,3}')  # up to 3 digits for byte values up to FF

def replace_with_byte(match):
    return chr(int(match.group(0)[1:], 8))

def repair(brokenjson):
    return invalid_escape.sub(replace_with_byte, brokenjson)

def extract(s):
    start = s.find('(')
    if start == -1:
        # No opening bracket found. Should this be an error?
        return ''
    start += 1  # skip the bracket, move to the next character
    end = s.find(')', start)
    if end == -1:
        # No closing bracket found after the opening bracket.
        # Should this be an error instead?
        return s[start:]
    else:
        return s[start:end]

url="http://www.espncricinfo.com/series/8048/game/1136567/sunrisers-hyderabad-vs-mumbai-indians-7th-match-indian-premier-league-2018/"
#url="http://www.espncricinfo.com/series/791129/scorecard/829823/Mumbai-Indians-vs-Chennai-Super-Kings-Final-Pepsi-Indian-Premier-League"
req = requests.get(url)
respData = req.content
paragraphs = re.findall(r"__INITIAL_STATE__ = (.*?)};",str(respData))
str1 = ''.join(str(e) for e in paragraphs)
str1 = str1 + "}"
str2 = re.sub(r'(?<!\\)\\', r'', str1)
data = json.loads(str2)

score =(data["gamePackage"]["scorecard"])

i=0

player= []
runouts =['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0']
points= ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0']
team = ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0']
runs = ['-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1','-1']
fours = ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0']
sixes = ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0']
catches = ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0']
stumps = ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0']
maidens = ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0']
wickets = ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0']
runout = ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0']
cplayer = []
splayer = []
runplayer=[]

for element in score["innings"]["1"]["batsmen"]:
    player.append(element["name"])

for element in score["innings"]["2"]["batsmen"]:
    player.append(element["name"])

for element in score["innings"]["1"]["didNotBat"]:
    player.append(element["name"])

for element in score["innings"]["2"]["didNotBat"]:
    player.append(element["name"])


#print(x["name"])

for element in score["innings"]["1"]["bowlers"]:
    x=(element["name"])
    for sub in element["stats"]:
        if sub["name"]== "maidens":
            y= sub["value"]
        if sub["name"]== "wickets":
            z= sub["value"]
    for i in range(len(player)):
        if player[i] == x:
            maidens[i]=y
            wickets[i]=z


for element in score["innings"]["1"]["batsmen"]:
    i=0
    x=(element["name"])
    for sub in element["stats"]:
        if sub["name"]== "runs":
           y= sub["value"]
        if sub["name"]== "fours":
            z= sub["value"]
        if sub["name"]== "sixes":
            r= sub["value"]
    for i in range(len(player)):
        if player[i] == x:
            runs[i]=y
            fours[i]=z
            sixes[i]=r


for element in score["innings"]["2"]["bowlers"]:
    i=0
    x=(element["name"])
    for sub in element["stats"]:
        if sub["name"]== "maidens":
            y = sub["value"]
        if sub["name"]== "wickets":
            z = sub["value"]
    for i in range(len(player)):
        if player[i] == x:
            maidens[i]=y
            wickets[i]=z



for element in score["innings"]["2"]["batsmen"]:
    i=0
    x=(element["name"])
    for sub in element["stats"]:
        if sub["name"]== "runs":
            y = sub["value"]
        if sub["name"]== "fours":
            z = sub["value"]
        if sub["name"]== "sixes":
            r = sub["value"]
    for i in range(len(player)):
        if player[i] == x:
            runs[i]=y
            fours[i]=z
            sixes[i]=r


for element in score["innings"]["1"]["batsmen"]:
    if element["isNotOut"] is False:
        rows = element["shortText"]
        sp_rows = rows.split(" ")
        for i in range(len(sp_rows)):
            if sp_rows[i] == "c":
                l = sp_rows[i+1]
                cplayer.append(l)


for element in score["innings"]["2"]["batsmen"]:
    if element["isNotOut"] is False:
        rows = element["shortText"]
        sp_rows = rows.split(" ")
        for i in range(len(sp_rows)):
            if sp_rows[i] == "c":
               l = sp_rows[i+1]
               cplayer.append(l)

for element in score["innings"]["1"]["batsmen"]:
    if element["isNotOut"] is False:
        rows = element["shortText"]
        sp_rows = rows.split(" ")
        for i in range(len(sp_rows)):
            if sp_rows[i] == "st":
                br = sp_rows[i+1].split(";")
                splayer.append(br)

for element in score["innings"]["2"]["batsmen"]:
    if element["isNotOut"] is False:
        rows = element["shortText"]
        sp_rows = rows.split(" ")
        for i in range(len(sp_rows)):
            if sp_rows[i] == "st":
                br = sp_rows[i+1].split(";")
                splayer.append(br[1])


for element in score["innings"]["1"]["batsmen"]:
    if element["isNotOut"] is False:
        rows = element["shortText"]
        if (extract(rows)):
            runplayer.append(extract(rows))

for element in score["innings"]["2"]["batsmen"]:
    if element["isNotOut"] is False:
        rows = element["shortText"]
        if (extract(rows)):
            runplayer.append(extract(rows))           

                        

for i in range(len(player)):
    catch=0
    for x in range(len(cplayer)):
        if cplayer[x] in player[i]:
            catch=catch+1
    catches[i]=catch


for i in range(len(player)):
    stum=0
    for x in range(len(splayer)):
        if splayer[x] in player[i]:
            stum=stum+1
    stumps[i]=stum

for i in range(len(player)):
    rout=0
    for x in range(len(runplayer)):
        if runplayer[x] in player[i]:
            rout=rout+1
    runout[i]=rout 

                
for i in range(len(player)):
    print ("player : " + player[i] +" team :"+ team[i] +" Runs : "+ runs[i] +" fours :" + fours[i] +
    " sixes : "+ sixes[i] + " catches : " + str(catches[i]) + " stumps : " + str(stumps[i]) + " maidens :" + maidens[i] + " wickets :" + wickets[i])
                                     
for i in range(len(player)):
    if int(runs[i]) >= 100:
        points[i]=int(runs[i]) + 100
    if int(runs[i]) >= 75:
        points[i]=int(runs[i]) + 50
    if int(runs[i]) >= 50:
        points[i]=int(runs[i]) + 25
    if int(runs[i]) == 0:
        points[i]= int(points[i])- 20
    if int(runs[i]) == -1:
        points[i]= 0
    else:
        points[i]=int(runs[i])
    if int(wickets[i]) >= 5:
        points[i]=points[i]+int(wickets[i])*20 + 50
    if int(wickets[i]) >= 3:
        points[i]=points[i]+int(wickets[i])*20 + 25
    else:
        points[i]=points[i]+int(wickets[i])*20
        
    points[i]=points[i]+(int(catches[i])*5)+(int(stumps[i])*10)+(int(runout[i]))
#    points[i]=points[i]+(int(catches[i])*5)+(int(stumps[i])*10)+(int(maidens[i])*5)+(int(sixes[i])*10)+(int(runout[i]*10))

with open('names.csv', 'w') as csvfile:
    fieldnames = ['players', 'points']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for i in range(len(player)):
         writer.writerow({'players': player[i], 'points': str(points[i])})
