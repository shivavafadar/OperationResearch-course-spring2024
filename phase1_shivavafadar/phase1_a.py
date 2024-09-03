import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull

# تعریف محدودیت‌ها
def constraints(x1, x2, x3):
    return (
        x2 <= 8 and
        x1 + x2 + 3*x3 <= 200 and
        2*x1 + 2*x2 + x3 <= 110 and
        x1 >= 0 and
        x2 >= 0 and
        x3 >= 0
    )

# ایجاد نقاطی که محدودیت‌ها را رعایت می‌کنند
x1_vals = np.linspace(0, 100, 50)
x2_vals = np.linspace(0, 8, 50)
x3_vals = np.linspace(0, 100, 50)

points = []
for x1 in x1_vals:
    for x2 in x2_vals:
        for x3 in x3_vals:
            if constraints(x1, x2, x3):
                points.append([x1, x2, x3])

points = np.array(points)

# محاسبه محدب محدب
hull = ConvexHull(points)

# تعریف نقاط مرزی برای هر محدودیت
boundary_points = []

for x1 in x1_vals:
    for x3 in x3_vals:
        boundary_points.append([x1, 8, x3])  # x2 <= 8

for x1 in x1_vals:
    for x2 in x2_vals:
        boundary_points.append([x1, x2, 200 - 2*x1 - x2])  # 2*x1 + x2 + x3 <= 200
        boundary_points.append([x1, x2, (200 - x1 - x2) / 3])  # x1 + x2 + 3*x3 <= 200
        boundary_points.append([x1, x2, (110 - x1 - x2) * 2])  # x1 + x2 + 0.5*x3 <= 110

boundary_points = np.array(boundary_points)

# محاسبه محدب محدب مرزها
hull = ConvexHull(boundary_points)

# رسم چندوجهی
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# افزودن سطوح چندوجهی
poly3d = [[boundary_points[vertice] for vertice in simplex] for simplex in hull.simplices]
ax.add_collection3d(Poly3DCollection(poly3d, facecolors='lightyellow', linewidths=1, edgecolors='blue', alpha=0.5))

# رسم مرزهای محدودیت‌ها
for simplex in hull.simplices:
    simplex = np.append(simplex, simplex[0])  # بسته شدن چندوجهی
    ax.plot(boundary_points[simplex, 0], boundary_points[simplex, 1], boundary_points[simplex, 2], 'k-')

# تنظیمات نمودار
ax.set_xlabel('x1: khamir dandan ') 
ax.set_ylabel('x2: maye dastshooei ')
ax.set_zlabel('x3: maye ebasshooei ')

plt.show()
