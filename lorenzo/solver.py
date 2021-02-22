# Settings
path = './data/'
write = True


def read(filepath):

    with open(filepath, 'r') as file:

        pizzas = {}

        npizza, n2pt, n3pt, n4pt = [int(value) for value in file.readline().rstrip().split(' ')]

        for i in range(npizza):

            ingredients = file.readline().split()[1:]

            pizzas.update({i: {'ingredients': ingredients}})

    return npizza, n2pt, n3pt, n4pt, pizzas


def solver(task):

    if write:
        with open('./output/' + task + '.txt', 'w') as file:
            file.write('...')


# Debug
if __name__ == '__main__':

    task = 'a_example'

    npizza, n2pt, n3pt, n4pt, pizzas = read(path + task + '.in')

    # if write:
    #    with open('./output/' + task + '.txt', 'w') as file:





