import cassiopeia as cass
import sqlite3
import random
import requests
import json
import os
import operator
import pandas as pd
import seaborn as sns

conn = sqlite3.connect("squad.db")
cur = conn.cursor()

def setUpDatabase():
    conn = sqlite3.connect("squad.db")
    cur = conn.cursor()
    return cur, conn

def getJsonAsList():
    url = "https://pokemon-go1.p.rapidapi.com/pokemon_stats.json"

    headers = {
        'x-rapidapi-host': "pokemon-go1.p.rapidapi.com",
        'x-rapidapi-key': "f795a5645emsh67e333a942de32bp146411jsn51057dbf6e68"
    }

    response = requests.request("GET", url, headers=headers)
    data = json.loads(response.text)
    return data

def setUpPokeStatsTable(cur, conn, data):
    poke_list = []

    cur.execute("DROP TABLE IF EXISTS Poke_Damage")
    cur.execute("DROP TABLE IF EXISTS Poke_Defense")
    cur.execute("DROP TABLE IF EXISTS Poke_Health")
    cur.execute("DROP TABLE IF EXISTS Poke_Final")
    cur.execute("CREATE TABLE Poke_Damage (name TEXT PRIMARY KEY, damage INTEGER)")
    cur.execute("CREATE TABLE Poke_Defense (name TEXT PRIMARY KEY, defense INTEGER)")
    cur.execute("CREATE TABLE Poke_Health (name TEXT PRIMARY KEY, health INTEGER)")
    cur.execute("CREATE TABLE Poke_Final (name TEXT PRIMARY KEY, final_damage INTEGER, final_defense INTEGER, final_health INTEGER)")
    for pokemon in data:
        if pokemon["pokemon_name"] not in poke_list:
            poke_list.append(pokemon["pokemon_name"])
            cur.execute("INSERT INTO Poke_Damage (name, damage) VALUES (?, ?)",(pokemon["pokemon_name"], pokemon["base_attack"]))
            cur.execute("INSERT INTO Poke_Defense (name, defense) VALUES (?, ?)",(pokemon["pokemon_name"], pokemon["base_defense"]))
            cur.execute("INSERT INTO Poke_Health (name, health) VALUES (?, ?)",(pokemon["pokemon_name"], pokemon["base_stamina"]))
    cur.execute("SELECT Poke_Health.name, Poke_Damage.damage, Poke_Health.health, Poke_Defense.defense FROM Poke_Health INNER JOIN Poke_Damage ON Poke_Health.name=Poke_Damage.name INNER JOIN Poke_Defense ON Poke_Health.name=Poke_Defense.name")
    for row in cur.fetchall():
        name = row[0]
        damage = row[1]
        health = row[2]
        defense = row[3]
        cur.execute("INSERT INTO Poke_Final (name, final_damage, final_health, final_defense) VALUES (?,?,?,?)", (name, damage, health, defense))
    conn.commit()

def createDataFrame():
    poke_list = []
    cur.execute("SELECT Poke_Final.name, Poke_Final.final_damage, Poke_Final.final_defense, Poke_Final.final_health")
    for row in cur.fetchall():
        stats = []
        stats.append(row[0])
        stats.append(row[1])
        stats.append(row[2])
        stats.append(row[3])
        poke_list.append(stats)
    poke_df = pd.DataFrame(poke_list, columns=["name", "damage", "defense", "health"])
    return poke_df

def drawBoxPlot(data):
    boxplot = sns.boxplot(x=data)
    sns.plt.show()

def removeOutliers(df):
    Q1 = df.quantile(0.25)
    Q3 = df.quantile(0.75)
    IQR = Q3 - Q1
    df_out = df[~((df < (Q1 - 1.5 * IQR)) |(df > (Q3 + 1.5 * IQR))).any(axis=1)]
    return df_out

