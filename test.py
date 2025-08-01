import numpy as np


def MM():
    min_score = []
    for i in A:
        min_score.append(min(i))
    return max(min_score)


def BL():
    avg_score = []
    for i in A:
        avg_score.append(sum(i) / len(i))
    return max(avg_score)


def S():
    max_values = np.max(A, axis=0)
    risk_matrix = np.expand_dims(max_values, axis=0) - A
    max_values2 = np.max(risk_matrix, axis=1)
    return min(max_values2)


def HW():
    a = []
    for i in A:
        s = y * min(i) + (1 - y) * max(i)
        a.append(s)
    return max(a)


def HL():
    a = []
    for i in A:
        for j in q:
            w = y * sum(np.multiply(i, j)) + (1 - y) * min(i)
            a.append(w)
    return max(a)


def G():
    b = []
    l = [
        [53, 51, 29, 32, 59],
        [74, 51, 50, 57, 37],
        [12, 49, 26, 98, 71],
        [14, 23, 84, 72, 24],
        [90, 4, 88, 40, 30],
    ]
    for i in range(len(l)):
        for j in range(len(l[i])):
            if l[i][j] < 0:
                l[i][j] = l[i][j] * l[j]
            if l[i][j] > 0:
                l[i][j] = l[i][j] / q[j]
        b.append(min(l[i]))
    return max(b)


def BLMM():
    return 0


def prod():
    a = []
    for i in A:
        b = np.prod(np.array(i))
        a.append(b)
    return max(a)


A = [
    [53, 51, 29, 32, 59],
    [74, 51, 50, 57, 37],
    [12, 49, 26, 98, 71],
    [14, 23, 84, 72, 24],
    [90, 4, 88, 40, 30],
]
q = [0.2, 0.2, 0.2, 0.2, 0.2]
y = 0.5
print("Критерий минимакса:", MM())
print("Критерий Байеса-Лапласа:", BL())
print("Критерий Сэвиджа:", S())
print("Критерий Гурвица:", HW())
print("Критерий Ходжа-Лемана:", HL())
print("Критерий Гермейера:", G())
print("Критерий Байеса-Лапласа и Минимакса:", BLMM())
print("Критерий Произведения:", prod())
