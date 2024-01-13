import numpy as np

# Create a multidimensional array
array = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])

# Get all indices using numpy.indices
indices = np.indices(array.shape).T.reshape(-1, array.ndim)

# Display the result
print(indices)
print(array[indices[0]])