import numpy as np
import matplotlib.pyplot as plt

n = 100
y_size = 35
k = 2
b = 3
x = np.linspace(0, n, n)
y = x * k + b
vals = y + np.random.normal(0, y_size * 0.2, y.shape[0])


def less_squares_method():
    mean_x = np.mean(x)
    mean_y = np.mean(vals)
    kf = np.sum((x - mean_x) * (vals - mean_y)) / np.sum((x - mean_x) ** 2)
    bf = mean_y - kf * mean_x
    return bf, kf


def gradient_decent(n_iter, lr, X, Y):
    errors = np.zeros(n_iter)
    kf = np.random.random(1)[0]
    bf = np.random.random(1)[0]
    for i in range(n_iter):
        y1 = kf * X + bf
        kf += lr * (2 * np.mean(X * (vals - y1)))
        bf += lr * (2 * np.mean(vals - y1))
        errors[i] = np.mean((Y - y1) ** 2)
    return bf, kf, errors


b_lin, k_lin = less_squares_method()
new_y = x * k_lin + b_lin

print(f"""Оцінка поліному степеню 1 для знайдених параметрів: {np.polyfit([b_lin], [k_lin], 1)},
для початкових {np.polyfit([b], [k], 1)}""")


b_grad, k_grad, errors_grad = gradient_decent(100, 0.0001, x, y)

new_y1 = x * k_grad + b_grad

plt.subplot(1, 2, 1)
plt.plot(x, new_y, label='Calculated line')
plt.plot(x, new_y1, label='Calculated line (Grad. de.)')
plt.plot(x, y, label='Start line')
plt.scatter(x, vals)
plt.legend()

plt.subplot(1, 2, 2)

plt.plot(errors_grad, label='Error function result')
plt.show()
