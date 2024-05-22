import numpy as np
import matplotlib.pyplot as plt

# Физическая константа
k = 8.99e9  # N m^2/C^2

def calculate_field_and_potential(l, lambda_, xP, yP, zP=0):
    x = np.linspace(-l, l, 1000)
    
    dEx = k * lambda_ * (x - xP) / ((x - xP)**2 + yP**2 + zP**2)**(3/2)
    dEy = k * lambda_ * yP / ((x - xP)**2 + yP**2 + zP**2)**(3/2)
    dEz = k * lambda_ * zP / ((x - xP)**2 + yP**2 + zP**2)**(3/2)
    
    Ex = np.trapz(dEx, x)
    Ey = np.trapz(dEy, x)
    Ez = np.trapz(dEz, x)
    
    E = np.sqrt(Ex**2 + Ey**2 + Ez**2)
    
    dphi = k * lambda_ / np.sqrt((x - xP)**2 + yP**2 + zP**2)
    phi = np.trapz(dphi, x)
    
    return Ex, Ey, phi

# Входные данные
l = 1.0  # Длина нити, м
lambda_ = 1.0e-6  # Линейная плотность заряда, Кл/м

# Координаты сетки для визуализации
x = np.linspace(-2, 2, 20)  # уменьшена плотность точек для лучшей визуализации векторов
y = np.linspace(-2, 2, 20)
X, Y = np.meshgrid(x, y)
print(X)
print(Y)
# Вычисление напряжённости и потенциала в каждой точке сетки
Ex_grid = np.zeros(X.shape)
Ey_grid = np.zeros(X.shape)
phi_grid = np.zeros(X.shape)

for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        Ex, Ey, phi = calculate_field_and_potential(l, lambda_, X[i, j], Y[i, j])
        Ex_grid[i, j] = Ex
        Ey_grid[i, j] = Ey
        phi_grid[i, j] = phi

# Визуализация

fig, ax = plt.subplots(figsize=(10, 8))

# Контурный график потенциала
contour = ax.contour(X, Y, phi_grid, levels=20, cmap='RdYlBu')
plt.colorbar(contour, ax=ax, label='Potential (V)')

# Векторное поле напряжённости
ax.quiver(X, Y, Ex_grid, Ey_grid, color='k', scale=1e6, width=0.005, headwidth=3)

# Нить
ax.plot([-l, l], [0, 0], 'r-', lw=2, label='Charged Wire')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Electric Field and Potential of a Charged Wire')
ax.legend()
plt.show()
