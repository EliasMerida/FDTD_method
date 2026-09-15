import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
# fuente tipo tex
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["cmr10"],          # Computer Modern Roman
    "mathtext.fontset": "cm",         # Computer Modern for math
    "axes.formatter.use_mathtext": True,  # tick labels use mathtext too
    "axes.unicode_minus": False,      # proper minus sign with cmr10
})
size = 200 # numero de nodos espaciales
nu_0 = 377 # impedancia del vacio
# inicializamos dos arreglos de size elementos, todos en cero
Ez = np.zeros(size)
Hy = np.zeros(size)
# ciclo para el avance temporal
q_time_max = 500 # maximo numero de pasos temporales
# arreglos bidimensionales para guardar toda la evolución
Ez_all = np.zeros((q_time_max,size))
Hy_all = np.zeros((q_time_max,size))
for q_time in range(q_time_max):
    # actualizamos el campo magnetico
    # el ultimo nodo (size-1) se deja afuera, es decir, siempre es cero
    # esto simula un "conductor magnetico perfecto"
    for m in range(size-1):
        Hy[m] = Hy[m] + (Ez[m+1] - Ez[m]) / nu_0
    # actualizamos el campo electrico
    # el primer nodo Ez[0] se deja fuera
    for m in range(1,size):
        Ez[m] = Ez[m] + (Hy[m] - Hy[m - 1]) * nu_0
    # nodo 0 contiene un campo electrico, tipo onda gaussiana
    Ez[0] = np.exp(-(q_time - 30.) * (q_time - 30.) / 100.)
    # guardamos los valores de E y H
    Ez_all[q_time,:] = Ez[:]
    Hy_all[q_time,:] = Hy[:]
print("Simulación terminada.")

# grafica
# figura con dos subplot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7))
# arreglos para x
x1 = np.arange(size)
x2 = np.arange(size)
# campo electrico
line1, = ax1.plot([], [], color="tab:blue")
ax1.set_xlim(0, len(x1))
ax1.set_ylim(Ez_all.min(), Ez_all.max())
ax1.set_xlabel("$x$")
ax1.set_ylabel("$E_z$")
ax1.set_title("Campo electrico")
# campo magnetico
line2, = ax2.plot([], [], color="tab:orange")
ax2.set_xlim(0, len(x2))
ax2.set_ylim(Hy_all.min(), Hy_all.max())
ax2.set_xlabel("$x$")
ax2.set_ylabel("$H_y$")
ax2.set_title("Campo magnetico")

def update(frame):
    line1.set_data(x1, Ez_all[frame])
    line2.set_data(x2, Hy_all[frame])
    return line1, line2,

anim = FuncAnimation(fig, update, frames=q_time_max, interval=50, blit=True)
plt.tight_layout()
plt.show()
anim.save("1D_example.gif", writer="pillow", fps=20)