from urllib.request import urlopen
from datetime import datetime
import pandas as pd


def data_download():
    now = datetime.now()
    current_date_time = now.strftime('%H-%M-%S_%d.%m.%Y')
    for i in range(1, 28):
        url = f"https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={i}&year1=1981&year2=2023&type=Mean"
        vhi_url = urlopen(url)
        with open(f'data/vhi_id_{i}_{current_date_time}.csv', 'w') as out:
            data = vhi_url.read().decode('utf-8').replace('<br>', '').replace('<tt><pre>', '').replace('</pre></tt>', '').replace(' ', '').split('\n')
            province = data.pop(0)
            province = province.split(':')[1].split(',')[0]
            out.write(f'{province}\n'+'\n'.join(data))
        print("VHI is downloaded...")


def data_read():
    data = pd.DataFrame(columns=['region', 'year', 'week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI'])
    for i in range(1, 28):
        region = pd.read_csv(f'data/vhi_id_{i}_00-44-34_22.09.2023.csv', index_col=False, header=1, skiprows=0)
        with open(f'data/vhi_id_{i}_00-44-34_22.09.2023.csv', 'r') as file:
            region['region'] = file.readline().replace('\n', ' ').replace("'", '')
        data = pd.concat([data, region[(region['year'] == 2000.0) & (region['week'] == 18.0)]])
    data.index = [22, 24, 23, 25, 3, 4, 8, 19, 20, 21, 9, 0, 10, 11, 12, 13, 14, 15, 16, 0, 17, 18, 6, 1, 2, 7, 5]
    data.sort_index(inplace=True)
    return data


def min_max_VHI(year, region):
    data = pd.read_csv(f'data/vhi_id_{region}_00-44-34_22.09.2023.csv', index_col=False, header=1, skiprows=0)
    min_v = data[(data['year'] == year) & (data['VHI'] != -1.00)]['VHI'].min()
    max_v = data[(data['year'] == year) & (data['VHI'] != -1.00)]['VHI'].max()
    return min_v, max_v


def thershold_VHI(region, threshold):
    data = pd.read_csv(f'data/vhi_id_{region}_00-44-34_22.09.2023.csv', index_col=False, header=1, skiprows=0)
    vhi_data = data[(data['VHI'] != -1.00)][['VHI', 'year']]
    over_threshold = set(data[(data['VHI'] > threshold)]['year'])
    return vhi_data, over_threshold


def normal_VHI(region, threshold):
    data = pd.read_csv(f'data/vhi_id_{region}_00-44-34_22.09.2023.csv', index_col=False, header=1, skiprows=0)
    vhi_data = data[(data['VHI'] != -1.00)][['VHI', 'year']]
    over_threshold = set(data[(data['VHI'] < threshold)]['year'])
    return vhi_data, over_threshold
