import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer

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
        self.encoding = []

    def __str__(self):
        return str(self.pizza_id) + ' ' + str(len(self.ingredients))


def read(filepath):
    with open(filepath, 'r') as file:
        pizzas = []
        counts = {}

        npizza, n2pt, n3pt, n4pt = [int(value) for value in file.readline().rstrip().split(' ')]

        for i in range(npizza):
            ingredients = file.readline().split()[1:]

            for j in ingredients:
                count = counts.get(j, 0)
                counts.update({j: count + 1})

            pizzas.append(Pizza(i, ingredients))

    return npizza, n2pt, n3pt, n4pt, pizzas, counts


def analysis(task):
    npizza, n2pt, n3pt, n4pt, pizzas, counts = read(path + task + '.in')

    print(task)
    print("Numero ingredienti unici " + str(len(counts)))

    dist_ingredients = {}

    for i in range(1, len(counts) + 1):
        dist_ingredients[i] = 0

    for i in pizzas:
        s = 0
        dist_ingredients[len(i.ingredients)] += 1

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


def normalize_pizza(pizza, counts, ingredients):
    if not len(pizza.encoding) > 0:
        pizza.encoding = [1 / (counts[ingredient] ** 2) if ingredient in pizza.ingredients else 0 for ingredient in
                          ingredients]

    return pizza


def best_pizza(team_encoding, pizzas, counts, ingredients):
    pizzas.sort(
        key=lambda pizza: np.linalg.norm(
            team_encoding - np.array(normalize_pizza(pizza, counts, ingredients).encoding)),
        reverse=True)
    return pizzas[0]


def solver(task):
    start = time.time()

    npizza, n2pt, n3pt, n4pt, pizzas, counts = read(path + task + '.in')

    output = []

    ingredients = [pizza.ingredients for pizza in pizzas]

    table = pd.Series(ingredients)

    mlb = MultiLabelBinarizer()

    encoding = pd.DataFrame(mlb.fit_transform(table), columns=mlb.classes_, index=table.index)
    # print(encoding)

    pizzas.sort(key=lambda x: len(x.ingredients), reverse=True)  # Sort iniziale

    j = 0
    n = n4pt + n3pt + n2pt

    for nteams, nmembers in zip([n4pt, n3pt, n2pt], [4, 3, 2]):  # Priorità
        # for nteams, nmembers in zip([n3pt, n4pt, n2pt], [3, 4, 2]):  # Priorità
        # for nteams, nmembers in zip([n2pt, n3pt, n4pt], [2, 3, 4]):  # Priorità
        for _ in range(nteams):

            if len(pizzas) >= nmembers:
                team = Team(j, [], [])
                j += 1
                print(str(round((j / n * 100), 2)) + "%")  # Percentuale teams completati

                pizza = pizzas.pop(0)  # TODO

                pizza = normalize_pizza(pizza, counts, encoding.columns)

                team.pizzas.append(pizza)
                team.unici.extend(pizza.ingredients)

                for _ in range(nmembers - 1):
                    team_encoding = [1 / counts[ingredient] if ingredient in team.unici else 0 for ingredient in
                                     encoding.columns]

                    best = best_pizza(team_encoding, pizzas[:min(100, len(pizzas))], counts,
                                      encoding.columns)  # Sliding window

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
    print(task, ' pizze rimanenti ' + str(len(pizzas)))
    print(task, ' team compleati ' + str(round((j / n * 100), 2)) + "%")


# Debug
if __name__ == '__main__':
    task = 'b_little_bit_of_everything'

    solver(task)
