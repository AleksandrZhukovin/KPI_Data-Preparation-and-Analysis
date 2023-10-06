from spyre import server
from urllib.request import urlopen
from datetime import datetime
import pandas as pd

server.include_df_index = True


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


regions = {'1': 'Cherkasy', '2': 'Chernihiv', '3': 'Chernivtsi', '4': 'Crimea', '5': "Dnipropetrovs'k", '6': "Donets'k",
           '7': "Ivano-Frankivs'k", '8': 'Kharkiv', '9': 'Kherson', '10': "Khmel'nyts'kyy", '11': 'Kiev',
           '12': 'KievCity', '13': 'Kirovohrad', '14': "Luhans'k", '15': "L'viv", '16': 'Mykolayiv', '17': 'Odessa',
           '18': 'Poltava', '19': 'Rivne', '20': "Sevastopol'", '21': 'Sumy', '22': "Ternopil'", '23': 'Transcarpathia',
           '24': 'Vinnytsya', '25': 'Volyn', '26': 'Zaporizhzhya', '27': 'Zhytomyr'}


class StockExample(server.App):
    title = "Region Data"

    inputs = [{
        "type": 'dropdown',
        "label": 'Region',
        "options": [{'label': regions[i], 'value': i} for i in regions],
        "value": 'Dnipro',
        "key": 'region'
    }, {
        "type": 'dropdown',
        "label": 'Year',
        "options": [{'label': str(i), 'value': str(i)} for i in range(1982, 2024)],
        "value": '1982',
        "key": 'year'
    }, {
        "type": "text",
        "key": "weeks",
        "label": "Weeks range separated with -"
    }]

    controls = [{
        "type": "button",
        "id": "update_data",
        "label": "Upload Data"
    }]

    tabs = ["Plot", "Table"]

    outputs = [
        {
            "type": "plot",
            "id": "plot",
            "control_id": "update_data",
            "tab": "Plot"},
        {
            "type": "table",
            "id": "table_id",
            "control_id": "update_data",
            "tab": "Table",
            "on_page_load": True
        }
    ]

    def getData(self, params):
        region = params['region']
        year = params['year']
        start_week = float(params['weeks'].split('-')[0])
        finish_week = float(params['weeks'].split('-')[1])
        print(params['weeks'])
        df = pd.read_csv(f'data/vhi_id_{region}_00-10-05_06.10.2023.csv', index_col=False, header=1, skiprows=0)
        vhi_data = df[(df['year'] == int(year)) & (df['week'] > start_week) & (df['week'] < finish_week)][['SMN', 'SMT',
                                                                                                           'VCI', 'TCI',
                                                                                                           'VHI']]
        return vhi_data

    def getPlot(self, params):
        df = self.getData(params)
        plt_obj = df.plot()
        plt_obj.set_ylabel("Price")
        plt_obj.set_xlabel("Date")
        plt_obj.set_title(regions[params['region']])
        return plt_obj.get_figure()


app = StockExample()
app.launch(port=8000)

test = 'Hello world'
