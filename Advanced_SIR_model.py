import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import tensorflow as tf
from matplotlib.ticker import FormatStrFormatter, FuncFormatter



def SIR_model(vector, time, beta, gamma, population): #Инициализация функции

    ds_dt = (-beta*vector[0]*vector[1])/(population)
    di_dt = (beta*vector[0]*vector[1])/(population) - gamma*vector[1]
    dr_dt = gamma*vector[1]

    return(ds_dt, di_dt, dr_dt)

time = np.linspace(-50, 150, 400)
population = 200000
I0 = tf.random.truncated_normal(shape=(100,), mean=1.0, stddev=0.5)

I0 = I0.numpy()
R0 = 0

# S0 = population - I0 - R0
# starting_conditions = [S0, I0, R0]
beta  = 0.5
gamma = 0.3
figure = plt.figure(figsize=(10,10))
ax = figure.subplots()

def formatOy(x, pos):
    return f"{x / 10000}"

for i in range(len(I0)):
    S0 = population - I0[i] - R0
    starting_conditions = [S0, I0[i], R0]
    solve = odeint(SIR_model, starting_conditions, time, args=(beta, gamma, population))
    ax.plot(time, solve[:, 1], color = 'skyblue',  linewidth = 0.05)

I0 = 1
S0 = population - I0 - R0
starting_conditions = [S0, I0, R0]
solve = odeint(SIR_model, starting_conditions, time, args=(beta, gamma, population))
ax.plot(time, solve[:, 1], 'r')

ax.yaxis.set_major_formatter(FuncFormatter(formatOy))

# plt.legend()
plt.ylabel('Population of Infected, $ x 10^4 $', fontsize = 10)
plt.xlabel('Time', fontsize = 10)
plt.xlim([0, 150])
plt.grid()
plt.show()
