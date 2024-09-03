import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull

def simplex_method(c, A, b):
    num_vars = len(c)
    num_constraints = len(b)
    tableau = np.zeros((num_constraints + 1, num_vars + num_constraints + 1))
    tableau[:-1, :-1] = np.hstack((A, np.eye(num_constraints)))
    tableau[:-1, -1] = b
    tableau[-1, :num_vars] = -c
    basis = list(range(num_vars, num_vars + num_constraints))
    tracking_points = []
    step_sizes = []
    objective_values = []

    while True:
        if np.all(tableau[-1, :-1] >= 0):
            break
        col = np.argmin(tableau[-1, :-1])
        if np.all(tableau[:-1, col] <= 0):
            raise Exception("The problem is unbounded.")
        ratios = np.divide(tableau[:-1, -1], tableau[:-1, col], out=np.full_like(tableau[:-1, -1], np.inf), where=tableau[:-1, col] > 0)
        row = np.argmin(ratios)
        pivot = tableau[row, col]
        step_sizes.append(tableau[row, -1])  # Record the step size (pivot value)
        tableau[row, :] /= pivot
        for i in range(num_constraints + 1):
            if i != row:
                tableau[i, :] -= tableau[i, col] * tableau[row, :]
        basis[row] = col
        solution = np.zeros(num_vars)
        for i in range(num_constraints):
            if basis[i] < num_vars:
                solution[basis[i]] = tableau[i, -1]
        tracking_points.append(solution.copy())
        current_z = np.dot(c, solution)  # Calculate the objective function value
        objective_values.append(current_z)

    return tableau, solution, tableau[-1, -1], tracking_points, step_sizes, objective_values

# Coefficients of the objective function and constraints
c = np.array([120, 190, 240])
A = np.array([[0, 1, 0], [2, 1, 1], [1, 1, 3], [2, 2, 1]])
b = np.array([8, 200, 200, 110])

tableau, solution, max_z, tracking_points, step_sizes, objective_values = simplex_method(c, A, b)

# Generate boundary points based on the constraints
x1_vals = np.linspace(0, 50, 100)
x2_vals = np.linspace(0, 8, 100)
x3_vals = np.linspace(0, 67, 100)
boundary_points = []
for x1 in x1_vals:
    for x2 in x2_vals:
        for x3 in x3_vals:
            if x2 <= 8 and 2 * x1 + x2 + x3 <= 200 and x1 + x2 + 3 * x3 <= 200 and 2 * x1 + 2 * x2 + x3 <= 110:
                boundary_points.append([x1, x2, x3])

# Plotting
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
boundary_points = np.array(boundary_points)
hull = ConvexHull(boundary_points)
poly3d = [[boundary_points[vertex] for vertex in face] for face in hull.simplices]
ax.add_collection3d(Poly3DCollection(poly3d, facecolors='cyan', alpha=0.25, edgecolors='r'))
tracking_points = np.array(tracking_points)
ax.scatter(tracking_points[:, 0], tracking_points[:, 1], tracking_points[:, 2], color='red', s=50, label='Simplex Iterations')

# Add arrows and print iteration details
if len(tracking_points) > 1:
    distances = np.linalg.norm(np.diff(tracking_points, axis=0), axis=1)
    arrow_length = np.mean(distances) / 5
    for i in range(1, len(tracking_points)):
        start_point = tracking_points[i - 1]
        end_point = tracking_points[i]
        arrow = end_point - start_point
        ax.quiver(start_point[0], start_point[1], start_point[2], arrow[0], arrow[1], arrow[2], color='blue', length=arrow_length, normalize=True)
        print(f"Iteration {i}: Point = {tracking_points[i]}, Objective Value = {objective_values[i]:.2f}, Step Size = {step_sizes[i-1]:.4f}")

ax.set_xlim([0, 50])
ax.set_ylim([0, 8])
ax.set_zlim([0, 67])
ax.set_xlabel('x1')
ax.set_ylabel('x2')
ax.set_zlabel('x3')
plt.legend()
plt.title('Feasible Region with Simplex Iterations')
plt.show()

# Print the final results
print("Final Tableau:")
print(tableau)
print("Solution:")
print(f"x1 = {solution[0]:.2f}, x2 = {solution[1]:.2f}, x3 = {solution[2]:.2f}")
print(f"Maximum z = {max_z:.2f}")
