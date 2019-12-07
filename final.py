import requests
import json
import sqlite3
import pandas as pd
import seaborn as sns

def setUpDatabase():
    conn = sqlite3.connect("pokemon.db")
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
    return tier_dict  

def main():
    cur, conn = setUpDatabase()
    data = getJsonAsList()
    setUpPokeStatsTable(cur, conn, data)
    poke_df = pd.DataFrame(data, columns=["name", "damage", "defense", "health"])

    # Dataframe without names
    poke_stats_df = poke_df.drop("name", axis=1)

    # Draw boxplots for each stats
    # drawBoxPlot(poke_df["damage"])
    # drawBoxPlot(poke_df["defense"])
    # drawBoxPlot(poke_df["health"])

    # Remove outliers using IQR
    new_poke_stats_df = removeOutliers(poke_stats_df)

    # Calculate standard deviation
    damage_stats, defense_stats, health_stats = calcSd(cur, conn)
    print(damage_stats, defense_stats, health_stats)

    # Calculate tiers
    tier_dict = assignTier(cur, conn, damage_stats, defense_stats, health_stats)
    
    # cur.execute("SELECT health from Poke_Tier")
    # tier_count = {1:0, 2:0, 3:0, 4:0, 5:0}
    # for row in cur.fetchall():
    #     tier_count[row[0]] += 1
    # print(tier_count)


    

if __name__ == "__main__":
    main()