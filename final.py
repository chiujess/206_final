from pokemon import *
from league import *
from heros import *

def userInput():
    # Instruction: You have 10 points in total. Please distribute them in the order of DAMAGE DEFENSE HEALTH.
    # Each number should be separated by one space.
    # Input example: 4 3 3
    # Take in user input
    #
    while True:
        print("Instructions: You have 10 points in total. Please distribute them to DAMAGE DEFENSE HEALTH.")
        damage_in = input("Enter damage point: ")
        defense_in = input("Enter defense point: ")
        health_in = input("Enter health point: ")
        try:
            damage_in + defense_in + health_in == 10
            break
        except:
            print("Please insert points that sum up to 10.")
            continue
    pokemon = getPokemon(damage_in, defense_in, health_in)
    league = getleague(damage_in, defense_in, health_in)
    hero = getHero(damage_in, defense_in, health_in)
    return pokemon, league, hero
    

def main():
    pokemon, league, hero = userInput()
    print("Your PERFECT squad is:", pokemon, league, hero)