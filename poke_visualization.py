import seaborn as sns

def drawBoxPlot(data):
    boxplot = sns.boxplot(x=data)
    boxplot.set_facecolor("red")
    sns.plt.show()

def getJsonAsList():
    url = "https://pokemon-go1.p.rapidapi.com/pokemon_stats.json"

    headers = {
        'x-rapidapi-host': "pokemon-go1.p.rapidapi.com",
        'x-rapidapi-key': "f795a5645emsh67e333a942de32bp146411jsn51057dbf6e68"
    }

    response = requests.request("GET", url, headers=headers)
    data = json.loads(response.text)
    return data

def main():
    poke_data = getJsonAsList()
    poke_df = pd.DataFrame(poke_data, columns=["name", "damage", "defense", "health"])
    poke_stats_df = poke_df.drop("name", axis=1)
    drawBoxPlot(poke_df["damage"])
    drawBoxPlot(poke_df["defense"])
    drawBoxPlot(poke_df["health"])