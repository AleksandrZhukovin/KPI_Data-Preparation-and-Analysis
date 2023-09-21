from urllib.request import urlopen
from datetime import datetime


def data_download():
    now = datetime.now()
    current_date_time = now.strftime('%H-%M-%S_%d.%m.%Y')
    for i in range(1, 28):
        url = f"https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={i}&year1=1981&year2=2023&type=Mean"
        vhi_url = urlopen(url)
        with open(f'vhi_id_{i}_{current_date_time}.csv', 'wb') as out:
            out.write(vhi_url.read())
        print("VHI is downloaded...")


data_download()
