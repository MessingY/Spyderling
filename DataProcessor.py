# -*- coding: utf-8 -*-
import csv
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib as mpl
from operator import itemgetter
import seaborn as sns

mpl.rcParams['font.sans-serif'] = ['KaiTi']
mpl.rcParams['font.serif'] = ['KaiTi']
mpl.rcParams['axes.unicode_minus'] = False

sns.set_style("darkgrid", {"font.sans-serif": ['KaiTi', 'Arial']})

with open("C:/Users/Innov/OneDrive/Desktop/NMNData.csv", encoding='utf-8') as csv_file:
    df = pd.read_csv(csv_file, delimiter=',')
    sellers = df['Seller'].unique()
    price = df['Price (RMB)']
    origins = df['Origin'].unique()
    forms = df['Form'].unique()
    deals = df['Deal (# Bottles)'].unique()
    cap_per_btl = df['# Capsules/Bottle'].unique()
    mg_per_cap = df['Mass per Capsule (mg/cap)'].unique()
    mg_per_btl = df['Total Mg/bottle'].unique()

    column_names = [
        'Seller',
        'Origin',
        'Deal (# Bottles)',
        '# Capsules/Bottle',
        'Mass per Capsule (mg/cap)',
        'Total Mg/bottle'
    ]
    for column_name in column_names:
        count = {}
        for i in range(0, len(df[column_name])):
        # for i in range(0, 30):
            if df[column_name][i] not in count:
                count[df[column_name][i]] = 1
            else:
                count[df[column_name][i]] += 1
        count = {k: v for k, v in sorted(count.items(), key=lambda item: item[1])}
        curr_df = pd.DataFrame({column_name: count.keys(), 'Occurances': count.values()})
        ax = curr_df.plot.bar(x=column_name, y='Occurances', rot=45)
        # wm = plt.get_current_fig_manager()
        # wm.window.state('zoomed')
        plt.tight_layout
        plt.show()
        print(count)
    fig, ax = plt.subplots()

    colors = {
        '美国': 'blue',
        '中国香港': 'green',
        '日本': 'red',
        '法国': 'blue',
        '澳大利亚': 'blue',
        '丹麦': 'blue',
        '加拿大': 'blue',
        '英国': 'blue'
    }

    # scatter = ax.scatter(df['Index'], df['Total Mg/bottle'], c=df['Origin'].map(colors), label=colors)

    # sns.barplot('Index', 'Price per mg (RMB/mg)', data=df.head(50), hue='Origin')
    # plt.legend(bbox_to_anchor=(1.05, 1), borderaxespad=0.)
    # sns.histplot(x='Deal (# Bottles)', data=df.head(50))

    # plt.legend(
    #     handles=scatter.legend_elements()[0],
    #     labels=colors.keys(),
    #     title="Origins"
    # )

    # plt.show()
