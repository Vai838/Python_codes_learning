# binapprox.py
# A Python program to calculate the approximate median of a list of numbers using the binapprox algorithm made by me with the help of chatgpt.

import numpy as np

def median_bins(values, B):
    """
    Calculate the mean, standard deviation, and bins to approximate the median.

    Parameters:
    values (list): The list of numbers from which we want to calculate the approximate median.
    B (int): The number of bins used to partition the data.

    Returns:
    mean (float): The mean of the values.
    std (float): The standard deviation of the values.
    left_bin (int): The number of values less than mean - std.
    bins (numpy array): The counts of values in each bin between mean - std and mean + std.
    """
    
    # Step 1: Calculate the mean and standard deviation of the list
    mean = np.mean(values)
    std = np.std(values)
    
    # Step 2: Initialize the bins
    left_bin = 0  # This counts how many values are less than mean - std
    bins = np.zeros(B)  # Array to store the count for each bin
    bin_width = 2 * std / B  # The width of each bin is determined by the total range (2 * std) divided by B

    # Step 3: Bin the values
    for value in values:
        if value < mean - std:
            # If the value is less than mean - std, count it in the left_bin
            left_bin += 1
        elif value < mean + std:
            # If the value lies between mean - std and mean + std, place it in the appropriate bin
            bin = int((value - (mean - std)) / bin_width)  # Calculate which bin this value belongs to
            bins[bin] += 1
        # Values greater than mean + std are ignored

    # Step 4: Return the calculated values: mean, std, the count of left_bin, and the bins array
    return mean, std, left_bin, bins

def median_approx(values, B):
    """
    Approximate the median of the given values using the binapprox algorithm.

    Parameters:
    values (list): The list of numbers from which we want to calculate the approximate median.
    B (int): The number of bins used to partition the data.

    Returns:
    median (float): The approximated median value.
    """
    
    # Step 5: Use the `median_bins` function to get the mean, std, left_bin count, and bin counts
    mean, std, left_bin, bins = median_bins(values, B)
    
    # Step 6: Calculate the middle position (N + 1)/2, where N is the number of elements in the list
    N = len(values)
    mid = (N + 1) / 2  # This is the target cumulative count for finding the median
    
    # Step 7: Find the bin that contains the median
    count = left_bin  # Start counting from the left_bin
    for b, bincount in enumerate(bins):
        count += bincount
        if count >= mid:
            # When the cumulative count exceeds the midpoint, we know the median is in this bin
            break
    
    # Step 8: Calculate the approximate median using the bin's position
    bin_width = 2 * std / B  # Recalculate bin width
    median = mean - std + bin_width * (b + 0.5)  # Midpoint of the bin is the lower boundary + half bin width
    
    return median

# You can use this to test your functions.
if __name__ == '__main__':
    # Test the functions with the examples provided in the question.
    
    # First test case
    values1 = [1, 1, 3, 2, 2, 6]
    B1 = 3
    print("Test Case 1:")
    print("Bins:", median_bins(values1, B1))
    print("Approximate Median:", median_approx(values1, B1))
    
    # Second test case
    values2 = [1, 5, 7, 7, 3, 6, 1, 1]
    B2 = 4
    print("\nTest Case 2:")
    print("Bins:", median_bins(values2, B2))
    print("Approximate Median:", median_approx(values2, B2))
    
    # Third test case where binapprox is a bad approximation
    values3 = [0, 1]
    B3 = 5
    print("\nTest Case 3:")
    print("Bins:", median_bins(values3, B3))
    print("Approximate Median:", median_approx(values3, B3))
