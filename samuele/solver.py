# Settings
path = './data/qualification_round_2020/'
write = True


def read(filepath):
    libraries = {}

    with open(filepath, 'r') as file:
        numbooks, numlibs, numdays = [int(value) for value in file.readline().split(' ')]

        scores = [int(score) for score in file.readline().split(' ')]

        for i in range(numlibs):
            nbooks, ndays, bxd = [int(value) for value in file.readline().split(' ')]
            books = [int(book) for book in file.readline().split(' ')]

            library = {i: {'numbooks': numbooks, 'numdays': ndays, 'bxd': bxd, 'books': books}}
            libraries.update(library)

        return numbooks, numlibs, numdays, scores, libraries


def solver(task):
    numbooks, numlibs, numdays, scores, libraries = read(path + task + '.txt')
    print(task, numbooks, numlibs, numdays)
    print(task, len(scores), type(scores), scores.count(5))
    print(task, len(libraries))

    if write:
        with open('./output/' + task + '.txt', 'w') as file:
            file.write('...')


# Debug
if __name__ == '__main__':
    task = 'a_example'

    numbooks, numlibs, numdays, scores, libraries = read(path + task + '.txt')
