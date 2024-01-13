import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

# Create a sample NumPy array with values ranging from 0 to 12
array = np.random.randint(0, 13, size=(10, 10))

# Define colors for each value
colors = ['white', 'blue', 'yellow', 'green', 'orange', 'purple', 'pink', 'brown', 'red', 'cyan', 'magenta', 'gray', 'lightgreen']

# Create a custom colormap
cmap = ListedColormap(colors)

# Plot the array using imshow
plt.imshow(array, cmap=cmap, vmin=0, vmax=12, interpolation='nearest')

# Add colorbar for reference
plt.colorbar(ticks=np.arange(13))

# Show the plot
plt.show()
