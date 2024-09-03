import numpy as np

def simplex_method(c, A, b):
    # c: Coefficients of the objective function (cost vector)
    # A: Coefficient matrix for constraints
    # b: Right-hand side values of constraints

    num_vars = len(c)
    num_constraints = len(b)

    # Initialize tableau
    tableau = np.zeros((num_constraints + 1, num_vars + num_constraints + 1))
    tableau[:-1, :-1] = np.hstack((A, np.eye(num_constraints)))
    tableau[:-1, -1] = b
    tableau[-1, :num_vars] = -c

    # Basis variables
    basis = list(range(num_vars, num_vars + num_constraints))

    while True:
        # Check if the solution is optimal (no negative coefficients in the objective row)
        if np.all(tableau[-1, :-1] >= 0):
            break

        # Entering variable (most negative coefficient in the objective row)
        col = np.argmin(tableau[-1, :-1])

        # Check if the problem is unbounded
        if np.all(tableau[:-1, col] <= 0):
            raise Exception("The problem is unbounded.")

        # Leaving variable (minimum ratio test)
        ratios = np.divide(tableau[:-1, -1], tableau[:-1, col], out=np.full_like(tableau[:-1, -1], np.inf), where=tableau[:-1, col] > 0)
        row = np.argmin(ratios)

        # Pivot on the tableau
        pivot = tableau[row, col]
        tableau[row, :] /= pivot
        for i in range(num_constraints + 1):
            if i != row:
                tableau[i, :] -= tableau[i, col] * tableau[row, :]

        basis[row] = col

    # Solution
    solution = np.zeros(num_vars)
    for i in range(num_constraints):
        if basis[i] < num_vars:
            solution[basis[i]] = tableau[i, -1]

    return tableau, solution, tableau[-1, -1]

# Coefficients of the objective function
c = np.array([120, 190, 240])

# Coefficient matrix for constraints
A = np.array([
    [0, 1, 0],  # x2 <= 8
    [2, 1, 1],  # 2x1 + x2 + x3 <= 200
    [1, 1, 3],  # x1 + x2 + 3x3 <= 200
    [2, 2, 1]   # 2x1 + 2x2 + x3 <= 110
])

# Right-hand side values of constraints
b = np.array([8, 200, 200, 110])

tableau, solution, max_z = simplex_method(c, A, b)
print("Final Tableau:")
print(tableau)
print("Solution:")
print("x1 = {:.2f}, x2 = {:.2f}, x3 = {:.2f}".format(*solution))
print("Maximum z = {:.2f}".format(max_z))
