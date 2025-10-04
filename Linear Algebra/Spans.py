# Week 5 Session 1
# Python Exploration: Visualizing Spans in Linear Algebra
# https://www.khanacademy.org/computing/computer-science/linear-algebra
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from itertools import product, combinations
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import proj3d

# Define two vectors in R^2
'''v1 = np.array([2, 1])
v2 = np.array([1, 2])

# Create a grid of linear combinations
a = np.linspace(-2, 2, 20)
b = np.linspace(-2, 2, 20)
A, B = np.meshgrid(a, b)
X = A * v1[0] + B * v2[0]
Y = A * v1[1] + B * v2[1]

# Plot the span of the two vectors
plt.figure(figsize=(6,6))
plt.quiver(0, 0, v1[0], v1[1], angles='xy', scale_units='xy', scale=1, color='r', label='v1')
plt.quiver(0, 0, v2[0], v2[1], angles='xy', scale_units='xy', scale=1, color='b', label='v2')
plt.scatter(X, Y, alpha=0.3, s=10)
plt.axhline(0, color='k',linewidth=0.5)
plt.axvline(0, color='k',linewidth=0.5)
plt.legend()
plt.grid(True)
plt.show()'''

# Define three vectors in R^3
v1 = np.array([1, -1, 2])
v2 = np.array([2, 1, -1])

# Generate linear combinations
a = np.linspace(1, 2, 10)
b = np.linspace(0, 1, 10)
A, B = np.meshgrid(a, b)
X = A * v1[0] + B * v2[0]
Y = A * v1[1] + B * v2[1]
Z = A * v1[2] + B * v2[2]

# Plot the span of the two vectors in 3D
fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, alpha=0.5, color = 'lightblue')
ax.quiver(0, 0, 0, v1[0], v1[1], v1[2], color='r', label='v1')
ax.quiver(0, 0, 0, v2[0], v2[1], v2[2], color='b', label='v2')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.legend()
plt.show()