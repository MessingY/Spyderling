
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib as mpl
from operator import itemgetter
import seaborn as sns
import os
import csv
import pandas as pd

mpl.rcParams['font.sans-serif'] = ['KaiTi']
mpl.rcParams['font.serif'] = ['KaiTi']
mpl.rcParams['axes.unicode_minus'] = False

sns.set_style("darkgrid", {"font.sans-serif": ['KaiTi', 'Arial']})

font = fm.FontProperties(fname='c:\\windows\\fonts\\Deng.ttc')
with open("C:/Users/Innov/OneDrive/Documents/NMN.csv", encoding='utf-8') as csvfile:
    df = pd.read_csv(csvfile)

    "Cleaning the comment count numbers"
    index = 0
    while index < len(df['Seller']):
        if df.loc[index, 'Comment Count'][-1] == '+':
            df.loc[index, 'Comment Count'] = int(df.loc[index, 'Comment Count'][:-1])
        index += 1

    "Cleaning the weight count numbers"
    index = 0
    while index < len(df['Weight']):
        if df.loc[index, 'Weight'][-2:] == "kg":
            df.loc[index, 'Weight'] = int(float(df.loc[index, 'Weight'][:-2]) * 1000)
        elif df.loc[index, 'Weight'][-1] == 'g':
            df.loc[index, 'Weight'] = int(float(df.loc[index, 'Weight'][:-1]))
        index += 1

    """Creating the price per gram column"""
    index = 0
    pw_index = []
    while index < len(df['Weight']):
        pw_index.append(
            df.loc[index, 'Price']/df.loc[index, 'Weight']
        )
        index += 1
    df['Price per Gram'] = pw_index
    df.to_csv("C:/Users/Innov/OneDrive/Documents/NMN.csv", index=False)

    # counts = {}
    # for item in reader:
    #     if item[3] in counts:
    #         counts[item[3]] += 1
    #     else:
    #         counts[item[3]] = 1
    # counts = dict(sorted(counts.items(), key=lambda counts: counts[1], reverse=False))
    # print(counts)
    # counts.pop('Seller')
    # sellers = counts.keys()
    # counter = 0
    # small_presence = []
    # for seller in sellers:
    #     if counts[seller] == 1 or counts[seller] == 2:
    #         counter += 1
    #         small_presence.append(seller)
    # for seller in small_presence:
    #     counts.pop(seller)
    # # counts['Others'] = counter
    # print(counts)
    # df = pd.DataFrame({'Figure': counts.values()}, index=counts.keys())
    # plot = df.plot.pie(y='Figure', radius=1, labeldistance=1, startangle=90)
    # plt.show()
