
import sqlite3
import numpy as np 
import matplotlib.pyplot as plt 

conn = sqlite3.connect('heroes.db')
cur = conn.cursor()

cur.execute('SELECT attack FROM Hero_Final')

damage = []
for row in cur.fetchall():
    damage.append(row[0])

num_bins = 50

n, bins, patches = plt.hist(damage, num_bins, facecolor = 'blue', alpha = 0.5)
plt.xlabel('final damage')
plt.ylabel('count')
plt.title('Histogram of heroes final damage')
plt.show()

defense = []
cur.execute('SELECT defense FROM Hero_Final')
for row in cur.fetchall():
    defense.append(row[0])

n, bins, patches = plt.hist(defense, num_bins, facecolor = 'blue', alpha = 0.5)
plt.xlabel('final defense')
plt.ylabel('count')
plt.title('Histogram of heroes final defense')
plt.show()


health = []
cur.execute('SELECT hp FROM Hero_Final')
for row in cur.fetchall():
    health.append(row[0])

n, bins, patches = plt.hist(health, num_bins, facecolor = 'blue', alpha = 0.5)
plt.xlabel('final health')
plt.ylabel('count')
plt.title('Histogram of heroes final health')
plt.show()