import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
# import sys


# np.set_printoptions(threshold=sys.maxsize)
# https://archive.ics.uci.edu/dataset/183/communities+and+crime dataset
df = pd.read_csv('data/communities.data', names=['state', 'county', 'community', 'population', 'householdsize'],
                 usecols=[0, 1, 2, 4, 5], na_values='?', dtype=float)

ar = np.genfromtxt('data/communities.data', dtype=float, names=['state', 'county', 'community', 'population',
                                                                'householdsize'],
                   usecols=[0, 1, 2, 4, 5], missing_values='?', delimiter=',', filling_values=0)


def fill_df_na():
    df.fillna(0)
    for i in ['county', 'community', 'population', 'householdsize']:
        df[i].fillna(df[i].mean(), inplace=True)


def fill_ar_na():
    for i in ['county', 'community', 'population', 'householdsize']:
        n = 0
        mean = np.mean(ar[i][ar[i] != 0])
        for a in ar[i]:
            ar[i][n] = mean if a == 0. else a
            n += 1


def normalize_df():
    for i in ['county', 'community', 'population', 'householdsize']:
        mean = df[i].mean()
        std = df[i].std()
        for a in range(len(df[i])):
            df.at[a, i] = (df.at[a, i] - mean) / std


def normalize_ar():
    min_max_county = (np.std(ar['county']), np.mean(ar['county']))
    min_max_community = (np.std(ar['community']), np.mean(ar['community']))
    min_max_population = (np.std(ar['population']), np.mean(ar['population']))
    min_max_householdsize = (np.std(ar['householdsize']), np.mean(ar['householdsize']))
    n = 0
    for i in ar:
        ar[n][1] = (i[1] - min_max_county[1]) / min_max_county[0]
        ar[n][2] = (i[2] - min_max_community[1]) / min_max_community[0]
        ar[n][3] = (i[3] - min_max_population[1]) / min_max_population[0]
        ar[n][4] = (i[4] - min_max_householdsize[1]) / min_max_householdsize[0]
        n += 1


normalize_df()
normalize_ar()


def plotting_ar(atr, *args):
    for i in range(1, len(args) + 1):
        plt.subplot(2, 3, i % 5 if i % 5 != 0 else 5)
        plt.hist(ar[atr][args[i - 1][0]:args[i - 1][1]], label=f'{args[i - 1][0]} - {args[i - 1][1]}')
        plt.legend()
        plt.xlabel(atr.title())
    plt.tight_layout()
    # plt.show()


# plotting_ar('community', (10, 100), (100, 200), (200, 300), (300, 400), (400, 500), (500, 600), (600, 700), (700, 800),
#                          (800, 900), (900, 1000))


def plotting_df(atr, *args):
    for i in range(1, len(args) + 1):
        plt.subplot(2, 3, i % 5 if i % 5 != 0 else 5)
        plt.hist(df[atr][args[i - 1][0]:args[i - 1][1]], label=f'{args[i - 1][0]} - {args[i - 1][1]}')
        plt.legend()
        plt.xlabel(atr.title())
    plt.tight_layout()
    # plt.show()

# plotting_df('community', (10, 100), (100, 200), (200, 300), (300, 400), (400, 500), (500, 600), (600, 700), (700, 800),
#                          (800, 900), (900, 1000))


def cor_plot_df(atr_1, atr_2):
    sns.kdeplot(data=df, x=atr_1, hue=atr_2)
    # plt.show()


def cor_plot_ar(atr_1, atr_2):
    data_frame = pd.DataFrame(ar)
    sns.kdeplot(data=data_frame, x=atr_1, hue=atr_2)
    # plt.show()


def pearson_ar(atr_1, atr_2):
    ar_pearson = stats.pearsonr(ar[atr_1], ar[atr_2]).statistic
    return ar_pearson


def pearson_df(atr_1, atr_2):
    df_pearson = stats.pearsonr(df[atr_1], df[atr_2]).statistic
    return df_pearson

# print(pearson('community', 'householdsize'))


