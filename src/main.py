import os
import codecs
import pandas as pd
import glob

from util import Util
from get_event import Get_event

util = Util()

if __name__ == '__main__':

    output_path = '../data/output/working_data.csv'
    config_path = '../config/config.json'

    config_data = Util.config_load(config_path)

    timefrom = '2021/03/01'
    timeto = '2021/03/30'

    get_event = Get_event(timefrom, timeto)
    working_data = get_event.get_event()

    working_data['作業工数（Ｈ）'] = working_data['時間'].astype(float)
    working_data['区分'] = working_data['作業詳細'].map(lambda x:str(x).split('_')[0])

    working_data = Util.mapping(working_data, config_data)
    working_data['作業日'] = working_data['作業日'].str.replace('/', '-')

    Util.output_csv(working_data.reindex(columns=['管理No', 'テーマ名', '事業分類', '荷主', '対応システム', 
    '作業タスク', '請求集計区分', '作業日', '作業工数（Ｈ）', '作業詳細']) , output_path)
