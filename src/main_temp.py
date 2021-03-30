import os
import codecs
import pandas as pd
import glob

from util import Util


util = Util()

if __name__ == '__main__':

    input_path = '../data/input/*.csv'
    output_path = '../data/output/working_data.csv'
    config_path = '../config/config.json'

    config_data = Util.config_load(config_path)

    data_list = []
    for path in glob.glob(input_path): # input_pathに存在するファイルの一覧を取得し処理
        data = Util.read_csv(path)
        data_list.append(data)
    working_data = pd.concat(data_list, axis=0, sort=True)

    working_data['作業工数（Ｈ）'] = working_data['時間'].astype(float)
    working_data['区分'] = working_data['タイトル'].map(lambda x:str(x).split('_')[0])

    # working_data['管理No'], working_data['テーマ名'], working_data['事業分類'] , working_data['荷主'], working_data['作業タスク'], working_data['請求集計区分'] = working_data['区分'].apply(Util.mapping, config_data=config_data)
    # working_data = working_data.apply(Util.mapping, config_data=config_data, axis=1)
    working_data = Util.mapping(working_data, config_data)

    working_data['作業日'] = working_data['開始日時'].str.replace('/', '-')

    Util.output_csv(working_data.reindex(columns=['管理No', 'テーマ名', '事業分類', '荷主', '対応システム', 
    '作業タスク', '請求集計区分', '作業日', '作業工数（Ｈ）', '作業詳細']) , output_path)