def calcSd(cur, conn):
    damage_total = 0
    defense_total = 0
    health_total = 0
    count = 0
    
    # Calculate mean
    cur.execute("SELECT final_damage, final_defense, final_health FROM Poke_Final")
    for row in cur.fetchall():
        damage_total += row[0]
        defense_total += row[1]
        health_total += row[2]
        count += 1
    damage_mean = damage_total/count
    defense_mean = defense_total/count
    health_mean = health_total/count

    # Reset total for calculating standard deviation
    damage_total = 0
    defense_total = 0
    health_total = 0
    # Calculate sd
    cur.execute("SELECT final_damage, final_defense, final_health FROM Poke_Final")
    for row in cur.fetchall():
        damage_total += (row[0] - damage_mean)**2
        defense_total += (row[1] - defense_mean)**2
        health_total += (row[2] - health_mean)**2
    damage_sd = (damage_total/count)**(1.0/2.0)
    defense_sd = (defense_total/count)**(1.0/2.0)
    health_sd = (health_total/count)**(1.0/2.0)

    return (damage_mean, damage_sd), (defense_mean, defense_sd), (health_mean, health_sd)

def assignTier(cur, conn, damage_stats, defense_stats, health_stats):
    cur.execute("DROP TABLE IF EXISTS Poke_Tier")
    cur.execute("CREATE TABLE Poke_Tier (name TEXT PRIMARY KEY, damage INTEGER, defense INTEGER, health INTEGER)")
    cur.execute("SELECT name, final_damage, final_defense, final_health FROM Poke_Final")
    tier_dict = {}

    for row in cur.fetchall():
        name = row[0]
        damage = row[1]
        defense = row[2]
        health = row[3]

        damage_tier = 0
        defense_tier = 0
        health_tier = 0

        if damage >= damage_stats[0] + 2 * damage_stats[1]:
            damage_tier = 5
        elif damage >= damage_stats[0] + damage_stats[1]:
            damage_tier = 4
        elif damage >= damage_stats[0]:
            damage_tier = 3
        elif damage >= damage_stats[0] - damage_stats[1]:
            damage_tier = 2
        else:
            damage_tier = 1

        if defense >= defense_stats[0] + 2 * defense_stats[1]:
            defense_tier = 5
        elif defense >= defense_stats[0] + defense_stats[1]:
            defense_tier = 4
        elif defense >= defense_stats[0]:
            defense_tier = 3
        elif defense >= defense_stats[0] - defense_stats[1]:
            defense_tier = 2
        else:
            defense_tier = 1

        if health >= health_stats[0] + 2 * health_stats[1]:
            health_tier = 5
        elif health >= health_stats[0] + health_stats[1]:
            health_tier = 4
        elif health >= health_stats[0]:
            health_tier = 3
        elif health >= health_stats[0] - health_stats[1]:
            health_tier = 2
        else:
            health_tier = 1
        tier_dict[name] = {"damage": damage_tier, "defense": defense_tier, "health": health_tier}
        cur.execute("INSERT INTO Poke_Tier (name, damage, health, defense) VALUES (?,?,?,?)", (name, damage_tier, health_tier, defense_tier))
    conn.commit()
    f = open("poke_tier.txt", "w")
    f.write(str(tier_dict))
    f.close()
    return tier_dict

def getPokemon(damage, defense, health, tier_dict):
    # Get each pokemon from dictionary - [name, damage, defense, health]
    # Create a dictionary that contains the distance between each pokemon and user input - dict = {pokemon_name: distance}
    # Sort the dictionary by distance
    # Find all pokemon with the same least distance output as list
    # import random, pick a random one from the list and return
    distance_dict = {}
    for name in tier_dict.keys():
        dis = (tier_dict[name]["damage"] - damage)**2 + (tier_dict[name]["defense"] - defense)**2 + (tier_dict[name]["health"] - health)**2
        distance_dict[name] = dis
    distance_sorted = sorted(distance_dict.items(), key=operator.itemgetter(1))
    randomized_list = []
    cur_dis = distance_sorted[0][1]
    for i in range(len(distance_sorted)):
        if(distance_sorted[i][1] == cur_dis):
            randomized_list.append(distance_sorted[i])
        else:
            break
    pokemon = random.choice(randomized_list)
    return pokemon[0]

heroes = []
num_heroes = 300

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
# conn = sqlite3.connect(path+'/'+'heroes.db')
# cur = conn.cursor()

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

cass.set_riot_api_key('RGAPI-ab902989-a52d-4c35-8a7d-7b4233a166e3')
cass.set_default_region('NA')
champions = cass.get_champions()

# conn = sqlite3.connect('League.sqlite')
# cur = conn.cursor()

