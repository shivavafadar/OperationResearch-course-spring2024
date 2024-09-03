import pulp

# ایجاد مدل بهینه‌سازی
model = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# تعریف متغیرها
x1 = pulp.LpVariable('x1', lowBound=0, cat='Continuous')
x2 = pulp.LpVariable('x2', lowBound=0, cat='Continuous')
x3 = pulp.LpVariable('x3', lowBound=0, cat='Continuous')

# تابع هدف
model += 120 * x1 + 190 * x2 + 240 * x3, "Profit"

# محدودیت‌ها
model += x2 <= 8
model += 2 * x1 + x2 + x3 <= 200
model += x1 + x2 + 3 * x3 <= 200
model += x1 + x2 + 0.5 * x3 <= 110

# حل مدل
model.solve()

# نمایش نتایج
print("Status:", pulp.LpStatus[model.status])
print("Optimal Solution to the problem: ")
print("x1 =", pulp.value(x1))
print("x2 =", pulp.value(x2))
print("x3 =", pulp.value(x3))
print("Maximum Profit = ", pulp.value(model.objective))