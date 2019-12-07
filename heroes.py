import requests
import json
import os
import sqlite3
import operator
import random

heroes = []
num_heroes = 500

for i in range(1, num_heroes+1):
    url = ('https://superheroapi.com/api/2550354465178834/{}/powerstats'.format(i))
    response = requests.get(url)
    data = response.text
    hero = json.loads(data)
    heroes.append(hero)

name = []
combat = []
power = []
intelligence = []
strength = []
defense = []
attack = []
hp = []

path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path+'/'+'heroes.db')
cur = conn.cursor()

for h in heroes:
    if h['combat'] != "null" and h['power'] != "null" and h['strength'] != "null" \
        and h['durability'] != "null" and h['intelligence'] != "null":
        name.append(h['name'])
        combat.append(h['combat'])
        power.append(h['power'])
        intelligence.append(h['intelligence'])
        strength.append(h['strength'])
        hp.append(h['durability'])
        attack.append((int(h['combat']) + int(h['power']))/2)
        defense.append((int(h['intelligence']) + int(h['strength']))/2)


cur.execute("DROP TABLE IF EXISTS Hero_Damage")
cur.execute("CREATE TABLE Hero_Damage (name TEXT PRIMARY KEY, combat INTEGER, power INTEGER, attack FLOAT)")
for i in range(len(name)):
        cur.execute("INSERT OR REPLACE INTO Hero_Damage (name, combat, power, attack) \
            VALUES (?,?,?,?)",(name[i], combat[i], power[i], attack[i]))

cur.execute("DROP TABLE IF EXISTS Defense")
cur.execute("DROP TABLE IF EXISTS Hero_Defense")
cur.execute("CREATE TABLE Hero_Defense (name TEXT PRIMARY KEY, intelligence INTEGER, strength INTEGER, defense FLOAT)")
for i in range(len(name)):
        cur.execute("INSERT OR REPLACE INTO Hero_Defense (name, intelligence, strength, defense) \
            VALUES (?,?,?,?)",(name[i], intelligence[i], strength[i], defense[i]))

cur.execute("DROP TABLE IF EXISTS Hero_Health")
cur.execute("CREATE TABLE Hero_Health (name TEXT PRIMARY KEY, hp INTEGER)")
for i in range(len(name)):
        cur.execute("INSERT OR REPLACE INTO Hero_Health (name, hp) \
            VALUES (?,?)",(name[i], hp[i]))

cur.execute("DROP TABLE IF EXISTS Hero_Final")
cur.execute("CREATE TABLE Hero_Final(name TEXT PRIMARY KEY, hp INTEGER, defense FLOAT, attack FLOAT)")

cur.execute("SELECT Hero_Damage.name, Hero_Damage.attack, Hero_Defense.defense, Hero_Health.hp FROM Hero_Damage \
    INNER JOIN Hero_Defense ON Hero_Damage.name = Hero_Defense.name INNER JOIN Hero_Health \
        ON Hero_Defense.name = Hero_Health.name")

for r in cur.fetchall():
    n = r[0]
    a = r[1]
    d = r[2]
    h = r[3]
    cur.execute("INSERT OR REPLACE INTO Hero_Final (name, attack, defense, hp) \
        VALUES (?,?,?,?)", (n, a, d, h))

conn.commit()

def get_damage_mean():
    cur.execute("SELECT attack FROM Hero_Final")
    total = 0
    count = 0
    for r in cur.fetchall():
        total += r[0]
        count += 1

    return total/count

def get_defense_mean():
    cur.execute("SELECT defense FROM Hero_Final")
    total = 0
    count = 0
    for r in cur.fetchall():
        total += r[0]
        count += 1

    return total/count

def get_health_mean():
    cur.execute("SELECT hp FROM Hero_Final")
    total = 0
    count = 0
    for r in cur.fetchall():
        total += r[0]
        count += 1

    return total/count

def get_damage_sd():
    mean = get_damage_mean()
    cur.execute("SELECT attack FROM Hero_Final")
    total = 0
    count = 0
    for r in cur.fetchall():
        total += (r[0]-mean)**2
        count += 1
    sd = (total/(count-1))**(0.5)
    return sd

def get_defense_sd():
    mean = get_defense_mean()
    cur.execute("SELECT defense FROM Hero_Final")
    total = 0
    count = 0
    for r in cur.fetchall():
        total += (r[0]-mean)**2
        count += 1
    sd = (total/(count-1))**(0.5)
    return sd

def get_health_sd():
    mean = get_health_mean()
    cur.execute("SELECT hp FROM Hero_Final")
    total = 0
    count = 0
    for r in cur.fetchall():
        total += (r[0]-mean)**2
        count += 1
    
    sd = (total/(count-1))**(0.5)
    return sd

def get_damage_tier(hero_name):
    mean = get_damage_mean()
    sd = get_damage_sd()
    cur.execute("SELECT attack FROM Hero_Final WHERE name = ?", (hero_name, ))
    for r in cur.fetchall():
        if r[0] <= mean - sd*2:
            return 1
        elif r[0] <= mean - sd:
            return 2
        elif r[0] <= mean:
            return 3
        elif r[0] <= mean + sd:
            return 4
        else:
            return 5

def get_defense_tier(hero_name):
    mean = get_defense_mean()
    sd = get_defense_sd()
    cur.execute("SELECT defense FROM Hero_Final WHERE name = ?", (hero_name, ))
    for r in cur.fetchall():
        if r[0] <= mean - sd*2:
            return 1
        elif r[0] <= mean - sd:
            return 2
        elif r[0] <= mean:
            return 3
        elif r[0] <= mean + sd:
            return 4
        else:
            return 5

def get_health_tier(hero_name):
    mean = get_health_mean()
    sd = get_health_sd()
    cur.execute("SELECT hp FROM Hero_Final WHERE name = ?", (hero_name, ))
    for r in cur.fetchall():
        if r[0] <= mean - sd*2:
            return 1
        elif r[0] <= mean - sd:
            return 2
        elif r[0] <= mean:
            return 3
        elif r[0] <= mean + sd:
            return 4
        else:
            return 5


def tier_dict():
    tier = {}
    
    for i in range(len(name)):
        tier[name[i]] = {}
        tier[name[i]]['damage'] = get_damage_tier(name[i])
        tier[name[i]]['defense'] = get_defense_tier(name[i])
        tier[name[i]]['health'] = get_health_tier(name[i])
        
    return tier

def getHero(damage, defense, health, tier_dict):
    dist_dict = {}
    for n in tier_dict.keys():
        a = (damage - tier_dict[n]['damage'])**2
        d = (defense - tier_dict[n]['defense'])**2
        h = (health - tier_dict[n]['health'])**2
        dist = a + d + h
        dist_dict[n] = dist
    dist_sort = sorted(dist_dict.items(), key = operator.itemgetter(1))
    dist_same = []
    first = dist_sort[0][1]
    for h in dist_sort:
        if h[1] == first:
            dist_same.append(h[0])
    return random.choice(dist_same)
    
print(getHero(4, 3, 3, tier_dict()))
f = open("hero_tier.txt", "w")
f.write(str(tier_dict()))
f.close()