# damage table
cur.execute('DROP TABLE IF EXISTS League_Damage')
cur.execute('CREATE TABLE League_Damage(name TEXT, base_damage FLOAT, damage_per_level FLOAT, final_damage FLOAT)')

for champion in champions[:20]:
    final_damage = champion.stats.attack_damage+17*champion.stats.attack_damage_per_level
    cur.execute('INSERT INTO League_Damage(name, base_damage, damage_per_level, final_damage) VALUES (?, ?, ?, ?)', (champion.name, champion.stats.attack_damage, champion.stats.attack_damage_per_level, final_damage))


conn.commit()

for champion in champions[20:40]:
    final_damage = champion.stats.attack_damage+17*champion.stats.attack_damage_per_level
    cur.execute('INSERT INTO League_Damage(name, base_damage, damage_per_level, final_damage) VALUES (?, ?, ?, ?)', (champion.name, champion.stats.attack_damage, champion.stats.attack_damage_per_level, final_damage))

conn.commit()

for champion in champions[40:60]:
    final_damage = champion.stats.attack_damage+17*champion.stats.attack_damage_per_level
    cur.execute('INSERT INTO League_Damage(name, base_damage, damage_per_level, final_damage) VALUES (?, ?, ?, ?)', (champion.name, champion.stats.attack_damage, champion.stats.attack_damage_per_level, final_damage))
conn.commit()

for champion in champions[60:80]:
    final_damage = champion.stats.attack_damage+17*champion.stats.attack_damage_per_level
    cur.execute('INSERT INTO League_Damage(name, base_damage, damage_per_level, final_damage) VALUES (?, ?, ?, ?)', (champion.name, champion.stats.attack_damage, champion.stats.attack_damage_per_level, final_damage))

conn.commit()

for champion in champions[80:100]:
    final_damage = champion.stats.attack_damage+17*champion.stats.attack_damage_per_level
    cur.execute('INSERT INTO League_Damage(name, base_damage, damage_per_level, final_damage) VALUES (?, ?, ?, ?)', (champion.name, champion.stats.attack_damage, champion.stats.attack_damage_per_level, final_damage))

conn.commit()

for champion in champions[100:120]:
    final_damage = champion.stats.attack_damage+17*champion.stats.attack_damage_per_level
    cur.execute('INSERT INTO League_Damage(name, base_damage, damage_per_level, final_damage) VALUES (?, ?, ?, ?)', (champion.name, champion.stats.attack_damage, champion.stats.attack_damage_per_level, final_damage))

conn.commit()

for champion in champions[120:140]:
    final_damage = champion.stats.attack_damage+17*champion.stats.attack_damage_per_level
    cur.execute('INSERT INTO League_Damage(name, base_damage, damage_per_level, final_damage) VALUES (?, ?, ?, ?)', (champion.name, champion.stats.attack_damage, champion.stats.attack_damage_per_level, final_damage))
conn.commit()

for champion in champions[140:]:
    final_damage = champion.stats.attack_damage+17*champion.stats.attack_damage_per_level
    cur.execute('INSERT INTO League_Damage(name, base_damage, damage_per_level, final_damage) VALUES (?, ?, ?, ?)', (champion.name, champion.stats.attack_damage, champion.stats.attack_damage_per_level, final_damage))
conn.commit()



# health table
cur.execute('DROP TABLE IF EXISTS League_Health')
cur.execute('CREATE TABLE League_Health(name_ TEXT, base_health FLOAT, health_per_level FLOAT, final_health FLOAT)')

for champion in champions[:20]:
    final_health = champion.stats.health+17*champion.stats.health_per_level
    cur.execute('INSERT INTO League_Health(name_, base_health, health_per_level, final_health) VALUES (?, ?, ?, ?)', (champion.name, champion.stats.health, champion.stats.health_per_level, final_health))


conn.commit()

for champion in champions[20:40]:
    final_health = champion.stats.health+17*champion.stats.health_per_level
    cur.execute('INSERT INTO League_Health(name_, base_health, health_per_level, final_health) VALUES (?, ?, ?, ?)', (champion.name, champion.stats.health, champion.stats.health_per_level, final_health))


conn.commit()

