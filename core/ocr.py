# coding:utf-8
import base64
import json
import requests
from aip import AipOcr

""" 你的 APPID AK SK """
APP_ID = '23718158'
API_KEY = 'hWjONQOWLrGdvqyX7f23vfbt'
SECRET_KEY = 'Yb8peHCPLr2juYOXSTLxoodSq23pePkn'


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def get_baidu_ocr_result(image):
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    """ 调用通用文字识别, 图片参数为本地图片 """
    # result = client.form(image)
    result = client.basicGeneral(image)

    return result


def get_aliyun_ocr_result(image):
    # import pydevd
    # pydevd.settrace('localhost', port=9650, stdoutToServer=True, stderrToServer=True)

    url = 'https://form.market.alicloudapi.com/api/predict/ocr_table_parse'
    image_base64 = str(base64.b64encode(image), encoding='utf-8')
    data = {'image': image_base64,
            "configure": {
                'format': 'json',
                'dir_assure': True,
                'line_less': False
            }}

    headers = {'Authorization': 'APPCODE 78bd71353ab04656b1a12a46cb5890c1'}
    res = requests.post(url, json=data, headers=headers)
    result = res.json()
    return result['tables']


if __name__ == '__main__':
    image = get_file_content('e:/2021-05-02-19-50-26.jpg')
    xlsx = get_aliyun_ocr_result(image)
    with open('e:/output.xlsx', 'wb') as fout:
        fout.write(base64.b64decode(xlsx))
    import pandas as pd
    df = pd.read_excel(base64.b64decode(xlsx))
    print(df)
