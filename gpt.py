import matplotlib.pyplot as plt
import numpy as np

# Generate some example data
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.tan(x)
y4 = np.exp(-x)
y5 = np.log(x + 1)

# Create a figure with a custom grid layout
fig = plt.figure(figsize=(15, 10))
gs = fig.add_gridspec(2, 3, width_ratios=[2, 1, 1], height_ratios=[1, 1])

# Add subplots to the grid
ax1 = fig.add_subplot(gs[0, 0])  # Top-left subplot (big)
ax2 = fig.add_subplot(gs[0, 1])  # Top-center subplot
ax3 = fig.add_subplot(gs[0, 2])  # Top-right subplot
ax4 = fig.add_subplot(gs[1, 1])  # Bottom-center subplot
ax5 = fig.add_subplot(gs[1, 2])  # Bottom-right subplot

# Plot the data on each subplot
ax1.plot(x, y1, label='sin(x)')
ax1.set_title('Plot 1 (Big)')
ax2.plot(x, y2, label='cos(x)')
ax2.set_title('Plot 2')
ax3.plot(x, y3, label='tan(x)')
ax3.set_title('Plot 3')
ax4.plot(x, y4, label='exp(-x)')
ax4.set_title('Plot 4')
ax5.plot(x, y5, label='log(x+1)')
ax5.set_title('Plot 5')

# Add labels, legends, etc. as needed
for ax in [ax1, ax2, ax3, ax4, ax5]:
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.legend()

# Adjust layout to prevent clipping of titles
plt.tight_layout()

# Show the plot
plt.show()
