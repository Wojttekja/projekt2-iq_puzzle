import numpy as np

# Creating a 2D array (adjust the array as needed)
original_array = np.array([[1, 2, 3],
                           [4, 5, 6],
                           [7, 8, 9]])

# Flipping the array 90 degrees
flipped_array = np.rot90(original_array, k=2)

print("Original Array:")
print(original_array)
print("\nFlipped Array (90 degrees):")
print(flipped_array)

print(np.flip(original_array, axis=(0, 1)))
print(original_array == flipped_array)