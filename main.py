import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as pl
import pickle
from scipy.stats import poisson
import json

#Lire un dataset en format CSV
def read_dataset(file):
    return pd.read_csv(file)

def read_json(file):
    fileObject = open(file, "r")
    jsonContent = fileObject.read()
    obj_python = json.loads(jsonContent)
    return obj_python

#retourne la liste des équipes du groupe
def teams_of_pool(group):
    res = read_json("my_json/pools.json")
    return res



#Prédire le score entre deux équipes en utilisant la loi de Poisson
def predicts_stats(home, away):
    if home in df_team_stats.index and away in df_team_stats.index:
        #lambda = goals_scored * goals_conceded
        lamb_home = df_team_stats.at[home,'GoalsScored'] * df_team_stats.at[away,'GoalsConceded']
        lamb_away = df_team_stats.at[away,'GoalsScored'] * df_team_stats.at[home,'GoalsConceded']
        prob_home, prob_away, prob_draw = 0, 0, 0

        for x in range(0,11):
            for y in range(0, 11):
                p = poisson.pmf(x, lamb_home) * poisson.pmf(y,lamb_away)
                if x == y:
                    prob_draw += p
                elif x > y:
                    prob_home += p
                else:
                    prob_away += p

            score_home = 3 * prob_home + prob_draw
            score_away = 3 * prob_away + prob_draw
            return (score_home, score_away)
        else:
            return (0,0)

#Main
if __name__ == "__main__":
    matches_from_1930 = read_dataset('csv/filtered_international_matches.csv')
    world_cup_matches = read_dataset('csv/clean_fifa_worldcup.csv')
    pools = read_json("my_json/pools.json")

    #dict_table = pickle.load(open('csv/dict_table','rb'))

    #séparer le jeu de données en équipe home et away
    df_home = matches_from_1930[['home_team', 'home_team_score', 'away_team_score']]
    df_away = matches_from_1930[['away_team', 'home_team_score', 'away_team_score']]

    #Renommer les colonnes pour mieux trier et effectuer des moyennes
    df_home = df_home.rename(columns={'home_team': 'Team', 'home_team_score': 'GoalsScored', 'away_team_score': 'GoalsConceded'})
    df_away = df_away.rename(columns={'away_team': 'Team', 'home_team_score': 'GoalsConceded', 'away_team_score': 'GoalsScored'})

    #Regrouper par équipe en faisant de moyenne des buts mis et encaissés depuis 1930
    df_team_stats = pd.concat([df_home, df_away], ignore_index=True).groupby('Team').mean()

    #Commencer à utiliser la loi de Poisson pour prédire le score d'un match
    #print(df_team_stats)

    #Récupérer que les 48 premiers match

    #print(teams_of_pool('A'))
    print(pools['A']['Qatar'])
    for index, row in world_cup_matches.iterrows():
        home, away, group = row['home'], row['away'], row['pool']

        points_home, points_away = predicts_stats(home,away)
        if points_home > points_away:
            winner = home
        else:
            winner = away

        pools[group][home] += points_home
        pools[group][away] += points_away

        print(home, " VS ", away, "(",winner,")")

    print(pools)
