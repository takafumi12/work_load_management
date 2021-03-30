import logging
import os
import json
import codecs
import pandas as pd

class Util:

    @classmethod
    def read_csv(cls, path:str):
        with codecs.open(path, 'r', encoding='CP932', errors='ignore') as f:
            return pd.read_csv(f, usecols=['タイトル', '開始日時', '終了日時', '時間'], dtype='object')

    @classmethod
    def output_csv(cls, df:pd.DataFrame ,path:str):
        df.to_csv(path, index=False, encoding='shift-jis')

    @classmethod
    def config_load(cls, path):
        with codecs.open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return json.load(f)

    @classmethod
    def mapping(cls, df, config_data):
        for idx, key in zip(df.index, df['区分'].values):
            try:
                config = config_data[key]
                df.at[idx, '管理No'] = config['管理No']
                df.at[idx, 'テーマ名'] = config['テーマ名']
                df.at[idx, '事業分類'] = config['事業分類']
                df.at[idx, '荷主'] = config['荷主']
                df.at[idx, '作業タスク'] = config['作業タスク']
                df.at[idx, '請求集計区分'] = config['請求集計区分']
            except Exception:
                pass

        return df

