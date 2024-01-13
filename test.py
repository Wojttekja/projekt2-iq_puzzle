import matplotlib.pyplot as plt
import numpy as np

# Create a sample NumPy array
array = np.random.random((10, 10))

# Specify values to change colors
threshold_value = 0.5

# Create a custom colormap
cmap = plt.cm.get_cmap('viridis')  # You can choose any other colormap

# Set the color for values below the threshold_value
cmap.set_under('red')

# Set the color for values above the threshold_value
cmap.set_over('blue')

# Plot the array using imshow
plt.imshow(array, cmap=cmap, vmin=0, vmax=1, interpolation='nearest')

# Add colorbar for reference
plt.colorbar()

# Show the plot
plt.show()
