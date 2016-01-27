import numpy as np
import hashlib
import pandas as pd
from scipy import stats
from os.path import isfile

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

def drawCard(cards,challenges,monsters):
    cardTypes       = cards[["Monsters","Events"]].fillna('').as_matrix()
    distribution    = cards["Quantity"].as_matrix()
    distribution    = distribution*1./np.sum(distribution)
    #dist            = stats.rv_discrete(name="cardDist",values=(range(0,len(distribution)),distribution))
    while True:    
        ind     = weighted_values(range(0,len(distribution)),distribution,1)
        card = cards.iloc[ind]
        print card["Monsters"], card["Events"]
        stop=raw_input("")
#    print distribution    
#    print cardTypes
    

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

drawCard(cards,challenges,monsters)
p1  = Player()
   
#rolls     = getProb(7,2,6)
#print np.max(rolls[0]), np.min(rolls[0])
#print rolls[1]