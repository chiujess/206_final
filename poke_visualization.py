import requests
import json
import pandas as pd
import seaborn as sns
import operator
import random
import matplotlib.pyplot as plt

def dataToList(data):
    poke_list = []
    damage_list = []
    defense_list = []
    health_list = []
    poke_stats = {}
    for pokemon in data:
        if pokemon["pokemon_name"] not in poke_list:
            poke_list.append(pokemon["pokemon_name"])
            damage_list.append(pokemon["base_attack"])
            defense_list.append(pokemon["base_defense"])
            health_list.append(pokemon["base_stamina"])
    return damage_list, defense_list, health_list

def getJsonAsList():
    url = "https://pokemon-go1.p.rapidapi.com/pokemon_stats.json"

    headers = {
        'x-rapidapi-host': "pokemon-go1.p.rapidapi.com",
        'x-rapidapi-key': "f795a5645emsh67e333a942de32bp146411jsn51057dbf6e68"
    }

    response = requests.request("GET", url, headers=headers)
    data = json.loads(response.text)
    return data

def drawHist(data_name, data_list):
    plt.hist(data_list, color='green', bins=150)
    plt.title("Histogram of pokemon " + data_name)
    plt.xlabel(data_name)
    plt.ylabel("count")
    plt.show()

def main():
    poke_data = getJsonAsList()
    damage_list, defense_list, health_list = dataToList(poke_data)
    drawHist("final damage", damage_list)
    drawHist("final defense", defense_list)
    drawHist("final health", health_list)

if if __name__ == "__main__":
    main()
