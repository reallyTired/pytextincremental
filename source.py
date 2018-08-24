
#=============== SET UP ================#
import time
import random as rand
try: # load players saved data from file
    accessfile = open('save._rt','r')
    file = accessfile.readlines()
    pick = int(file[0])
    gold = int(file[1])
    silver = int(file[2])
    copper = int(file[3])
    money = int(file[4])
    pickcost = int(file[5])
    room = int(file[6])
    Aminers = int(file[7])
    Aminercost = int(file[8])
    tipjar = int(file[9])
    food = int(file[10])
    
    accessfile.close()
except: # create blank variables when save file isnt found
    print('No save file detected, generating new one...\n')
    pick = 1
    gold = 0
    silver = 0
    copper = 0
    money = 0
    pickcost = 25
    room = 1
    Aminers = 0
    Aminercost = 1000
    tipjar = 0
    food = 0

def ui(roomnum,where,interactables): # shows basic ui, sets up room and takes input
    global room
    room = roomnum
    print('\ngold   :   ' + str(gold))
    print('silver  :   ' + str(silver))
    print('copper  :   ' + str(copper))
    print('money   :   ' + str(money))
    print('pick lvl   :   ' + str(pick))
    if Aminers > 0:
        print('autominers   :   ' + str(Aminers))
    if food > 0:
        print('food   :   ' + str(food))
    print(where)
    print(interactables)
    user = input('What do you want to do? ').lower()
    print('======================================================\n')
    return user

def invalid(): # typing this is quicker then typing/copying the whole print statemnent, just a response to any invalid inputs
    print('not a valid action here')

#=============== USER COMMANDS ===============#

def save(): # saves players progress
    global pick
    global gold
    global silver
    global copper
    global pickcost
    global room
    global Aminers
    global Aminercost
    global tipjar
    global food
    statlist = [str(pick), str(gold), str(silver), str(copper), str(money), str(pickcost), str(room), str(Aminers), str(Aminercost), str(tipjar), str(food)]
    accessfile = open('save._rt','w')
    for i in statlist:
        accessfile.write(statlist[i] + '\n')
    accessfile.close()
    
def close():
    user = input('Are you sure you wish to save and quit? ').lower()
    if user == 'yes':
        save()
        exit()

def mine(multi): # player gathers ore
    global gold
    global silver
    global copper
    tempG = 0
    tempS = 0
    tempC = 0
    for i in range(0,pick*multi):
        ore = rand.randrange(0,3)
        if ore == 0:
            tempG += 1
        elif ore == 1:
            tempS += 1
        elif ore == 2:
            tempC += 1
    print('You gained: ' + str(tempG) + ' gold, ' + str(tempS) + ' silver and ' + str(tempC) + ' copper.')
    gold += tempG
    silver += tempS
    copper += tempC

def sell(): # sells all the players ore
    global gold
    global silver
    global copper
    global money
    # for gold
    if gold >= 100:
        money += gold * 6
        gold = 0
    else:
        money += gold * 3
        gold = 0
    # for silver
    if silver >= 100:
        money += silver * 4
        silver = 0
    else:
        money += silver * 2
        silver = 0
    # for copper
    if copper >= 100:
        money += copper * 2
        copper = 0
    else:
        money += copper
        copper = 0

def upgrade(): # upgrades players pickaxe to improve mining ability
    global pickcost
    global money
    global pick
    user = input('Pick upgrade costs ' + str(pickcost) + ' money. Are you sure you want to upgrade your pickaxe? ')
    if user == 'yes':
        if money >= pickcost:
            money -= pickcost
            pick += 1
            pickcost *= 2
        else:
            print('You cannot afford a stronger pick')