for champion in champions[40:60]:
    final_health = champion.stats.health+17*champion.stats.health_per_level
    cur.execute('INSERT INTO League_Health(name_, base_health, health_per_level, final_health) VALUES (?, ?, ?, ?)', (champion.name, champion.stats.health, champion.stats.health_per_level, final_health))

conn.commit()

for champion in champions[60:80]:
    final_health = champion.stats.health+17*champion.stats.health_per_level
    cur.execute('INSERT INTO League_Health(name_, base_health, health_per_level, final_health) VALUES (?, ?, ?, ?)', (champion.name, champion.stats.health, champion.stats.health_per_level, final_health))

conn.commit()

for champion in champions[80:100]:
    final_health = champion.stats.health+17*champion.stats.health_per_level
    cur.execute('INSERT INTO League_Health(name_, base_health, health_per_level, final_health) VALUES (?, ?, ?, ?)', (champion.name, champion.stats.health, champion.stats.health_per_level, final_health))

conn.commit()

for champion in champions[100:120]:
    final_health = champion.stats.health+17*champion.stats.health_per_level
    cur.execute('INSERT INTO League_Health(name_, base_health, health_per_level, final_health) VALUES (?, ?, ?, ?)', (champion.name, champion.stats.health, champion.stats.health_per_level, final_health))

conn.commit()

for champion in champions[120:140]:
    final_health = champion.stats.health+17*champion.stats.health_per_level
    cur.execute('INSERT INTO League_Health(name_, base_health, health_per_level, final_health) VALUES (?, ?, ?, ?)', (champion.name, champion.stats.health, champion.stats.health_per_level, final_health))

conn.commit()

for champion in champions[140:]:
    final_health = champion.stats.health+17*champion.stats.health_per_level
    cur.execute('INSERT INTO League_Health(name_, base_health, health_per_level, final_health) VALUES (?, ?, ?, ?)', (champion.name, champion.stats.health, champion.stats.health_per_level, final_health))

conn.commit()


# defense table
cur.execute('DROP TABLE IF EXISTS League_Defense')
cur.execute('CREATE TABLE League_Defense(name__ TEXT, base_armor FLOAT, armor_per_level FLOAT, final_armor FLOAT)')

for champion in champions[:20]:
    final_armor = champion.stats.armor+17*champion.stats.armor_per_level
    cur.execute('INSERT INTO League_Defense(name__, base_armor, armor_per_level, final_armor) VALUES (?, ?, ?, ?)', (champion.name, champion.stats.armor, champion.stats.armor_per_level, final_armor))


conn.commit()

for champion in champions[20:40]:
    final_armor = champion.stats.armor+17*champion.stats.armor_per_level
    cur.execute('INSERT INTO League_Defense(name__, base_armor, armor_per_level, final_armor) VALUES (?, ?, ?, ?)', (champion.name, champion.stats.armor, champion.stats.armor_per_level, final_armor))

conn.commit()

for champion in champions[40:60]:
    final_armor = champion.stats.armor+17*champion.stats.armor_per_level
    cur.execute('INSERT INTO League_Defense(name__, base_armor, armor_per_level, final_armor) VALUES (?, ?, ?, ?)', (champion.name, champion.stats.armor, champion.stats.armor_per_level, final_armor))
conn.commit()

for champion in champions[60:80]:
    final_armor = champion.stats.armor+17*champion.stats.armor_per_level
    cur.execute('INSERT INTO League_Defense(name__, base_armor, armor_per_level, final_armor) VALUES (?, ?, ?, ?)', (champion.name, champion.stats.armor, champion.stats.armor_per_level, final_armor))

conn.commit()

for champion in champions[80:100]:
    final_armor = champion.stats.armor+17*champion.stats.armor_per_level
    cur.execute('INSERT INTO League_Defense(name__, base_armor, armor_per_level, final_armor) VALUES (?, ?, ?, ?)', (champion.name, champion.stats.armor, champion.stats.armor_per_level, final_armor))

conn.commit()

for champion in champions[100:120]:
    final_armor = champion.stats.armor+17*champion.stats.armor_per_level
    cur.execute('INSERT INTO League_Defense(name__, base_armor, armor_per_level, final_armor) VALUES (?, ?, ?, ?)', (champion.name, champion.stats.armor, champion.stats.armor_per_level, final_armor))
