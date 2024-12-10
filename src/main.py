from math import radians

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

import data

def calc_consts(dict_):
    G = data.m * data.g
    N = [G * math.sin(teta) for teta in data.teta]
    L1 = [data.H1 / math.sin(math.radians(teta)) for teta in data.teta]
    Xa = [Cxa * data.S * data.ro * math.pow(data.V, 2) / 2 for Cxa in data.Cxa]
    Ya = [Cya * data.S * data.ro * math.pow(data.V, 2) / 2 for Cya in data.Cya]
    nxa = [(data.R * math.cos(math.radians(data.alpha_R)) +
           data.P * math.cos(math.radians(data.alpha_P)) - Xa_value) / G for Xa_value in Xa]
    nya = [(data.R * math.sin(math.radians(data.alpha_R)) +
           data.P * math.sin(math.radians(data.alpha_P)) + Ya_value + N_value) / G for Ya_value, N_value in zip(Ya, N)]
    dict_['G'] = G
    dict_['N'] = N
    dict_['L1'] = L1
    dict_['Xa'] = Xa
    dict_['Ya'] = Ya
    dict_['nxa'] = nxa
    dict_['nya'] = nya

def j_velocity_calc(dict_):
    teta_r = [math.radians(angle) for angle in data.teta]
    j = [data.g * ((data.R * math.cos(math.radians(data.alpha_R)) +
                   data.P * math.cos(math.radians(data.alpha_P))) /
                  (data.g * data.m) -
                  math.sin(teta)) for teta in teta_r]
    nx_av = [j_value / data.g + math.sin(math.radians(teta)) for j_value, teta in zip(j, data.teta)]
    return j, nx_av

def v1_velocity_calc(dict_):
   V1 = [math.sqrt(2 * data.g * (nx_av_value - math.sin(math.radians(teta))) * L1_value)
         for nx_av_value, teta, L1_value in zip(dict_['nx_av'], data.teta, dict_['L1'])]
   return V1

def t1_calc(dict_):
    t1 = [V1_value / j_value for V1_value, j_value in zip(dict_['V1'], dict_['j'])]
    return t1

def forces_calc(dict_):
    P2 = [Ya_value + data.R * math.sin(math.radians(data.alpha_R)) +
          data.P * math.sin(math.radians(data.alpha_P)) for Ya_value in dict_['Ya']]
    G2 = [dict_['G'] * math.cos(math.radians(teta)) for teta in data.teta]
    return P2, G2

def l_as_calc(dict_):
    nx1 = [(data.R + data.P - Xa_value) / dict_['G'] for Xa_value in dict_['Xa']]
    nx2 = [(data.P - Xa_value) / dict_['G'] for Xa_value in dict_['Xa']]
    nx12 = [(nx1_value + nx2_value) / 2 for nx1_value, nx2_value in zip(nx1, nx2)]
    L_d = [1 / nx12_value * ((data.V2 ** 2 - V1_value ** 2) / (2 * data.g) + data.H2 - data.H1)
            for nx12_value, V1_value in zip(nx12, dict_['V1'])]
    return L_d


def show_plot(data_list, labels, xylabels, teta, fill_conditions=None):
    plt.figure(figsize=(10, 6))

    for vars_, label_ in zip(data_list, labels):
        plt.plot(teta, vars_, label=label_, linewidth=2)

    if fill_conditions:
        for condition in fill_conditions:
            y1 = condition['y1']
            y2 = condition['y2']
            where = condition['where']
            color = condition.get('color', 'gray')
            alpha = condition.get('alpha', 0.3)
            hatch = condition.get('hatch', None)

            plt.fill_between(
                teta, y1, y2, where=where, interpolate=True,
                color=color, alpha=alpha, hatch=hatch
            )

    # Настройки графика
    plt.xlabel(xylabels[0], fontsize=14, labelpad=10, color="black")
    plt.ylabel(xylabels[1], fontsize=14, labelpad=10, color="black")
    plt.title("", fontsize=16, fontweight="bold", color="darkorange")
    plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
    plt.legend(fontsize=12, loc="lower right")
    plt.grid(color="gray", linestyle="--", linewidth=0.5)
    plt.show()


def save_arrays_to_excel_pandas(filename, arrays):
    """
    Сохраняет данные из списков массивов в файл Excel.

    :param filename: Имя файла для сохранения (строка).
    :param arrays: Список массивов одинаковой длины (список списков).
    """
    # Проверка, что массивы имеют одинаковую длину
    if not all(len(arr) == len(arrays[0]) for arr in arrays):
        raise ValueError("Все массивы должны иметь одинаковую длину.")

    # Создаем DataFrame
    df = pd.DataFrame({f"Column {i + 1}": arr for i, arr in enumerate(arrays)})

    # Сохраняем в Excel
    df.to_excel(filename, index=False)
    print(f"Данные успешно сохранены в {filename}")


if __name__ == "__main__":
    values = {}
    calc_consts(values)
    values['j'], values['nx_av'] = j_velocity_calc(values)
    values['V1'] = v1_velocity_calc(values)
    values['t1'] = t1_calc(values)
    values['P2'], values['G2'] = forces_calc(values)
    values['L_d'] = l_as_calc(values)

    # Убедимся, что массивы совпадают по размерам
    data.teta = np.array(data.teta).flatten()
    values['P2'] = np.array(values['P2']).flatten()
    values['G2'] = np.array(values['G2']).flatten()
    where_condition = values['P2'] > values['G2']

    # Условия закраски
    fill_conditions = [
        {
            'y1': values['P2'],
            'y2': values['G2'],
            'where': where_condition,
            'color': 'black',
            'alpha': 0.3,
            'hatch': '//'
        },
        {
            'y1': values['P2'],
            'y2': values['G2'],
            'where': ~where_condition,
            'color': 'white',
            'alpha': 0.3,
            'hatch': ''
        }
    ]

    # save_arrays_to_excel_pandas("data.xlsx", [data.teta, values['j'], values['P2'], values['G2'], values['V1'], values['L_d']])

    show_plot([values['P2'], values['G2']], ["P2", "G2"], ["Angle, deg", "Force, N"], data.teta, fill_conditions)
    show_plot([values['j']], ["j"], ["Angle, deg", "Velocity, m/s"], data.teta)
    show_plot([values['V1']], ["V1"], ["Angle, deg", "Velocity, m/s"], data.teta)
    show_plot([values['L_d']], ["L_d"], ["Angle, deg", "Displacement, m"], data.teta)