from multiprocessing import Pool
import time

def square(n):
    return n * n

if __name__ == "__main__":
    start_pool = time.perf_counter()        #Start timer
    #Create a pool with 4 worker processes
    with Pool(4) as pool:
        #Apply square() to every number in the list
        results = pool.map(square, range(1, 11))

    end_pool = time.perf_counter()       #Stop timer

    print("Results using Pool:")
    print(results)

    print("Pool Time:", end_pool - start_pool, "seconds")

    #Using Normal For Loop
    start_loop = time.perf_counter()

    normal_results = []

    for i in range(1, 11):
        normal_results.append(square(i))

    end_loop = time.perf_counter()

    print("\nResults using For Loop:")
    print(normal_results)

    print("For Loop Time:", end_loop - start_loop, "seconds")


