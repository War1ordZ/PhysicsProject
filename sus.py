import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Константы
lambda_charge = 1e-6  # Кулоны на метр
L = 1.0  # Длина нити в метрах
epsilon_0 = 8.854187817e-12  # Фарад на метр

# Функция для вычисления потенциала в точке (x, y, z)
def potential(x, y, z, lambda_charge, L, epsilon_0):
    def integrand(x_prime):
        return lambda_charge / np.sqrt((x - x_prime)**2 + y**2 + z**2)
    x_values = np.linspace(-L/2, L/2, 1000)
    V = np.trapz(integrand(x_values), x_values) / (4 * np.pi * epsilon_0)
    return V

# Функция для вычисления электрического поля в точке (x, y, z)
def electric_field(x, y, z, lambda_charge, L, epsilon_0):
    def integrand(x_prime):
        r_squared = (x - x_prime)**2 + y**2 + z**2
        return (lambda_charge * (x - x_prime) / r_squared**(3/2),
                lambda_charge * y / r_squared**(3/2),
                lambda_charge * z / r_squared**(3/2))
    x_values = np.linspace(-L/2, L/2, 1000)
    Ex = np.trapz([integrand(x_prime)[0] for x_prime in x_values], x_values) / (4 * np.pi * epsilon_0)
    Ey = np.trapz([integrand(x_prime)[1] for x_prime in x_values], x_values) / (4 * np.pi * epsilon_0)
    Ez = np.trapz([integrand(x_prime)[2] for x_prime in x_values], x_values) / (4 * np.pi * epsilon_0)
    return Ex, Ey, Ez

# Сетка точек
x = np.linspace(-2, 2, 20)
y = np.linspace(-2, 2, 20)
z = np.linspace(-2, 2, 20)
X, Y, Z = np.meshgrid(x, y, z)

# Вычисление потенциала
V = np.vectorize(potential)(X, Y, Z, lambda_charge, L, epsilon_0)

# Вычисление компонентов электрического поля
Ex, Ey, Ez = np.vectorize(electric_field)(X, Y, Z, lambda_charge, L, epsilon_0)

# Визуализация потенциала
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X, Y, Z, c=V, cmap='viridis')
ax.set_title('Electric Potential due to a Uniformly Charged Rod')
ax.set_xlabel('x (m)')
ax.set_ylabel('y (m)')
ax.set_zlabel('z (m)')
plt.colorbar(ax.scatter(X, Y, Z, c=V, cmap='viridis'), label='Electric Potential (V)')
plt.show()

# Визуализация напряженности поля
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.quiver(X, Y, Z, Ex, Ey, Ez, length=0.1, normalize=True)
ax.set_title('Electric Field due to a Uniformly Charged Rod')
ax.set_xlabel('x (m)')
ax.set_ylabel('y (m)')
ax.set_zlabel('z (m)')
plt.show()