conn.commit()

for champion in champions[120:140]:
    final_armor = champion.stats.armor+17*champion.stats.armor_per_level
    cur.execute('INSERT INTO League_Defense(name__, base_armor, armor_per_level, final_armor) VALUES (?, ?, ?, ?)', (champion.name, champion.stats.armor, champion.stats.armor_per_level, final_armor))
conn.commit()

for champion in champions[140:]:
    final_armor = champion.stats.armor+17*champion.stats.armor_per_level
    cur.execute('INSERT INTO League_Defense(name__, base_armor, armor_per_level, final_armor) VALUES (?, ?, ?, ?)', (champion.name, champion.stats.armor, champion.stats.armor_per_level, final_armor))
conn.commit()
# final data table

cur.execute('DROP TABLE IF EXISTS League_Final')
cur.execute('CREATE TABLE League_Final(champ TEXT, final_damage FLOAT, final_health FLOAT, final_defense FLOAT)')

cur.execute('SELECT h.name_, d.final_damage, h.final_health, a.final_armor FROM League_Health h INNER JOIN League_Damage d ON name_=name INNER JOIN League_Defense a ON name_=name__')
for row in cur.fetchall():
     champ = row[0]
     damage = row[1]
     health = row[2]
     defense = row[3]
     cur.execute('INSERT INTO League_Final (champ, final_damage, final_health, final_defense) VALUES (?,?,?,?)', (champ, damage, health, defense))

conn.commit()

# calculations
def get_mean_damage():
    cur.execute('SELECT final_damage from League_Final')
    total = 0
    count = 0
    for row in cur.fetchall():
        total+=row[0]
        count+=1
    mean = total/count
    return mean

def get_sd_damage():
    mean = get_mean_damage()
    cur.execute('SELECT final_damage from League_Final')
    total = 0
    count = -1
    for row in cur.fetchall():
        total+=(row[0]-mean)**2
        count+=1
    sd = (total/count)**(1.0/2.0)
    return sd

# print(get_mean_damage())
# print(get_sd_damage())

def get_mean_health():
    cur.execute('SELECT final_health from League_Final')
    total = 0
    count = 0
    for row in cur.fetchall():
        total+=row[0]
        count+=1
    mean = total/count
    return mean

def get_sd_health():
    mean = get_mean_health()
    cur.execute('SELECT final_health from League_Final')
    total = 0
    count = -1
    for row in cur.fetchall():
        total+=(row[0]-mean)**2
        count+=1
    sd = (total/count)**(1.0/2.0)
    return sd

# print(get_mean_health())
# print(get_sd_health())

def get_mean_defense():
    cur.execute('SELECT final_defense from League_Final')
    total = 0
    count = 0
    for row in cur.fetchall():
        total+=row[0]
        count+=1
    mean = total/count
    return mean

def get_sd_defense():
    mean = get_mean_defense()
    cur.execute('SELECT final_defense from League_Final')
    total = 0
    count = -1
    for row in cur.fetchall():
        total+=(row[0]-mean)**2
        count+=1
    sd = (total/count)**(1.0/2.0)
    return sd

# tier functions
def get_damage_tier_1(champion):
    mean = get_mean_damage()
    sd = get_sd_damage()
    cur.execute('SELECT final_damage FROM League_Final WHERE champ = ?', (champion.name, ))
    for row in cur.fetchall():
        final_damage = row[0] 
    if final_damage >= mean+2*sd:
        tier = 5
    elif final_damage >= mean+sd:
        tier = 4
    elif final_damage >= mean:
        tier = 3
    elif final_damage >= mean-sd:
        tier = 2
    else:
        tier = 1
    return tier

# damage_tier_list = []
# for champion in champions:
#     damage_tier_list.append({champion.name: get_damage_tier(champion)})

#print(damage_tier_list)

def get_health_tier_1(champion):
    mean = get_mean_health()
    sd = get_sd_health()
    cur.execute('SELECT final_health FROM League_Final WHERE champ = ?', (champion.name, ))
    for row in cur.fetchall():
        final_health = row[0] 
    if final_health >= mean+2*sd:
        tier = 5
    elif final_health >= mean+sd:
        tier = 4
    elif final_health >= mean:
        tier = 3
    elif final_health >= mean-sd:
        tier = 2
    else:
        tier = 1
    return tier

