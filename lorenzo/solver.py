import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
import numpy as np

# Settings
path = './data/'
write = False


class Team:

    def __init__(self, team_id, pizzas):
        self.team_id = team_id
        self.pizzas = pizzas


class Pizza:

    def __init__(self, pizza_id, ingredients):
        self.pizza_id = pizza_id
        self.ingredients = ingredients

    def __str__(self):
        return str(self.pizza_id) + ' ' + str(len(self.ingredients))


def read(filepath):

    with open(filepath, 'r') as file:

        pizzas = []

        npizza, n2pt, n3pt, n4pt = [int(value) for value in file.readline().rstrip().split(' ')]

        for i in range(npizza):

            ingredients = file.readline().split()[1:]

            pizzas.append(Pizza(i, ingredients))

    return npizza, n2pt, n3pt, n4pt, pizzas


def solver(task):

    npizza, n2pt, n3pt, n4pt, pizzas = read(path + task + '.in')

    output = []
    j = 0

    # sort pizza
    pizzas.sort(key=lambda x: len(x.ingredients), reverse=True)

    # for nteams, nmembers in zip([n2pt, n3pt, n4pt], [2, 3, 4]):
    for nteams, nmembers in zip([n4pt, n3pt, n2pt], [4, 3, 2]):

        for _ in range(nteams):

            if len(pizzas) >= nmembers:

                team = Team(j, [])
                j += 1

                team.pizzas.append(pizzas.pop(0))

                for _ in range(nmembers - 1):

                    ingredients = set([ingredient for pizza in team.pizzas for ingredient in pizza.ingredients])

                    # pizza selection
                    candidates = pizzas[:min(200, len(pizzas))]
                    # candidates = pizzas
                    candidates.sort(key=lambda x: len(ingredients - set(x.ingredients)), reverse=True)

                    pizza = candidates[0]
                    pizzas.remove(pizza)

                    # delivery pizza
                    team.pizzas.append(pizza)

                output.append([pizza.pizza_id for pizza in team.pizzas])

    if write:

        with open('./output/' + task + '.txt', 'w') as file:

            file.write(str(len(output)) + '\n')

            for item in output:
                file.write(str(len(item)) + ' ')
                file.write(' '.join([str(value) for value in item]))
                file.write('\n')

    print(task, ' finished')


# Debug
if __name__ == '__main__':

    task = 'a_example'
    # task = 'b_little_bit_of_everything'

    npizza, n2pt, n3pt, n4pt, pizzas = read(path + task + '.in')

    output = []

    ingredients = [pizza.ingredients for pizza in pizzas]

    table = pd.Series(ingredients)

    mlb = MultiLabelBinarizer()

    encoding = pd.DataFrame(mlb.fit_transform(table), columns=mlb.classes_, index=table.index)


    def best_pizza(query, pizzas):

        query = np.array(encoding.iloc[query.pizza_id].to_list())
        pizzas.sort(key=lambda pizza: np.linalg.norm(query - np.array(encoding.iloc[pizza.pizza_id].to_list())),
                    reverse=True)
        return pizzas[0]

    pizza = pizzas.pop(1)
    best = best_pizza(pizza, pizzas)

    if write:

        with open('./output/' + task + '.txt', 'w') as file:

            file.write(str(len(output)) + '\n')

            for item in output:
                file.write(str(len(item)) + ' ')
                file.write(' '.join([str(value) for value in item]))
                file.write('\n')





















