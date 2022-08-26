# -*- coding: utf-8 -*-
import csv
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib as mpl
from operator import itemgetter
import seaborn as sns
import json
from ast import literal_eval

mpl.rcParams['font.sans-serif'] = ['KaiTi']
mpl.rcParams['font.serif'] = ['KaiTi']
mpl.rcParams['axes.unicode_minus'] = False

sns.set_style("darkgrid", {"font.sans-serif": ['KaiTi', 'Arial']})

hotwords = {}

with open("C:/Users/Innov/OneDrive/Desktop/NMN_ID.csv", encoding='utf-8') as csv_file:
    df = pd.read_csv(csv_file, delimiter=',')
    for entry in df['Keywords']:
        if entry == "{}":
            pass
        else:
            thing = literal_eval(entry)
            for word in thing:
                if word in hotwords:
                    hotwords[word] += thing[word]
                else:
                    hotwords[word] = thing[word]

g = open('C:/Users/Innov/OneDrive/Desktop/cool.csv', 'w', encoding='UTF-8', newline='')
writer = csv.DictWriter(g, fieldnames=hotwords.keys())
writer.writeheader()
writer.writerow(hotwords)
g.close()
