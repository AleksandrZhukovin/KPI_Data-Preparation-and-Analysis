import numpy as np
import matplotlib.pyplot as plt

n = 100
k = 2
b = 3
x = np.linspace(0, n, n)
y = x * k + b
vals = []
for i in y:
    vals.append(np.random.normal(i, 2, 1)[0])
vals = np.array(vals)


def less_squares_method():
    kf = np.random.random(1)[0]
    bf = np.random.random(1)[0]
    mean_x = np.mean(x)
    mean_y = np.mean(vals)
    kf = np.sum((x - mean_x) * (vals - mean_y)) / np.sum((x - mean_x) ** 2)
    bf = mean_y - kf * mean_x
    return bf, kf


def gradient_decent(n_iter, lr, x, y):
    errors = np.zeros(n_iter)
    kf = np.random.random(1)[0]
    bf = np.random.random(1)[0]
    for i in range(n_iter):
        y1 = kf * x + bf
        kf += lr * (2 * np.sum(x * (vals - y1)))
        bf += lr * (2 * np.sum(vals - y1))
        errors[i] = np.mean((y - y1) ** 2)
    return bf, kf, errors


def error(n_iter, lr):
    kt = np.random.random(1)[0]
    bt = np.random.random(1)[0]
    for _ in range(n_iter):
        y1 = kt * x + bt
        kt += lr * (2 * np.sum(x * (vals - y1)))
        bt += lr * (2 * np.sum(vals - y1))
    return np.sum((vals - (kt * x + bt))**2)


bf, kf = less_squares_method()
new_y = x * kf + bf
print(f"""Оцінка поліному степеню 1 для знайдених параметрів: {np.polyfit([bf], [kf], 1)},
для початкових {np.polyfit([b], [k], 1)}""")

kf = np.random.random(1)[0]
bf = np.random.random(1)[0]
bf1, kf1, errors = gradient_decent(1000, 0.001, x, y)
print(errors)
new_y1 = x * kf1 + bf1

plt.subplot(1, 2, 1)
plt.plot(x, new_y, label='Calculated line')
plt.plot(x, new_y1, label='Calculated line (Grad. de.)')
plt.plot(x, y, label='Start line')
# plt.scatter(x, vals)
plt.legend()

plt.subplot(1, 2, 2)
iters = [i for i in range(1, 11)]
# errors = [error(e, 0.0001) for e in range(1, 11)]
plt.plot(errors, label='Error function result')
plt.show()
