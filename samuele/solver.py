import matplotlib.pyplot as plt

# Settings
import numpy as np

path = './data/'
write = True


def read(filepath):
    with open(filepath, 'r') as file:
        pizzas = {}
        count_ingredients = []

        npizza, n2pt, n3pt, n4pt = [int(value) for value in file.readline().rstrip().split(' ')]

        for i in range(npizza):
            ingredients = file.readline().split()[1:]

            for j in ingredients:
                count_ingredients.append(j)

            pizzas.update({i: {'ingredients': ingredients}})

    return npizza, n2pt, n3pt, n4pt, pizzas, count_ingredients


def solver(task):
    npizza, n2pt, n3pt, n4pt, pizzas, count_ingredients = read(path + task + '.in')

    # Score
    count = {}
    unici = set(count_ingredients)

    for i in unici:
        count.update({i: count_ingredients.count(i)})

    for i in range(0, npizza):
        s = 0
        for j in pizzas[i]['ingredients']:
            s += 1 / count[j]  # Score

        pizzas[i]['score'] = s

    # Analisi dei dataset
    print(task)
    print("Numero ingredienti unici " + len(unici).__str__())

    dist_ingredients = {}

    for i in range(1, len(unici) + 1):
        dist_ingredients[i] = 0

    for i in range(0, npizza):
        dist_ingredients[len(pizzas[i]['ingredients'])] += 1

    plt.figure()
    x = np.arange(len(dist_ingredients))
    plt.bar(x, height=list(dist_ingredients.values()))
    plt.xticks(x, list(dist_ingredients.keys()))
    plt.title("Distribuzione ingredienti")
    plt.xlabel("Numero ingredienti")
    plt.ylabel("Quante pizze hanno quel numero di ingredienti")
    plt.savefig("output/" + task + "_dist_ingredients")
    # plt.show()

    team_dist = [0, 0, n2pt, n3pt, n4pt]

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

    if write:
        with open('./output/' + task + '.txt', 'w') as file:
            file.write('...')


# Debug
if __name__ == '__main__':
    task = 'a_example'
