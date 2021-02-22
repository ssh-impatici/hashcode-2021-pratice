from multiprocessing import Process

from solver import solver

if __name__ == '__main__':

    tasks = [
        'a_example',
        'b_read_on',
        'c_incunabula',
        'd_tough_choices',
        'e_so_many_books',
        'f_libraries_of_the_world',
    ]

    for task in tasks:
        process = Process(target=solver, args=([task]))
        process.start()
