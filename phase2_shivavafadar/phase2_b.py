import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull

# Define the constraints function
def constraints(x1, x2, x3):
    return (
        x2 <= 8 and
        2 * x1 + x2 + x3 <= 200 and
        x1 + x2 + 3 * x3 <= 200 and
        2 * x1 + 2 * x2 + x3 <= 110 and
        x1 >= 0 and
        x2 >= 0 and
        x3 >= 0
    )

x1_vals = np.linspace(0, 100, 100)
x2_vals = np.linspace(0, 8, 100)
x3_vals = np.linspace(0, 100, 100)

boundary_points = []

# Generate points on each constraint surface
for x1 in x1_vals:
    for x2 in x2_vals:
        if 2 * x1 + x2 <= 200:
            boundary_points.append([x1, x2, 200 - 2 * x1 - x2])  # 2*x1 + x2 + x3 = 200
        if x1 + x2 <= 200:
            boundary_points.append([x1, x2, (200 - x1 - x2) / 3])  # x1 + x2 + 3*x3 = 200
        if 2 * x1 + 2 * x2 <= 110:
            boundary_points.append([x1, x2, 110 - 2 * x1 - 2 * x2])  # 2*x1 + 2*x2 + x3 = 110

for x1 in x1_vals:
    for x3 in x3_vals:
        boundary_points.append([x1, 8, x3])  # x2 = 8

for x2 in x2_vals:
    for x3 in x3_vals:
        boundary_points.append([0, x2, x3])  # x1 = 0

# Convert to numpy array for hull computation
boundary_points = np.array(boundary_points)

# Plotting
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Filter only points within all constraints
filtered_points = np.array([pt for pt in boundary_points if constraints(*pt)])
hull = ConvexHull(filtered_points)

# Draw the convex hull
poly3d = [[filtered_points[vertex] for vertex in face] for face in hull.simplices]
ax.add_collection3d(Poly3DCollection(poly3d, facecolors='cyan', alpha=0.25, edgecolors='black'))

# Mark the edges of the convex hull
for simplex in hull.simplices:
    simplex = np.append(simplex, simplex[0])  # wrap back to first vertex
    ax.plot(filtered_points[simplex, 0], filtered_points[simplex, 1], filtered_points[simplex, 2], 'k-')

ax.set_xlabel('x1')
ax.set_ylabel('x2')
ax.set_zlabel('x3')
ax.set_title('Feasible Region with Boundaries Highlighted')
plt.show()
