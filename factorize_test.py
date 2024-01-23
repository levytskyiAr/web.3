import timeit

def factorize(numbers):
    result = []
    for num in numbers:
        factors = []
        for i in range(1, num + 1):
            if num % i == 0:
                factors.append(i)
        result.append(factors)
    return result

# Початкові дані
input_numbers = [128, 255, 99999, 10651060]

# Виміряйте час виконання функції
elapsed_time = timeit.timeit(lambda: factorize(input_numbers), number=1)

# Виведіть результат та час виконання
output_factors = factorize(input_numbers)
for i in range(len(input_numbers)):
    print(f"Factors of {input_numbers[i]}: {output_factors[i]}")

print(f"Elapsed time: {elapsed_time:.20f} seconds")

'''
фУНКЦІЯ БЕЗ multiprocessing
'''