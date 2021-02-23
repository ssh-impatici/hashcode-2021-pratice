from multiprocessing import Process

from solver import solver, analysis

if __name__ == '__main__':

    tasks = [
        'a_example',
        'b_little_bit_of_everything',
        'c_many_ingredients',
        'd_many_pizzas',
        'e_many_teams'
    ]

    anal = False
    sol = True

    # Analysis
    if anal:
        for task in tasks:
            process = Process(target=analysis, args=([task]))
            process.start()

    # Solver
    if sol:
        for task in tasks:
            process = Process(target=solver, args=([task]))
            process.start()