# health_tier_list = []
# for champion in champions:
#     health_tier_list.append({champion.name: get_health_tier(champion)})

#print(health_tier_list)

def get_defense_tier_1(champion):
    mean = get_mean_defense()
    sd = get_sd_defense()
    cur.execute('SELECT final_defense FROM League_Final WHERE champ = ?', (champion.name, ))
    for row in cur.fetchall():
        final_defense = row[0] 
    if final_defense >= mean+2*sd:
        tier = 5
    elif final_defense >= mean+sd:
        tier = 4
    elif final_defense >= mean:
        tier = 3
    elif final_defense >= mean-sd:
        tier = 2
    else:
        tier = 1
    return tier

# defense_tier_list = []
# for champion in champions:
#     defense_tier_list.append({champion.name: get_defense_tier(champion)})

#print(defense_tier_list)

final_champ_dictionary = {}
for champion in champions:
    final_champ_dictionary[champion.name] = {}
    final_champ_dictionary[champion.name]['damage'] = get_damage_tier_1(champion)
    final_champ_dictionary[champion.name]['defense'] = get_defense_tier_1(champion)
    final_champ_dictionary[champion.name]['health'] = get_health_tier_1(champion)
print(final_champ_dictionary)

f = open('final_champ_dictionary.txt', 'w')
f.write(str(final_champ_dictionary))
f.close()

def getleague(damage, defense, health):
    champ_dis_list = []
    for champ in final_champ_dictionary:
        a = final_champ_dictionary[champ]['damage']
        d = final_champ_dictionary[champ]['defense']
        h = final_champ_dictionary[champ]['health']
        dis = (damage-a)**2+(defense-a)**2+(health-h)**2
        champ_dis_list.append((champ, dis))
    sort_champ_dis_list = sorted(champ_dis_list, key=lambda x: x[1])
    choice_list = []
    min_dis = sort_champ_dis_list[0][1]
    for champ in sort_champ_dis_list:
        if champ[1] == min_dis:
            choice_list.append(champ[0])
    final_champion = random.choice(choice_list)
    return final_champion

def userInput(poke_tier_dict):
    # Instruction: You have 10 points in total. Please distribute them in the order of DAMAGE DEFENSE HEALTH.
    # Each number should be separated by one space.
    # Input example: 4 3 3
    # Take in user input
    #
    while True:
        print("Instructions: You have 10 points in total. Please distribute them to DAMAGE DEFENSE HEALTH.")
        damage_in = int(input("Enter damage point: "))
        defense_in = int(input("Enter defense point: "))
        health_in = int(input("Enter health point: "))
        try:
            damage_in + defense_in + health_in == 10
        except:
            print("Please insert points that sum up to 10.")
            continue
    pokemon = getPokemon(damage_in, defense_in, health_in, poke_tier_dict)
    league = getleague(damage_in, defense_in, health_in)
    hero = getHero(damage_in, defense_in, health_in, tier_dict())
    print("Your PERFECT squad is: {}, {}, {}".format(pokemon, league, hero))
    

def main():
    cur, conn = setUpDatabase()
    data = getJsonAsList()
    setUpPokeStatsTable(cur, conn, data)
    poke_df = pd.DataFrame(data, columns=["name", "damage", "defense", "health"])

    # Dataframe without names
    poke_stats_df = poke_df.drop("name", axis=1)

    # Remove outliers using IQR
    new_poke_stats_df = removeOutliers(poke_stats_df)

    # Calculate standard deviation
    damage_stats, defense_stats, health_stats = calcSd(cur, conn)
    print(damage_stats, defense_stats, health_stats)

    # Calculate tiers
    tier_dict = assignTier(cur, conn, damage_stats, defense_stats, health_stats)
    
    cur.execute("SELECT health from Poke_Tier")
    tier_count = {1:0, 2:0, 3:0, 4:0, 5:0}
    for row in cur.fetchall():
        tier_count[row[0]] += 1
    print(tier_count)
    pokemon, league, hero = userInput(tier_dict)
    print("Your PERFECT squad is: {}, {}, {}".format(pokemon, league, hero))

if __name__ == "__main__":
    main()