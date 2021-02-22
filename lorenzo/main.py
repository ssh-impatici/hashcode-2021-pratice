from multiprocessing import Process

from solver import solver

if __name__ == '__main__':

    tasks = [
        'a_example',
        'b_little_bit_of_everything',
        'c_many_ingredients',
        'd_many_pizzas',
        'e_many_teams'
    ]

    for task in tasks:
        process = Process(target=solver, args=([task]))
        process.start()