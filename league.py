import cassiopeia as cass
import sqlite3
import random

cass.set_riot_api_key('RGAPI-ab902989-a52d-4c35-8a7d-7b4233a166e3')
cass.set_default_region('NA')
champions = cass.get_champions()

conn = sqlite3.connect('League.sqlite')
cur = conn.cursor()

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
def get_damage_tier(champion):
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

def get_health_tier(champion):
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

def get_defense_tier(champion):
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
    final_champ_dictionary[champion.name]['damage'] = get_damage_tier(champion)
    final_champ_dictionary[champion.name]['defense'] = get_defense_tier(champion)
    final_champ_dictionary[champion.name]['health'] = get_health_tier(champion)
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
        dis = (damage-a)**2+(defense-d)**2+(health-h)**2
        champ_dis_list.append((champ, dis))
    sort_champ_dis_list = sorted(champ_dis_list, key=lambda x: x[1])
    choice_list = []
    min_dis = sort_champ_dis_list[0][1]
    for champ in sort_champ_dis_list:
        if champ[1] == min_dis:
            choice_list.append(champ[0])
    final_champion = random.choice(choice_list)
    return final_champion

print(getleague(3,3,4))
print(getleague(3,3,4))
    

