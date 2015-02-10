__author__ = '109714'

import matplotlib.pyplot as plt
import numpy as nmp
import csv


def load_data(file_name):
    with open(file_name, 'rb') as f:
        reader = csv.reader(f)
        tmp = [row[1:] for row in reader]
    f.close()
    data = nmp.array(tmp[1:])

    m = []
    for i in range(0, 200):
        suma = 0.0
        for j in data[i, 1:]:
            suma += float(j)
        m.append(suma*100/32)

    ox = []
    for i in data[:, 0]:
        ox.append(int(i)/1000)

    last = []
    for i in data[199, 1:]:
        last.append(float(i)*100)

    return m, ox, last


def draw_left(m_list, ox_list, series):
    s1 = plt.subplot(1, 2, 1)
    [i.set_linewidth(0.5) for i in s1.spines.itervalues()]
    plt.xlim(xmax=500)
    plt.axis(siez='small')
    plt.grid(True, alpha=0.5, linewidth=0.3)
    plt.tick_params(labelsize='x-small')
    i = 0
    for c, l, mark in series:
        plt.plot(ox_list[i], m_list[i], color=c, label=l, marker=mark, markersize=5, markevery=25, alpha=0.8)
        i += 1
    legend = plt.legend(loc = 'lower right', framealpha=0.5, fontsize='small', fancybox=True, prop={'size': 'x-small'})
    legend.get_frame().set_linewidth(0.5)
    plt.xlabel('Rozegranych gier ($\\times$ 1000)', size='x-small')
    plt.ylabel('Odsetek wygranych gier [$\%$]', size='x-small')
    s2 = plt.twiny()
    plt.xlabel('Pokolenie', size='x-small')
    s2.set_xticks([0, 40, 80, 120, 160, 200])
    s2.tick_params(labelsize='x-small')


def draw_right(m_list, last_list):
    s = plt.subplot(1, 2, 2)
    i = 1
    for m in m_list:
        plt.scatter(i, m[199])
        i += 1
    plt.boxplot(last_list, notch=True, sym='b+')
    s.yaxis.tick_right()
    [i.set_linewidth(0.5) for i in s.spines.itervalues()]
    plt.tick_params(labelsize='x-small')
    plt.grid(True, alpha=0.5, linewidth=0.3)
    plt.axis((0.5, 5.5, 60, 100), size='small')
    plt.xticks(range(1, 6), ['1-Evol-RS', '1-Coev-RS', '2-Coev-RS', '1-Coev', '2-Coev'], rotation=20, size='x-small')


def main():
    font = {'family': 'Times New Roman', 'weight': 'normal', 'size': 13}
    plt.rc('font', **font)
    plt.figure(figsize=(6, 5), dpi=80)

    names = ['rsel.csv', 'cel-rs.csv', '2cel-rs.csv', 'cel.csv', '2cel.csv']
    m_list = []
    ox_list = []
    last_list = []
    for name in names:
        m, ox, last = load_data(name)
        m_list.append(m)
        ox_list.append(ox)
        last_list.append(last)
    series = [['blue', '1-Evol-RS', 'o'], ['green', '1-Coev-RS', 'v'], ['red', '2-Coev-RS', 'D'],
        ['black', '1-Coev', 's'], ['magenta', '2-Coev', 'd']]

    draw_left(m_list, ox_list, series)
    draw_right(m_list, last_list)

    plt.savefig('myplot.pdf')
    plt.close()

if __name__ == '__main__':
    main()