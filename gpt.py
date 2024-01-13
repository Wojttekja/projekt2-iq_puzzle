import matplotlib.pyplot as plt
import numpy as np

# Create a figure with a custom grid layout
fig = plt.figure(figsize=(15, 10))
gs = fig.add_gridspec(2, 3, width_ratios=[2, 1, 1], height_ratios=[1, 1])

# Add subplots to the grid
ax1 = fig.add_subplot(gs[0, 0])  # Top-left subplot (big)
ax2 = fig.add_subplot(gs[0, 1])  # Top-center subplot
ax3 = fig.add_subplot(gs[0, 2])  # Top-right subplot
ax4 = fig.add_subplot(gs[1, 1])  # Bottom-center subplot
ax5 = fig.add_subplot(gs[1, 2])  # Bottom-right subplot

# Plot the initial data on each subplot using imshow for NumPy ndarrays
img1 = ax1.imshow(np.sin(np.linspace(0, 10, 100)).reshape(-1, 1), aspect='auto', cmap='viridis')
ax1.set_title('Plot 1 (Big)')

img2 = ax2.imshow(np.cos(np.linspace(0, 10, 100)).reshape(-1, 1), aspect='auto', cmap='viridis')
ax2.set_title('Plot 2')

img3 = ax3.imshow(np.tan(np.linspace(0, 10, 100)).reshape(-1, 1), aspect='auto', cmap='viridis')
ax3.set_title('Plot 3')

img4 = ax4.imshow(np.exp(-np.linspace(0, 10, 100)).reshape(-1, 1), aspect='auto', cmap='viridis')
ax4.set_title('Plot 4')

img5 = ax5.imshow(np.log(np.linspace(1, 11, 100) + 1).reshape(-1, 1), aspect='auto', cmap='viridis')
ax5.set_title('Plot 5')

# Remove ticks and labels on the axes
ax1.set_xticks([])
ax1.set_yticks([])
ax1.set_xticklabels([])
ax1.set_yticklabels([])

# Optionally, remove ticks and labels on other subplots as needed
for ax in [ax2, ax3, ax4, ax5]:
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xticklabels([])
    ax.set_yticklabels([])

# Adjust layout to prevent clipping of titles
plt.tight_layout()

# Update the data in the plots as your arrays change (example with random data)
for i in range(10):
    img1.set_data(np.sin(np.linspace(0, 10, 100)).reshape(-1, 1) + np.random.normal(0, 0.1, (100, 1)))
    img2.set_data(np.cos(np.linspace(0, 10, 100)).reshape(-1, 1) + np.random.normal(0, 0.1, (100, 1)))
    img3.set_data(np.tan(np.linspace(0, 10, 100)).reshape(-1, 1) + np.random.normal(0, 0.1, (100, 1)))
    img4.set_data(np.exp(-np.linspace(0, 10, 100)).reshape(-1, 1) + np.random.normal(0, 0.1, (100, 1)))
    img5.set_data(np.log(np.linspace(1, 11, 100) + 1).reshape(-1, 1) + np.random.normal(0, 0.1, (100, 1)))

    # Optionally, you can pause for a short time to see the updates
    plt.pause(0.5)

# Show the final plot
plt.show()
