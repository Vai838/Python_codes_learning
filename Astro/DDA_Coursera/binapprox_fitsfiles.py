import numpy as np
from astropy.io import fits
from helper import running_stats

def median_bins_fits(filenames, B):
    """
    Calculate the mean, standard deviation, and bin counts for pixel values across multiple FITS files.
    
    Parameters:
    filenames : list of str
        List of FITS file paths.
    B : int
        Number of bins used to approximate the median.
    
    Returns:
    mean : 2D numpy array
        Array of mean values for each pixel.
    std : 2D numpy array
        Array of standard deviation values for each pixel.
    left_bin : 2D numpy array
        Number of pixel values below mean - std for each pixel.
    bins : 3D numpy array
        Bin counts for pixel values in the range [mean - std, mean + std].
        The shape is (width, height, B), where B is the number of bins.
    """
    # Step 1: Calculate mean and standard deviation for each pixel
    mean, std = running_stats(filenames)
    
    # Determine the dimensions of the 2D image (assuming all images have the same size)
    dim = mean.shape

    # Step 2: Initialize the bins
    # left_bin stores counts of pixel values < (mean - std) for each pixel
    left_bin = np.zeros(dim)
    
    # bins stores counts of pixel values within each bin range for each pixel
    bins = np.zeros((dim[0], dim[1], B))  # Shape: (rows, cols, number of bins)
    
    # Bin width is 2*std divided into B equal bins for each pixel
    bin_width = 2 * std / B

    # Step 3: Iterate over all FITS files
    for filename in filenames:
        # Open the FITS file and extract the 2D image data
        with fits.open(filename) as hdulist:
            data = hdulist[0].data
        
        # Step 4: Populate the left_bin and bins arrays
        for i in range(dim[0]):  # Loop through rows
            for j in range(dim[1]):  # Loop through columns
                value = data[i, j]  # Pixel value at (i, j)
                mean_ = mean[i, j]  # Mean value for pixel (i, j)
                std_ = std[i, j]    # Standard deviation for pixel (i, j)

                # Case 1: Pixel value less than (mean - std)
                if value < (mean_ - std_):
                    left_bin[i, j] += 1  # Increment count of left_bin
                
                # Case 2: Pixel value falls within the bin range
                elif (mean_ - std_) <= value < (mean_ + std_):
                    # Determine the bin index for the current pixel value
                    bin_idx = int((value - (mean_ - std_)) / bin_width[i, j])
                    bins[i, j, bin_idx] += 1  # Increment the corresponding bin count

    # Return the mean, std, left_bin, and bins arrays
    return mean, std, left_bin, bins

def median_approx_fits(filenames, B):
    """
    Approximate the median for each pixel across multiple FITS files.
    
    Parameters:
    filenames : list of str
        List of FITS file paths.
    B : int
        Number of bins used to approximate the median.
    
    Returns:
    median : 2D numpy array
        Approximated median values for each pixel.
    """
    # Step 1: Compute the bins and other necessary statistics
    mean, std, left_bin, bins = median_bins_fits(filenames, B)
    
    # Determine the dimensions of the image
    dim = mean.shape
    
    # Step 2: Calculate the median approximation
    # Number of files
    N = len(filenames)
    
    # Midpoint is (N + 1) // 2, i.e., the middle value in sorted order
    mid = (N + 1) / 2

    # Bin width is the same as before, 2*std divided into B bins
    bin_width = 2 * std / B

    # Step 3: Initialize an empty array to store the median approximation
    median = np.zeros(dim)
    
    # Step 4: Calculate the median for each pixel
    for i in range(dim[0]):  # Loop through rows
        for j in range(dim[1]):  # Loop through columns
            count = left_bin[i, j]  # Start with the count of values less than (mean - std)

            # Go through each bin and accumulate counts until the cumulative count >= midpoint
            for b in range(B):
                count += bins[i, j, b]
                if count >= mid:
                    # We have found the bin that contains the median
                    # Approximate the median as the center of this bin
                    median[i, j] = mean[i, j] - std[i, j] + bin_width[i, j] * (b + 0.5)
                    break  # No need to continue once we found the median bin

    # Return the approximated median array
    return median
