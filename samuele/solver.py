import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from collections import Counter

# Settings
path = './data/'
write = True


class Team:

    def __init__(self, team_id, pizzas, unici):
        self.team_id = team_id
        self.pizzas = pizzas
        self.unici = unici


class Pizza:

    def __init__(self, pizza_id, ingredients):
        self.pizza_id = pizza_id
        self.ingredients = ingredients  # TODO Sortare
        self.score = 0  # TODO Score

    def __str__(self):
        return str(self.pizza_id) + ' ' + str(len(self.ingredients))


def read(filepath):
    with open(filepath, 'r') as file:
        pizzas = []
        count_ingredients = []

        npizza, n2pt, n3pt, n4pt = [int(value) for value in file.readline().rstrip().split(' ')]

        for i in range(npizza):
            ingredients = file.readline().split()[1:]

            for j in ingredients:
                count_ingredients.append(j)

            pizzas.append(Pizza(i, ingredients))

    return npizza, n2pt, n3pt, n4pt, pizzas, count_ingredients


def analysis(task):
    npizza, n2pt, n3pt, n4pt, pizzas, count_ingredients = read(path + task + '.in')

    # Score
    count_unici = {}

    unici = set(count_ingredients)

    for i in unici:
        count_unici.update({i: count_ingredients.count(i)})

    dist_ingredients = {}

    for i in range(1, len(unici) + 1):
        dist_ingredients[i] = 0

    for i in pizzas:
        s = 0
        dist_ingredients[len(i.ingredients)] += 1
        for j in i.ingredients:
            i.score += 1 / count_unici[j]  # Score

    # Datasets
    print(task)
    print("Numero ingredienti unici " + len(unici).__str__())

    plt.figure()
    x = np.arange(len(dist_ingredients))
    plt.bar(x, height=list(dist_ingredients.values()))
    # plt.xticks(x, list(dist_ingredients.keys()))
    plt.title("Distribuzione ingredienti")
    plt.xlabel("Numero ingredienti")
    plt.ylabel("Quante pizze hanno quel numero di ingredienti")
    plt.savefig("output/" + task + "_dist_ingredients")
    # plt.show()

    plt.figure()
    x = np.arange(3)
    plt.bar(x, height=[n2pt, n3pt, n4pt])
    plt.xticks(x, ['2', '3', '4'])
    plt.ylabel("Numero di teams")
    plt.title("Distribuzione teams")
    plt.savefig("output/" + task + "_dist_teams")
    # plt.show()

    p_tot = (n2pt * 2 + n3pt * 3 + n4pt * 4)

    print("Persone totali " + p_tot.__str__() + " - Pizze totali " + str(npizza) + " - " + (
            100 * npizza // p_tot).__str__() + " %")
    print("\n")


def normalize(df, pizzas):
    copy = df.copy()

    ingredients = [ingredient for pizza in pizzas for ingredient in pizza.ingredients]

    unqique_ingredients = list(set(ingredients))
    counts = Counter(ingredients)

    for ingredient in unqique_ingredients:
        copy[ingredient] = copy[ingredient].apply(lambda x: x/counts[ingredient])

    return copy, counts


def best_pizza(query, pizzas, normalized_encoding):
    pizzas.sort(
        key=lambda pizza: np.linalg.norm(query - np.array(normalized_encoding.iloc[pizza.pizza_id].to_list())),
        reverse=True)
    return pizzas[0]


def solver(task):
    start = time.time()

    npizza, n2pt, n3pt, n4pt, pizzas, count_ingredients = read(path + task + '.in')

    output = []

    ingredients = [pizza.ingredients for pizza in pizzas]

    table = pd.Series(ingredients)

    mlb = MultiLabelBinarizer()

    print("Inizio ENCODING")
    encoding = pd.DataFrame(mlb.fit_transform(table), columns=mlb.classes_, index=table.index)
    # print(encoding)
    print("Fine ENCODING")

    print("Inizio SORT")
    # Sort pizza
    pizzas.sort(key=lambda x: len(x.ingredients), reverse=True)  # TODO
    print("Fine SORT")

    print("Inizio NORMALIZE")
    normalized_encoding, counts = normalize(encoding, pizzas)
    # print(normalized_encoding)
    print("Fine NORMALIZE")

    j = 0

    # for nteams, nmembers in zip([n2pt, n3pt, n4pt], [2, 3, 4]):
    for nteams, nmembers in zip([n4pt, n3pt, n2pt], [4, 3, 2]):  # TODO

        for _ in range(nteams):

            if len(pizzas) >= nmembers:
                team = Team(j, [], [])
                j += 1

                pizza = pizzas.pop(0)  # TODO

                team.pizzas.append(pizza)
                team.unici.extend(pizza.ingredients)

                for _ in range(nmembers - 1):
                    # fake_pizza = Pizza(-1, team.unici)

                    riga = pd.DataFrame([[1 / counts[ingredients] if ingredients in team.unici else 0 for ingredients in
                                          encoding.columns]], columns=encoding.columns)
                    #print(riga)
                    query = np.array(riga.iloc[0].to_list())
                    #print(query)

                    best = best_pizza(query, pizzas[:min(40, len(pizzas))], normalized_encoding)  # Sliding window

                    team.pizzas.append(best)
                    team.unici.extend(best.ingredients)
                    team.unici = list(set(team.unici))

                    pizzas.remove(best)

                output.append([pizza.pizza_id for pizza in team.pizzas])

    if write:
        with open('./output/' + task + '.txt', 'w') as file:

            file.write(str(len(output)) + '\n')

            for item in output:
                file.write(str(len(item)) + ' ')
                file.write(' '.join([str(value) for value in item]))
                file.write('\n')

    print(task, ' finished in ' + (time.time() - start).__str__())


# Debug
if __name__ == '__main__':
    task = 'b_little_bit_of_everything'

    solver(task)
