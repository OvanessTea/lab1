import matplotlib.pyplot as pyplot
import control.matlab as matlab
import numpy
import sympy
import math

# Исходные данные
#################################################
ky = 21
koc = 2
tg = 8
ty = 5
# Турбина - паро
tpt = 5
kpt = 1
# Обратная связь - гибкая
#################################################

# Передаточная функция  обратной связи:
woc = matlab.tf([koc, 0], [1])

# Передаточная функция генератора:
wg = matlab.tf([1], [tg, 1])

# Передаточная функция паровой турбины:
wt = matlab.tf([kpt], [tpt, 1])

# Передаточная функция исполнительного устройства:
wy = matlab.tf([ky], [ty, 1])

# Эквивалентная передаточная функция
equivalentLink = matlab.feedback(wy * wg * wt, woc, -1)

# Построение графика переходной функции
timeLine = []
for i in range(0, 10000):
    timeLine.append(i / 1000)
[y, x] = matlab.step(equivalentLink, timeLine)
pyplot.subplot(1, 1, 1)
pyplot.grid(True)
pyplot.plot(x, y, 'purple')
pyplot.show()

sauPoles = matlab.pole(equivalentLink)
print(sauPoles)

systemStability = True

# Проверка устойчивости системы
for i in sauPoles:
    if i.real > 0:
        systemStability = False
        break

# Вывод сообщения о устойчивости / неустойчивости системы
print('Система устойчива' if systemStability else 'Система неустойчива')

# Размыкание САУ и оценка устойчивости по критерию Найквиста
openSau = wt * wg * wy
print(openSau)

# Вывод диаграммы Найквиста
matlab.nyquist(openSau)
pyplot.grid(True)
pyplot.title('Nyquist Diagram of openSau(s) = 21/(200 * s^3 + 105 * s^2 + 18 * s + 1)')
pyplot.xlabel('Re(s)')
pyplot.ylabel('Im(s)')
pyplot.show()

# Снятие логарифмической амплитудно-частотной и логарифмической фазов-частотной характеристик разомкнутой системы
matlab.bode(openSau, dB=False)
pyplot.plot()
axes = pyplot.gcf().get_axes()
axes[0].set_title("ЛАЧХ")
axes[1].set_title("ЛФЧХ")
pyplot.xlabel('Частота, Гц')
pyplot.show()


