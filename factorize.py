from multiprocessing import Pool
import timeit


def factorize(num):
    factors = []
    for i in range(1, num + 1):
        if num % i == 0:
            factors.append(i)
    return factors


def process_input_number(input_number):
    factors = factorize(input_number)
    print(f"Factors of {input_number}: {factors}")


if __name__ == '__main__':
    input_numbers = [128, 255, 99999, 10651060]

    # Вимірюємо час для одного виклику factorize
    elapsed_time = timeit.timeit(lambda: factorize(input_numbers[0]), number=1)

    # Використовуємо Pool для обробки чисел паралельно
    with Pool() as pool:
        pool.map(process_input_number, input_numbers)

    print(f"Elapsed time: {elapsed_time:.20f} seconds")

'''
фУНКЦІЯ З multiprocessing
'''