import numpy as np
import hashlib
import pandas as pd
from scipy import stats
from os.path import isfile
import os

def getProb(x,ndice,dtype):
    numbers     = np.ceil(np.random.rand(10000,ndice)*dtype)
    sums        = np.sum(numbers,axis=1)
    perc        = np.sum(np.where(sums>=x,1,0))*1./10000
    print sums[:10]
    print np.where(sums[:10]>=x,1,0)
    return sums, perc

def weighted_values(values, probabilities, size):
    bins = np.add.accumulate(probabilities)
    whatever    = np.digitize(np.random.random_sample(size), bins)
    if len(whatever)>1:
        return values[np.digitize(np.random.random_sample(size), bins)]
    else:
        return values[whatever[0]]

def buildEncounter(encounter,item,types):
    if item != "nan":
        #print types
        types   = types[types["Level"]==int(float(item))]
        dist    = types["Quantity"].as_matrix()
        dist    = dist*1./np.sum(dist)
        card    = types.iloc[weighted_values(range(0,len(dist)),dist,1)]
        #print card
        encounter.append(card)

def resolveCard(card,challenges,monsters,treasures):
    encounter   = []
    reward      = []
    monsterList = str(card["Monsters"]).split(',')
    eventList   = str(card["Events"]).split(',')
    treasureList= str(card["Treasure"]).split(',')
    XP          = card["XP"]
    for monster in monsterList:
        buildEncounter(encounter,monster,monsters)
        numMonsters     = len(encounter)
    for event in eventList:
        buildEncounter(encounter,event,challenges)
        numEvents   = len(encounter) - numMonsters
    for treasure in treasureList:
        buildEncounter(encounter,treasure,treasures)
        numRewards  = len(encounter) - numMonsters - numEvents
    printEncounter(encounter,numMonsters,numEvents,numRewards,XP)
    
def printEncounter(encounter,nM,nE,nR,XP):
    #print encounter, nM, nE, nR
    os.system('clear')
    print "*"*80
    print "New Card"
    print "*"*80
    if nM > 0:
        print "Combat!"
        prettyPrintMonsters(encounter[:nM])
    if nE > 0:
        print "Encounter!"
        prettyPrintEvents(encounter[nM:nE])
    stop=raw_input("\nDid you succeed?")
    os.system('clear')
    if nR > 0:
        print "Rewards!"
        prettyPrintRewards(encounter[-nR:])
    print "XP: ", XP

    
    
def prettyPrintMonsters(monsters):
    for monster in monsters:
        print "*"*25
        print monster["Name"]
        print "*"*25
        print "Attack: ", monster["Attack"]
        print "Defense: ", monster["Defense"]
        print "Speed: ", monster["Speed"]
        print "Damage: ", monster["Damage"]
        print "Health: ", monster["Health"]
        print "Ability: ", monster["Special"]
        print ""
    
def prettyPrintEvents(events):
    for event in events:
        print event["Description"]
    
def prettyPrintRewards(rewards):
    for reward in rewards:
        print "*"*20
        print reward["Name"]
        print reward["Type"]
        print reward["Ability"]
        print "*"*20
def drawCard(cards,challenges,monsters,treasures):
    #cardTypes       = cards[["Monsters","Events"]].fillna('').as_matrix()
    distribution    = cards["Quantity"].as_matrix()
    distribution    = distribution*1./np.sum(distribution)
    #dist            = stats.rv_discrete(name="cardDist",values=(range(0,len(distribution)),distribution))
    while True:    
        ind     = weighted_values(range(0,len(distribution)),distribution,1)
        card = cards.iloc[ind]
        resolveCard(card,challenges,monsters,treasures)
        stop=raw_input("")

    

class Player():
    
    def __init__(self,att=0,defense=7,dam=2,hp=10,aPoints=2,speed=5):
        self.attack     = att
        self.defense    = defense
        self.damage     = dam
        self.health     = hp
        self.APs        = aPoints
        self.speed      = speed

        self.enemies    = [] 
        self.ID         = hashlib.md5(str(np.random.rand())).hexdigest()[:10]
        print "new Player with ID: ", self.ID        

class Monster():
    
    def __init__(self,att=0,defense=2,dam=2,hp=1,speed=3):
        self.attack     = att
        self.defense    = defense
        self.damage     = dam
        self.health     = hp
        self.speed      = speed

        self.enemies    = [] 
        self.ID         = hashlib.md5(str(np.random.rand())).hexdigest()[:10]        
 
 
monsters    = pd.read_csv("monsters.csv",encoding='utf-8') 
cards       = pd.read_csv("cards.csv",encoding='utf-8')
challenges  = pd.read_csv("challenges.csv",encoding='utf-8')
treasures   = pd.read_csv("treasures.csv",encoding='utf-8')

drawCard(cards,challenges,monsters,treasures)
p1  = Player()
   
#rolls     = getProb(7,2,6)
#print np.max(rolls[0]), np.min(rolls[0])
#print rolls[1]