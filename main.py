import multiprocessing

def factorize_worker(number, result_queue):
    factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            factors.append(i)
    result_queue.put(factors)

def factorize_parallel(numbers):
    result_queue = multiprocessing.Queue()
    processes = []

    for num in numbers:
        process = multiprocessing.Process(target=factorize_worker, args=(num, result_queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    results = [result_queue.get() for _ in range(len(numbers))]
    return results

def main():
    numbers = [128, 255, 99999, 10651060]

    # Synchronous version
    for num in numbers:
        result = factorize_worker(num)
        print(f"Factors of {num} (Sync): {result}")

    # Parallel version
    results_parallel = factorize_parallel(numbers)
    for i, result in enumerate(results_parallel):
        print(f"Factors of {numbers[i]} (Parallel): {result}")

if __name__ == "__main__":
    main()