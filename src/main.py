import matplotlib.pyplot as plt
import numpy as np
import math

import data

def calc_consts(dict_):
    G = data.m * data.g
    N = G
    L1 = [data.H / math.sin(math.radians(teta)) for teta in data.teta]
    Xa = data.Cxa * data.S * data.ro * math.pow(data.V, 2) / 2
    Ya = data.Cya * data.S * data.ro * math.pow(data.V, 2) / 2
    nxa = (data.R * math.cos(math.radians(data.alpha_R)) +
           data.P * math.cos(math.radians(data.alpha_P)) - Xa) / G
    nya = (data.R * math.sin(math.radians(data.alpha_R)) +
           data.P * math.sin(math.radians(data.alpha_P)) + Ya + N) / G

    dict_['G'] = G
    dict_['N'] = N
    dict_['L1'] = L1
    dict_['Xa'] = Xa
    dict_['Ya'] = Ya
    dict_['nxa'] = nxa
    dict_['nya'] = nya



def j_velocity_calc():
    teta_r = [math.radians(angle) for angle in data.teta]
    j = [data.g * ((data.R * math.cos(math.radians(data.alpha_R)) +
                   data.P * math.cos(math.radians(data.alpha_P))) /
                  (data.g * data.m) -
                  math.sin(teta)) for teta in teta_r]
    return j

# def V1_velocity_calc():
#    V1 = math.sqrt(2 * data.g * ())
#    return V1

def show_plot(vars, teta):
    plt.figure(figsize=(10, 6))  # Размер графика
    plt.plot(teta, vars, label="Sine Wave", color="blue", linewidth=1)
    plt.xlabel("X-axis (top)", fontsize=14, labelpad=10, color="darkred")
    plt.ylabel("Y-axis (bottom)", fontsize=14, labelpad=10, color="darkblue")
    plt.title("Beautiful Plot Example", fontsize=16, fontweight="bold", color="darkorange")
    plt.legend(fontsize=12, loc="upper right")
    plt.grid(color="gray", linestyle="--", linewidth=0.5)
    plt.show()

if __name__ == "__main__":
    values = {}
    calc_consts(values)
    show_plot(values['L1'], data.teta)
    print()