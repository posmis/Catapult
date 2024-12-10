import pandas as pd

# Исходные данные
# Константы
ro = 1.225 # кг/м^3
g = 9.81 # м/с^2

# Воздушный винт и двигатель
P = 9.5 * g # Н
n = 8500 # об/мин

# Самолет
V = 22 # м/с
S = 0.68 # м^2
m = 28 # кг

# Катапульта
H1 = 1 # м

R = 200 # Н
alpha_R = 0 # град
alpha_P = 0 # град

V2 = 1.2 * V # /с
H2 = 10.7 # м


data_file = "NACA23012_alpha_Cya_Cxa.csv"
teta, Cya, Cxa = [], [], []
df = pd.read_csv(data_file, sep=';')
teta = df['teta'].tolist()
Cya = df['Cya'].tolist()
Cxa = df['Cxa'].tolist()