def one_hot_ar():
    global ar
    ar = ar.view(np.float64).reshape(ar.shape + (-1,))
    with open('data/states.txt', 'r') as file:
        states = [i.replace('\n', '') for i in file.readlines()]
        states.insert(0, '')
        states.extend(['California' for i in range(6)])
    sta = []
    for i in range(len(ar[:, 0])):
        sta.append(states[int(ar[:,0][i])])
    sta = np.array(sta).reshape((len(ar[:, 0]), 1))
    oh = OneHotEncoder()
    new = oh.fit_transform(sta).toarray()
    new = np.hstack((new, ar))
    return new


def one_hot_df():
    global df
    with open('data/states.txt', 'r') as file:
        states = [i.replace('\n', '') for i in file.readlines()]
        states.insert(0, '')
        states.extend(['California' for i in range(6)])
    df.replace([np.float64(i) for i in range(1, 58)], states, inplace=True)
    oh = OneHotEncoder()
    new = oh.fit_transform(df['state'].to_numpy().reshape((-1, 1))).toarray()
    new = pd.DataFrame(new)
    new = pd.concat([df, new], axis=1).drop('state', axis=1)
    return new


def viz_3d_df():
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    xs = df['community']
    ys = df['householdsize']
    zs = df['county']
    ax.scatter(xs, ys, zs, s=50, alpha=0.6, edgecolors='w')
    ax.set_xlabel('Community')
    ax.set_ylabel('Household Size')
    ax.set_zlabel('County')
    # plt.show()


def viz_3d_ar():
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    xs = ar['community']
    ys = ar['householdsize']
    zs = ar['county']
    ax.scatter(xs, ys, zs, s=50, alpha=0.6, edgecolors='w')
    ax.set_xlabel('Community')
    ax.set_ylabel('Household Size')
    ax.set_zlabel('County')
    # plt.show()


def np_reg():
    data = train_test_split(ar, test_size=0.5, train_size=0.5)
    reg = linear_model.LinearRegression()
    reg.fit(data[0]['community'].reshape(1, -1), data[0]['householdsize'].reshape(1, -1))
    print(mean_squared_error(data[1]['householdsize'].reshape(1, -1),
                             reg.predict(data[1]['community'].reshape(1, -1))))

    reg1 = linear_model.Lasso(alpha=0.1)
    reg1.fit(data[0]['community'].reshape(1, -1), data[0]['householdsize'].reshape(1, -1))
    print(mean_squared_error(data[1]['householdsize'].reshape(1, -1),
                             reg1.predict(data[1]['community'].reshape(1, -1))))

    reg2 = linear_model.LassoLars(alpha=.1)
    reg2.fit(data[0]['community'].reshape(1, -1), data[0]['householdsize'].reshape(1, -1))
    print(mean_squared_error(data[1]['householdsize'].reshape(1, -1),
                             reg2.predict(data[1]['community'].reshape(1, -1))))


def df_reg():
    data = train_test_split(df, test_size=0.5, train_size=0.5)
    reg = linear_model.LinearRegression()
    reg.fit(data[0]['community'].to_numpy().reshape(1, -1), data[0]['householdsize'].to_numpy().reshape(1, -1))
    print(mean_squared_error(data[1]['householdsize'].to_numpy().reshape(1, -1),
                             reg.predict(data[1]['community'].to_numpy().reshape(1, -1))))

    reg1 = linear_model.Lasso(alpha=0.1)
    reg1.fit(data[0]['community'].to_numpy().reshape(1, -1), data[0]['householdsize'].to_numpy().reshape(1, -1))
    print(mean_squared_error(data[1]['householdsize'].to_numpy().reshape(1, -1),
                             reg1.predict(data[1]['community'].to_numpy().reshape(1, -1))))

    reg2 = linear_model.LassoLars(alpha=.1)
    reg2.fit(data[0]['community'].to_numpy().reshape(1, -1), data[0]['householdsize'].to_numpy().reshape(1, -1))
    print(mean_squared_error(data[1]['householdsize'].to_numpy().reshape(1, -1),
                             reg2.predict(data[1]['community'].to_numpy().reshape(1, -1))))