def autominer(): # allows player to buy or use the autominers depending on location
    global Aminers
    global money
    global Aminercost
    if room == 1:
        timeleft = 60
        for i in range(0,4):
            print(str(timeleft) + ' seconds remaining')
            timeleft -= 15
            time.sleep(15)
        mine(60*Aminers)
    if room == 2:
        user = input('Autominer costs ' + str(Aminercost) + ' money, are you sure you wish to purchase it? ').lower()
        if user == 'yes':
            if money >= Aminercost:
                Aminers += 1
                money -= Aminercost
                Aminercost *= 1.5
                Aminercost = int(Aminercost)
                print("Shop Keeper:\n'Thanks for your purchase!'")
            else:
                print('You cannot afford to buy the autominer')

def shopkeeper():
    randshoptext = ["'You work in the mine right? how\'s that going?'",
                    "'The tipjar is currently out of order, there is a hole at the bottom and money sort of vanishes once it falls in'",
                    "'I hear that shack is haunted'",
                    "'The inn is where you want to look if youre wanting a drink, some rumours or a good night... ill be here when you want to get back to work'",
                    "'Our autominers are top of the range! sit back, relax and watch that ore roll in!'"]
    print('Shop Keeper:\n' + rand.choice(randshoptext))

def tipjar():
    global money
    global tipjar
    print('The tipjar has an incomprehensably deep and dark whole at the bottom')
    user = input('How big of a \'tip\' do you put inside? ').lower()
    try:
        user = int(user)
        if  user <= money:
            money -= user
            tipjar += user
        else:
            print('You dont have that much money!')
    except:
        print('Canceled')

def buyfood():
    global money
    global food
    print('Food costs 150 per meal')
    user = input('How many meals do you want to buy? ').lower()
    if money >= 150 * user:
        
    

#=============== ROOMS ===============#

def InMines(): # Sets interactions available in the mines
    user = ui(1,'You\'re in a dingy mine','There is a merchent and rich veins of ore')
    if user == 'save':
        save()
    elif user == 'quit':
        close()
    elif user == 'mine':
        mine(1)
    elif user == 'sell':
        sell()
    elif user == 'upgrade':
        upgrade()
    elif user == 'talk' or user == 'merchent':
        print("Mining Merchant:\n'Sorry, i aint much for talking, got good prices on my picks though'")
    elif user == 'leave':
        InTown()
    elif user == 'autominer' and Aminers > 0:
        autominer()
    else:
        invalid()

def InTown(): # Sets interactions available in the town
    user = ui(2,'You\'re in the street of a small town','There is the mine enterance, a shop, an abandoned shack, a long norhern road and an inn')
    if user == 'save':
        save()
    elif user == 'quit':
        close()
    elif user == 'mine':
        InMines()
    elif user == 'shop':
        InShop()
    elif user == 'abandoned shack' or user == 'shack':
        InShack()
    elif user == 'inn':
        InInn()
    else:
        invalid()

def InShop(): # sets interactions available in the shop
    user = ui(3,'You\'re inside a small, cozy shop','There is a shop keeper, a pyramid display of big box\'s labelled autominer 6000, shelves stocked with food and a tipjar')
    if user == 'save':
        save()
    elif user == 'quit':
        close()
    elif user == 'shop keeper' or user == 'shopkeeper' or user == 'keeper':
        shopkeeper()
    elif user == 'autominer' or user == 'autominer 6000' or user == 'automine' or user == 'miner':
        autominer()
    elif user == 'tip' or user == 'tip jar' or user == 'tipjar' or user == 'jar':
        tipjar()
    elif user == 'food':
        buyfood()
    elif user == 'leave' or user == 'town' or user == 'street':
        InTown()
    else:
        invalid()

def InInn(): # sets interactions available in the inn
    user = ui(4,'You\'re inside a spacious, warm inn','There is a bartender at the bar,  and a nice atmosphere')
    if user == 'save':
        save()
    elif user == 'quit':
        close()
    elif user == 'bartender'
        bartender()
    else:
        invalid()

#=============== GAME LOOP ===============#

while True:
    if room == 1:
        InMines()
    elif room == 2:
        InTown()
    elif room == 3:
        InShop()
    elif room == 4:
        InInn()
    
