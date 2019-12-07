
import sqlite3
import numpy as np 
import matplotlib.pyplot as plt 

conn = sqlite3.connect('League.sqlite')
cur = conn.cursor()

cur.execute('SELECT final_health FROM League_Final')

champion_health_list = []
for row in cur.fetchall():
    champion_health_list.append(row[0])

num_bins = 146

n, bins, patches = plt.hist(champion_health_list, num_bins, facecolor = 'red', alpha = 0.5)
plt.xlabel('final health')
plt.ylabel('count')
plt.title('Histogram of champion final health')
plt.show()

champion_damage_list = []
cur.execute('SELECT final_damage FROM League_Final')
for row in cur.fetchall():
    champion_damage_list.append(row[0])

num_bins = 146
n, bins, patches = plt.hist(champion_damage_list, num_bins, facecolor = 'red', alpha = 0.5)
plt.xlabel('final damage')
plt.ylabel('count')
plt.title('Histogram of champion final damage')
plt.show()


champion_defense_list = []
cur.execute('SELECT final_defense FROM League_Final')
for row in cur.fetchall():
    champion_defense_list.append(row[0])

num_bins = 146
n, bins, patches = plt.hist(champion_defense_list, num_bins, facecolor = 'red', alpha = 0.5)
plt.xlabel('final defense')
plt.ylabel('count')
plt.title('Histogram of champion final defense')
plt.show()