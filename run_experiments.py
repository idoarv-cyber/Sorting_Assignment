import time
import random
import matplotlib.pyplot as plt
import numpy as np
import argparse


# --- PART A: Sorting Algorithms Implementation ---

def bubble_sort(arr):                   # Bubble Sort - O(n^2)
    n = len(arr)
    for i in range(n):                      # Outer loop - each iteration scans the whole array
        for j in range(0, n - i - 1):       # Inner loop - j is index is the scan
            if arr[j] > arr[j + 1]:         # if current element is bigger than the next:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]  # it should be switched
    return arr


def selection_sort(arr):                # Selection Sort - O(n^2)
    n = len(arr)
    for i in range(n):                          # Outer loop - goes over the array elements
        min_idx = i                             # marking current round element for compare
        for j in range(i + 1, n):               # inner loop
            if arr[j] < arr[min_idx]:           # if we found a new minimum:
                min_idx = j                        # set the new minimum
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
                            # after finishing the round - switch between curr element and new min
    return arr


def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def partition(arr, low, high):                # assisting func of QuickSort
    pivot = arr[high]                           # Choose "random" element as pivot (the last one)
    lower_bound = low - 1                       # bound index for those who smaller than pivot

    for j in range(low, high):
        if arr[j] <= pivot:                    # j element smaller than pivot
            lower_bound += 1                       # goes one after the last lower
            arr[lower_bound], arr[j] = arr[j], arr[lower_bound]  # switch places: lower goes to next
                                                                                 # place in lower section
    arr[high], arr[lower_bound+1] = arr[lower_bound+1] , arr[high]          # move pivot to its place
    return lower_bound+1                                                    # return pivot's index


def quick_sort(arr, low=0, high=None):          # Quick Sort O(nlogn)
    if high is None:                               # first setting of high
        high = len(arr) - 1

    if low < high:                                 # there are still elements between low and high
        pivot_index = partition(arr, low, high)        # do first iteration of sort, and get pivot index

        quick_sort(arr, low, pivot_index - 1)           # send first part [low,pivot) to QuickSort
        quick_sort(arr, pivot_index + 1, high)          # send last part (pivot, high] to QuickSort
    return arr



# --- PART D: Command Line Interface (CLI) ---

def main():
    parser = argparse.ArgumentParser(description="Sorting Benchmarks")
    parser.add_argument("-a", "--algorithms", nargs='+', type=int, required=True,
                        help="IDs: 2=Selection, 3=Insertion, 5=QuickSort")
    parser.add_argument("-s", "--sizes", nargs='+', type=int, required=True,
                        help="Array sizes e.g. 100 500 1000")
    parser.add_argument("-r", "--repetitions", type=int, default=5,
                        help="Number of repetitions for mean/std")
    parser.add_argument("-e", "--experiment", type=int, choices=[1, 2],
                        help="1=Nearly sorted 5% noise, 2=Nearly sorted 20% noise. (Omit for Random)")

    args = parser.parse_args()

    # Menu
    algo_map = {2: (selection_sort, "Selection Sort"),
                3: (insertion_sort, "Insertion Sort"),
                5: (quick_sort, "Quick Sort")}

    plt.figure(figsize=(10, 6))

    # Loop through each selected algorithm
    for algo_id in args.algorithms:
        if algo_id not in algo_map:
            continue

        algo_func, algo_name = algo_map[algo_id]
        avg_times = []
        std_times = []

        # For each size, we run the experiment 'r' times
        for size in args.sizes:
            run_times = []
            for _ in range(args.repetitions):
                # Generate array based on experiment type
                if args.experiment is None:
                    # PART B: Random Array
                    data = [random.randint(0, 10000) for _ in range(size)]
                else:
                    # PART C: Nearly Sorted (5% or 20% noise)
                    data = list(range(size))
                    noise_level = 0.05 if args.experiment == 1 else 0.20
                    num_swaps = int(size * noise_level)
                    for _ in range(num_swaps):
                        idx1, idx2 = random.sample(range(size), 2)
                        data[idx1], data[idx2] = data[idx2], data[idx1]

                # Timing and Sorting
                start = time.time()
                algo_func(data)
                run_times.append(time.time() - start)

            # Record stats for this specific size
            avg_times.append(np.mean(run_times))
            std_times.append(np.std(run_times))

        # --- PART 3: Visualization with Shaded Area ---
        avg_np = np.array(avg_times)
        std_np = np.array(std_times)

        line, = plt.plot(args.sizes, avg_np, marker='o', label=algo_name, linewidth=2)

        # Shade the error area (ensuring it stays above 0)
        plt.fill_between(args.sizes,
                         np.maximum(0, avg_np - std_np),
                         avg_np + std_np,
                         color=line.get_color(), alpha=0.15)

    # Final Graph Formatting
    if args.experiment is None:
        exp_title = "Random Arrays"
        filename = "result1.png"
    else:
        noise_str = "5%" if args.experiment == 1 else "20%"
        exp_title = f"Nearly Sorted ({noise_str} Noise)"
        filename = f"result2.png"

    plt.title(f"Runtime Comparison ({exp_title})", fontsize=14)
    plt.xlabel("Array size (n)", fontsize=12)
    plt.ylabel("Runtime (seconds)", fontsize=12)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)

    plt.savefig(filename, dpi=300)
    print(f"Finished! Graph saved as {filename}")


if __name__ == "__main__":
    main()
